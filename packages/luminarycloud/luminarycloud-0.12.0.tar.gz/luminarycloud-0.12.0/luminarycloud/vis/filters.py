from luminarycloud.types import Vector3
from luminarycloud.enum import VisQuantity
from .._proto.api.v0.luminarycloud.vis import vis_pb2
from .util import *
from abc import ABC, abstractmethod
import string, random, math
import dataclasses as dc
from .display import Field, DisplayAttributes


def generate_id(prefix: str) -> str:
    return prefix + "".join(random.choices(string.ascii_lowercase, k=24))


def set_filter_display_attrs(filter: vis_pb2.Filter, attrs: DisplayAttributes) -> None:
    filter.display_attrs.visible = attrs.visible
    filter.display_attrs.representation = attrs.representation.value
    filter.display_attrs.field.component = attrs.field.component.value
    filter.display_attrs.field.quantity_typ = attrs.field.quantity.value


@vector3_wrapper
@dataclass
class Plane:
    """
    This class defines a plane.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    origin : Vector3
        A point defined on the plane. Default: [0,0,0].
    normal : Vector3
        The vector orthogonal to the  plane. Default: [0,1,0]
    """

    origin: Vector3 = field(default_factory=lambda: Vector3(x=0, y=0, z=0))
    normal: Vector3 = field(default_factory=lambda: Vector3(x=1, y=0, z=0))


@vector3_wrapper
@dataclass
class Box:
    """
    This class defines a box used for filter such as box clip.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    center: Vector3
        A point defined at the center of the box. Default: [0,0,0].
    lengths: Vector3
        The the legnths of each side of the box. Default: [1,1,1]
    angles: Vector3
        The rotation of the box specified in Euler angles (degrees) and applied
        in XYZ ordering. Default: [0,0,0]
    """

    center: Vector3 = field(default_factory=lambda: Vector3(x=0, y=0, z=0))
    lengths: Vector3 = field(default_factory=lambda: Vector3(x=1, y=1, z=1))
    angles: Vector3 = field(default_factory=lambda: Vector3(x=0, y=0, z=0))


class Filter(ABC):
    """
    This is the base class for all filters. Each derived filter class
    is responsible for providing a _to_proto method to convert to a filter
    protobuf.

    .. warning:: This feature is experimental and may change or be removed in the future.
    """

    def __init__(self) -> None:
        self.display_attrs = DisplayAttributes()

    @abstractmethod
    def _to_proto(self) -> vis_pb2.Filter:
        pass


class Slice(Filter):
    """
    The slice filter is used to extract a cross-section of a 3D dataset by
    slicing it with a plane.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    plane : Plane
        The slice plane.
    name : str
        A user provided name for the filter.
    display_attrs : DisplayAttributes
        Specifies this filter's appearance.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._plane = Plane()
        self._project_vectors: bool = False
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id = generate_id("slice-")
        self.name = name

    @property
    def plane(self) -> Plane:
        return self._plane

    @plane.setter
    def plane(self, new_plane: Plane) -> None:
        if not isinstance(new_plane, Plane):
            raise TypeError(f"Expected 'Plane', got {type(new_plane).__name__}")
        self._plane = new_plane

    @property
    def project_vectors(self) -> bool:
        return self._project_vectors

    @project_vectors.setter
    def project_vectors(self, new_project_vectors: bool) -> None:
        if not isinstance(new_project_vectors, bool):
            raise TypeError(f"Expected 'bool', got {type(new_project_vectors).__name__}")
        self._project_vectors = new_project_vectors

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.slice.plane.origin.CopyFrom(self.plane.origin._to_proto())
        vis_filter.slice.plane.normal.CopyFrom(self.plane.normal._to_proto())
        vis_filter.slice.project_vectors = self.project_vectors
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter


class PlaneClip(Filter):
    """
    Clip the dataset using a plane. Cells in the direction of the plane normal
    are kept, while the cells in the opposite direction are removed.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    plane : Plane
        The plane that defines the clip.
    name : str
        A user provided name for the filter.
    display_attrs (DisplayAttributes)
        Specifies this filters appearance.
    inverted : bool
        Inverts the direction of the clip. If true, cells in the direction of the normal
        are removed. Default: False
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._plane: Plane = Plane()
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id = generate_id("clip-")
        self.name = name
        self.inverted: bool = False

    @property
    def plane(self) -> Plane:
        return self._plane

    @plane.setter
    def plane(self, new_plane: Plane) -> None:
        if not isinstance(new_plane, Plane):
            raise TypeError(f"Expected 'Plane', got {type(new_plane).__name__}")
        self._plane = new_plane

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.clip.plane.origin.CopyFrom(self.plane.origin._to_proto())
        vis_filter.clip.plane.normal.CopyFrom(self.plane.normal._to_proto())
        vis_filter.clip.inverted = self.inverted
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter


