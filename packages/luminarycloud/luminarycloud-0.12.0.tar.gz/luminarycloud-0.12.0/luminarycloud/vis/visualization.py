from .._proto.api.v0.luminarycloud.vis import vis_pb2
from .._client import get_default_client
from ..solution import Solution
from ..mesh import get_mesh_metadata, Mesh
from ..geometry import Geometry
from ..enum.vis_enums import *
from ..simulation import get_simulation
from .display import DisplayAttributes, ColorMap
from .filters import Filter, PlaneClip, Slice, BoxClip
from .util import *
from luminarycloud.types import Vector3
import io

from luminarycloud._proto.client import simulation_pb2 as clientpb

from typing import List, cast
import requests
from time import time, sleep
import logging
import dataclasses as dc

logger = logging.getLogger(__name__)


@dc.dataclass
class DirectionalCamera:
    """
    Class defining a directional camera for visualization. Directional
    camera are oriented around the visible objects in the scene and will
    always face towards the scene.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name : str
        A user defined name for the camera.
    direction : CameraDirection
        The orientation of the camera. Default: X_POSITIVE
    projection : CameraProjection
        The type of projection used for the camera. Default: ORTHOGRAPHIC
    """

    name: str = "default directional camera"
    direction: CameraDirection = CameraDirection.X_POSITIVE
    projection: CameraProjection = CameraProjection.ORTHOGRAPHIC


@vector3_wrapper
@dataclass
class LookAtCamera:
    """
    Class defining a look at camera for visualization.  Unlike the directional
    camera which is placed relative to what is visisble, the the look at camera
    is an explict camera, meaning that we have to fully specify the parameters.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    look_at: Vector3
        The point the camera is looking at. Default (0,0,0)
    position: Vector3
        The position of the camera. Default (0,1,0)
    up: Vector3
        The up vector for the camera. Default (0,0,1)
    projection : CameraProjection
        The type of projection used for the camera. Default: ORTHOGRAPHIC

    """

    name: str = "default look at camera"
    look_at: Vector3 = field(default_factory=lambda: Vector3(x=0, y=0, z=0))
    position: Vector3 = field(default_factory=lambda: Vector3(x=0, y=1, z=0))
    up: Vector3 = field(default_factory=lambda: Vector3(x=0, y=0, z=1))
    projection: CameraProjection = CameraProjection.ORTHOGRAPHIC


class ImageExtract:
    """
    The image extract represents the request to extract an image from some data.
    The operation exectutes asyncronously, so the caller must check the status of the
    image extract. If the status is completed, then the resuling image is available
    for download.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name: str
        The user provided name of the extract.
    description: str
        The user provided description of the extract.
    status: ImageStatusType
        The status of the extract (i.e., has it completed or not).
    _extract_id: str
        The unique indentifier of the extract.
    _project_id: str
        The project id associated with the extract.
    _deleted: bool
        Internal flag to track if the extract has been deleted.
    """

    def __init__(
        self, extract_id: str, project_id: str, name: str, desciption: str, status: ImageStatusType
    ):
        # TODO(matt): We could make all of these read only.
        self._extract_id: str = extract_id
        self._project_id: str = project_id
        self.status: ImageStatusType = status
        self.name: str = name
        self.description: str = desciption
        self._deleted = False

    def __repr__(self) -> str:
        return f"ImageExtract(Id: {self._extract_id} status: {self.status})"

    def refresh(self) -> "ImageExtract":
        """
        Refesh the status of the ImageExtract.

        Returns
        -------
        self
        """
        self._fail_if_deleted()
        image = get_image(self._project_id, self._extract_id)
        self.status = image.status
        return self

    def wait(
        self, interval_seconds: float = 5, timeout_seconds: float = float("inf")
    ) -> ImageStatusType:
        """
        Wait until the ImageExtract is completed or failed.

        Parameters
        ----------
        interval : float, optional
            Number of seconds between polls.
        timeout : float, optional
            Number of seconds before timeout.

        Returns
        -------
        ImageStatusType: Current status of the image extract.
        """
        self._fail_if_deleted()
        deadline = time() + timeout_seconds
        while True:
            self.refresh()

            if self.status in [
                ImageStatusType.COMPLETED,
                ImageStatusType.FAILED,
                ImageStatusType.INVALID,
            ]:
                return self.status
            if time() >= deadline:
                logger.error("`ImageExtract: wait ` timed out.")
                raise TimeoutError
            sleep(max(0, min(interval_seconds, deadline - time())))

    def download_image(self) -> "io.BytesIO":
        """
        Downloads the resulting jpeg image as a binary buffer. This is useful
        for displaying images in notebooks.  If that status is not complete, an
        error will be raised.

        .. warning:: This feature is experimental and may change or be removed in the future.

        """
        self._fail_if_deleted()
        self.refresh()
        if self.status != ImageStatusType.COMPLETED:
            raise Exception("download_image: status not complete.")
        req = vis_pb2.DownloadImageRequest()
        req.extract_id = self._extract_id
        req.project_id = self._project_id
        res: vis_pb2.DownloadImageResponse = get_default_client().DownloadImage(req)
        buffer = io.BytesIO()

        if res.file.signed_url:
            response = requests.get(res.file.signed_url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                buffer.write(chunk)
        elif res.file.full_contents:
            buffer.write(res.file.full_contents)
        else:
            raise Exception("download_image respose contains no data.")

        # Reset buffer position to the beginning for reading
        buffer.seek(0)
        return buffer

    def save_image(self, file_name: str) -> None:
        """
        Download and save resulting image to the file system. If that status is not
        complete, an error will be raised.

        .. warning:: This feature is experimental and may change or be removed in the future.

        Parameters
        ----------
        file_name: str, required
            The file name to save the image to. '.jpg' will be appended to the file name.
        """
        if not file_name:
            raise ValueError("file_name must be non-empty")

        binary = self.download_image()
        output_file = file_name + ".jpg"
        with open(output_file, "wb") as file:
            file.write(binary.getvalue())

    def _fail_if_deleted(self) -> None:
        if self._deleted:
            raise ValueError("ImageExtract has been deleted.")

    def delete(self) -> None:
        """Delete the image."""
        self._fail_if_deleted()
        req = vis_pb2.DeleteImageRequest()
        req.extract_id = self._extract_id
        req.project_id = self._project_id
        get_default_client().DeleteImage(req)
        self._deleted = True


class Scene:
    """
    The scene class is the base for any visualization. The scene is constructed
    with what "entity" you want to visualize: a solution, a mesh, or
    a geometry.

    global display attributes: The global display attributes control the default
    appearance of all the surfaces (i.e. boundaries). Attributes include visibitiy,
    what fields are displayed on the surfaces (if applicable), and representation
    (e.g., surface, surface with edges, ...).

    Individaul surface visibities can be overidden to hide/show specific surfaces.
    Additionally, if the scene is contructed around a simulation, a helper method is
    provided to automatically hide surfaces associated with far fields.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    global_display_attrs : DisplayAttributes
        These attributes apply to all the surfaces in the
        geometry/mesh/solution. Individual surface visibilities can be
        overridden with the 'surface_visibility' function.
    """

    def __init__(self, project_id: str, entity: Geometry | Solution | Mesh):
        # Global display attrs
        self.global_display_attrs = DisplayAttributes()
        self._filters: List[Filter] = []
        self._color_maps: List[ColorMap] = []
        self._camera: DirectionalCamera | LookAtCamera = DirectionalCamera()
        self._entity_type: EntityType = EntityType.SIMULATION

        # TODO(matt): remove project id when its accessible from the solution
        # object.
        if not isinstance(project_id, str):
            raise TypeError(f"Expected 'str', got {type(project_id).__name__}")
        self._project_id = project_id

        # Find out what we are working on.
        if isinstance(entity, Solution):
            self._solution: Solution = entity
            self._entity_type = EntityType.SIMULATION
        elif isinstance(entity, Mesh):
            self._mesh: Mesh = entity
            self._entity_type = EntityType.MESH
        elif isinstance(entity, Geometry):
            self._geometry: Geometry = entity
            self._entity_type = EntityType.GEOMETRY
        else:
            raise TypeError(f"Expected Solution, Mesh or Geometry, got {type(entity).__name__}")

        self._surface_visibilities: dict[str, bool] = {}

        # Find all the surfaces from the metadata.
        mesh_meta = None
        if self._entity_type == EntityType.SIMULATION:
            simulation = get_simulation(self._solution.simulation_id)
            mesh_meta = get_mesh_metadata(simulation.mesh_id)
        elif self._entity_type == EntityType.MESH:
            mesh_meta = get_mesh_metadata(self._mesh.id)

        self._surface_ids = []
        if mesh_meta:
            for zone in mesh_meta.zones:
                for bound in zone.boundaries:
                    self._surface_ids.append(bound.name)
        else:
            surface_list = self._geometry.list_entities()[0]
            for surface in surface_list:
                self._surface_ids.append(surface.id)

        self._far_field_boundary_ids: List[str] = []

        # Find all the far field surfaces if we can get the params.
        if self._entity_type == EntityType.SIMULATION:
            params = simulation.get_parameters()
            for physics in params.physics:
                if physics.fluid:
                    for bc in physics.fluid.boundary_conditions_fluid:
                        if bc.physical_boundary == clientpb.PhysicalBoundary.FARFIELD:
                            for bc_surface in bc.surfaces:
                                self._far_field_boundary_ids.append(bc_surface)

    def hide_far_field(self) -> None:
        """
        Hide all far fields surfaces. Will work if the entity is a simulation.
        """

        for boundary_id in self._far_field_boundary_ids:
            self.surface_visibility(boundary_id, False)

    def surface_ids(self) -> List[str]:
        """Get a list of all the surface ids associated with the mesh."""
        return self._surface_ids

    def surface_visibility(self, id: str, visible: bool) -> None:
        """Explicitly override the the visibility of a surface by id."""
        if not id in self._surface_ids:
            raise ValueError(f"Id {id} not a boundary id")
        self._surface_visibilities[id] = visible

    def add_filter(self, filter: Filter) -> None:
        """
        Add a filter to the scene. Filters not currently supported with geometries and will
        raise an error if added.
        """
        if not isinstance(filter, Filter):
            raise TypeError(f"Expected 'Filter', got {type(filter).__name__}")
        if self._entity_type == EntityType.GEOMETRY:
            raise ValueError("Filters with geometries are not currently supported.")
        elif self._entity_type == EntityType.MESH and not isinstance(
            filter, (BoxClip, PlaneClip, Slice)
        ):
            raise ValueError("Only 'BoxClip', 'PlaneClip', and 'Slice' are supported with meshes.")
        self._filters.append(filter)

    def add_color_map(self, color_map: ColorMap) -> None:
        """
        Add a color map to the scene. If a color map with the field
        already exists, it will be overwritten.
        """
        if not isinstance(color_map, ColorMap):
            raise TypeError(f"Expected 'ColorMap', got {type(filter).__name__}")

        # We can only have one color map per field, so check.
        found = False
        for cmap in self._color_maps:
            if cmap.field == color_map.field:
                found = True
                cmap = color_map
                logger.warning("Color map for field already exists. Overwriting.")

        if not found:
            self._color_maps.append(color_map)

    def set_camera(self, camera: DirectionalCamera | LookAtCamera) -> None:
        """Set the scene's camera."""
        if not isinstance(camera, (DirectionalCamera, LookAtCamera)):
            raise TypeError(
                f"Expected 'DirectionalCamera or LookAtCamera, got {type(camera).__name__}"
            )
        self._camera = camera

    def _create_request(
        self, width: int, height: int, name: str, description: str
    ) -> vis_pb2.CreateImageRequest:
        req = vis_pb2.CreateImageRequest()
        req.camera.name = self._camera.name
        req.camera.projection = self._camera.projection.value
        if isinstance(self._camera, LookAtCamera):
            lookat = cast(LookAtCamera, self._camera)
            req.camera.look_at.position.CopyFrom(lookat.position._to_proto())
            req.camera.look_at.up.CopyFrom(lookat.up._to_proto())
            req.camera.look_at.look_at.CopyFrom(lookat.look_at._to_proto())
        elif isinstance(self._camera, DirectionalCamera):
            directional = cast(DirectionalCamera, self._camera)
            req.camera.direction = self._camera.direction.value
        else:
            raise TypeError(f"Internal error: expected 'camera', got {type(self._camera).__name__}")

        req.camera.resolution.width = width
        req.camera.resolution.height = height
        req.global_display_attributes.visible = self.global_display_attrs.visible
        req.global_display_attributes.representation = (
            self.global_display_attrs.representation.value
        )
        req.global_display_attributes.field.component = (
            self.global_display_attrs.field.component.value
        )
        req.global_display_attributes.field.quantity_typ = (
            self.global_display_attrs.field.quantity.value
        )
        for id, visible in self._surface_visibilities.items():
            req.surface_visibilities[id] = visible
        for filter in self._filters:
            if isinstance(filter, Filter):
                vis_filter: vis_pb2.Filter = filter._to_proto()
                req.filters.append(vis_filter)
            else:
                raise TypeError(f"Expected 'filter', got {type(filter).__name__}")

        for cmap in self._color_maps:
            color_map: vis_pb2.ColorMap = cmap._to_proto()
            req.color_maps.append(color_map)

        req.project_id = self._project_id
        if self._entity_type == EntityType.SIMULATION:
            req.entity.simulation.id = self._solution.simulation_id
            req.entity.simulation.solution_id = self._solution.id
        elif self._entity_type == EntityType.MESH:
            req.entity.mesh.id = self._mesh.id
        elif self._entity_type == EntityType.GEOMETRY:
            req.entity.geometry.id = self._geometry.id
        else:
            raise ValueError(f"Unknown entity type: '{self._entity_type}' ")
        req.name = name
        req.description = description
        return req

    def create_image(self, width: int, height: int, name: str, description: str) -> ImageExtract:
        """
        Create an image of the scene using the camera.
        Parameters
        ----------
        width : int
            The width of the image.
        height : int
            The height of the image.
        name : str
            A short name for the image.
        description : str
           A longer description of the scene and image.
        """
        req: vis_pb2.CreateImageRequest = self._create_request(
            width=width, height=height, name=name, description=description
        )
        res: vis_pb2.CreateImageResponse = get_default_client().CreateImage(req)
        logger.info("Successfully submitted 'create_image' request")
        return ImageExtract(
            extract_id=res.image.extract_id,
            project_id=self._project_id,
            name=name,
            desciption=description,
            status=ImageStatusType(res.image.status),
        )


def get_image(project_id: str, extract_id: str) -> ImageExtract:
    """
    Get a previously created image by project and extract id.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Parameters
    ----------
    project_id : str
        The project id to of the extract.
    extract_id: str
        The id to of the extract.

    """
    req = vis_pb2.GetImageRequest()
    req.extract_id = extract_id
    req.project_id = project_id
    res: vis_pb2.GetImageResponse = get_default_client().GetImage(req)
    image_extract = ImageExtract(
        extract_id=extract_id,
        project_id=project_id,
        name=res.image.name,
        desciption=res.image.description,
        status=ImageStatusType(res.image.status),
    )
    return image_extract


def list_images(project_id: str, entity: Geometry | Mesh | Solution) -> List[ImageExtract]:
    """
    Lists all previously created image associated with a project and an entity.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Parameters
    ----------
    project_id : str
        The project id to query.
    entity : Geometry | Mesh | Solution
        Specifies what types of image extracts to list(e.g., geometry, mesh or solution).

    """
    if not isinstance(project_id, str):
        raise TypeError(f"Expected 'str', got {type(project_id).__name__}")

    # Find out what we are working on.
    entity_type: EntityType = EntityType.GEOMETRY
    if isinstance(entity, Solution):
        entity_type = EntityType.SIMULATION
    elif isinstance(entity, Mesh):
        entity_type = EntityType.MESH
    elif isinstance(entity, Geometry):
        entity_type = EntityType.GEOMETRY
    else:
        raise TypeError(f"Expected Solution, Mesh or Geometry, got {type(entity).__name__}")

    req = vis_pb2.ListImagesRequest()
    req.project_id = project_id

    if entity_type == EntityType.SIMULATION:
        # Make the linter happy
        sim_entity = cast(Solution, entity)
        req.entity.simulation.id = sim_entity.simulation_id
        req.entity.simulation.solution_id = sim_entity.id
    elif entity_type == EntityType.MESH:
        req.entity.mesh.id = entity.id
    elif entity_type == EntityType.GEOMETRY:
        req.entity.geometry.id = entity.id
    else:
        raise ValueError(f"Unknown entity type: '{entity_type}' ")

    res: vis_pb2.ListImagesResponse = get_default_client().ListImages(req)

    results: List[ImageExtract] = []
    for image in res.images:
        extract = ImageExtract(
            extract_id=image.extract_id,
            project_id=image.project_id,
            name=image.name,
            desciption=image.description,
            status=ImageStatusType(image.status),
        )

        # TODO(matt): the List images request is giving us nil for the status.
        # This need to be fixed on the backend, but manually refreshing works for now.
        extract.refresh()
        results.append(extract)

    return results