class BoxClip(Filter):
    """
    Clip the dataset using a box. Cells inside the box are kept while cells completely outside the
    box are removed.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name : str
        A user provided name for the filter.
    box : Box
        The box definition to clip by.
    display_attrs (DisplayAttributes)
        Specifies this filters appearance.
    inverted: bool
        Inverts the direction of the clip. If true, cells completely inside the box are removed.
        Default : False
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._box: Box = Box()
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id = generate_id("clip-")
        self.name = name
        self.inverted: bool = True

    @property
    def box(self) -> Box:
        return self._box

    @box.setter
    def box(self, new_box: Box) -> None:
        if not isinstance(new_box, Box):
            raise TypeError(f"Expected 'Box', got {type(new_box).__name__}")
        self._box = new_box

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.clip.box.center.CopyFrom(self.box.center._to_proto())
        vis_filter.clip.box.lengths.CopyFrom(self.box.lengths._to_proto())
        # The api interface is in degrees but the backend needs radians
        radians = Vector3(x=self.box.angles.x, y=self.box.angles.y, z=self.box.angles.z)
        radians.x = radians.x * (math.pi / 180)
        radians.y = radians.y * (math.pi / 180)
        radians.z = radians.z * (math.pi / 180)
        vis_filter.clip.box.angles.CopyFrom(radians._to_proto())
        vis_filter.clip.inverted = self.inverted
        set_filter_display_attrs(vis_filter, self.display_attrs)
        print(vis_filter)
        return vis_filter


class VectorGlyphs(Filter):
    """
    VectorGlyphs is the base class for the two vector glyph types.
    The full doc strings are located in the derived classes.
    .. warning:: This feature is experimental and may change or be removed in the future.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id: str = generate_id("vector-")
        self.name: str = name
        # TODO(matt): we should be able to help set some reasonable defaults bases
        # on the mesh size (i.e., number of points) and bounds (the default glyph size).
        # The scene has accesss to this theoretically. Perhaps the scene class can be used
        # as a factory.
        self._sampling_rate: int = 500
        self.field: Field = Field()
        # TODO(matt): we should only allow vectors somehow
        self.field.quantity = VisQuantity.VELOCITY

    @property
    def sampling_rate(self) -> int:
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, rate: int) -> None:
        if not isinstance(rate, int) and not isinstance(rate, float):
            raise TypeError(f"Sampling rate must be a number, got {type(rate).__name__}")
        if rate < 1:
            raise ValueError("Sampling rate must be a integer > 0")
        self._sampling_rate = rate


class FixedSizeVectorGlyphs(VectorGlyphs):
    """
    Vector Glyphs is a vector field visualization techique that places arrows (e.g., glyphs),
    in the 3D scene that are oriented in the direction of the underlying vector field.
    Fixed size vector glyhs places vector annotations at sampled points in
    meshes that are a fixed size. This filter is only valid on vector fields.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name : str
        A user provided name for the filter.
    sampling_rate : int
        Specifies how many vector glyphs to place. A sampling rate of 1 means that a glyph
        will be placed at every point in the input mesh. A sampling rate of 10 means that glyphs
        are paced at every 10th point. The value must be a integer greater than 1. Default: 500.
    size : float
        The size in world units (meters) of the glyphs.
    display_attrs (DisplayAttributes)
        Specifies this filters appearance.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.size: float = 1.0

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.glyph.fixed_size_glyphs = self.size
        vis_filter.glyph.n_glyphs = self.sampling_rate
        vis_filter.glyph.sampling_mode = vis_pb2.GLYPH_SAMPLING_MODE_EVERY_NTH
        vis_filter.glyph.field.quantity_typ = self.field.quantity.value
        vis_filter.glyph.field.component = self.field.component.value
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter


class ScaledVectorGlyphs(VectorGlyphs):
    """
    Vector Glyphs is a vector field visualization techique that places arrows
    (e.g., glyphs), in the 3D scene that are oriented in the direction of the
    underlying vector field.  Scaled vector glyphs changes the size of the
    arrows base on the magnitude of the vector. For example when visualizing the
    velocity field, a glyph where the magnitude is twice the magnitude of
    another glyph will appear twice as large.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name : str
        A user provided name for the filter.
    sampling_rate : int
        Specifies how many vector glyphs to place. A sampling rate of 1 means that a glyph
        will be placed at every point in the input mesh. A sampling rate of 10 means that glyphs
        are paced at every 10th point. The value must be a integer greater than 1. Default: 500.
    scale: float
        The scale applied to the vector glyph. The actual vector glpyh size is the magnitude of the
        vector at the sampled point multiplied by the scale. For example, if the vector magnitude is
        0.5 and the scale is 2 then the resulting world space size is 1 meter. Default: 1.
    display_attrs (DisplayAttributes)
        Specifies this filters appearance.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.scale: float = 1.0

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.glyph.glyph_scale_size = self.scale
        vis_filter.glyph.n_glyphs = self.sampling_rate
        vis_filter.glyph.sampling_mode = vis_pb2.GLYPH_SAMPLING_MODE_EVERY_NTH
        vis_filter.glyph.field.quantity_typ = self.field.quantity.value
        vis_filter.glyph.field.component = self.field.component.value
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter
