from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HPileTypeMetric(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HP_UNSPECIFIED_METRIC: _ClassVar[HPileTypeMetric]
    E_360x174: _ClassVar[HPileTypeMetric]
    E_360x152: _ClassVar[HPileTypeMetric]
    E_360x132: _ClassVar[HPileTypeMetric]
    E_360x108: _ClassVar[HPileTypeMetric]
    E_310x125: _ClassVar[HPileTypeMetric]
    E_310x110: _ClassVar[HPileTypeMetric]
    E_310x93: _ClassVar[HPileTypeMetric]
    E_310x79: _ClassVar[HPileTypeMetric]
    E_250x85: _ClassVar[HPileTypeMetric]
    E_250x62: _ClassVar[HPileTypeMetric]
    E_200x53: _ClassVar[HPileTypeMetric]

class HPileTypeImperial(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HP_UNSPECIFIED_IMPERIAL: _ClassVar[HPileTypeImperial]
    E_14x117: _ClassVar[HPileTypeImperial]
    E_14x102: _ClassVar[HPileTypeImperial]
    E_14x89: _ClassVar[HPileTypeImperial]
    E_14x73: _ClassVar[HPileTypeImperial]
    E_12x84: _ClassVar[HPileTypeImperial]
    E_12x74: _ClassVar[HPileTypeImperial]
    E_12x63: _ClassVar[HPileTypeImperial]
    E_12x53: _ClassVar[HPileTypeImperial]
    E_10x57: _ClassVar[HPileTypeImperial]
    E_10x42: _ClassVar[HPileTypeImperial]
    E_8x36: _ClassVar[HPileTypeImperial]

class HPilePerimeter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PERIMETER_UNSPECIFIED: _ClassVar[HPilePerimeter]
    E_H_PILE_PERIMETER: _ClassVar[HPilePerimeter]
    E_H_BOX_PERIMETER: _ClassVar[HPilePerimeter]

class HPileArea(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AREA_UNSPECIFIED: _ClassVar[HPileArea]
    E_H_PILE_AREA: _ClassVar[HPileArea]
    E_H_BOX_AREA: _ClassVar[HPileArea]
    E_H_USER_SELECT: _ClassVar[HPileArea]
HP_UNSPECIFIED_METRIC: HPileTypeMetric
E_360x174: HPileTypeMetric
E_360x152: HPileTypeMetric
E_360x132: HPileTypeMetric
E_360x108: HPileTypeMetric
E_310x125: HPileTypeMetric
E_310x110: HPileTypeMetric
E_310x93: HPileTypeMetric
E_310x79: HPileTypeMetric
E_250x85: HPileTypeMetric
E_250x62: HPileTypeMetric
E_200x53: HPileTypeMetric
HP_UNSPECIFIED_IMPERIAL: HPileTypeImperial
E_14x117: HPileTypeImperial
E_14x102: HPileTypeImperial
E_14x89: HPileTypeImperial
E_14x73: HPileTypeImperial
E_12x84: HPileTypeImperial
E_12x74: HPileTypeImperial
E_12x63: HPileTypeImperial
E_12x53: HPileTypeImperial
E_10x57: HPileTypeImperial
E_10x42: HPileTypeImperial
E_8x36: HPileTypeImperial
PERIMETER_UNSPECIFIED: HPilePerimeter
E_H_PILE_PERIMETER: HPilePerimeter
E_H_BOX_PERIMETER: HPilePerimeter
AREA_UNSPECIFIED: HPileArea
E_H_PILE_AREA: HPileArea
E_H_BOX_AREA: HPileArea
E_H_USER_SELECT: HPileArea

class GetHPilePropertiesRequest(_message.Message):
    __slots__ = ("session_id", "model_id", "pile_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PILE_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    model_id: str
    pile_id: str
    def __init__(self, session_id: _Optional[str] = ..., model_id: _Optional[str] = ..., pile_id: _Optional[str] = ...) -> None: ...

class GetHPilePropertiesResponse(_message.Message):
    __slots__ = ("hpile_props",)
    HPILE_PROPS_FIELD_NUMBER: _ClassVar[int]
    hpile_props: HPileProperties
    def __init__(self, hpile_props: _Optional[_Union[HPileProperties, _Mapping]] = ...) -> None: ...

class SetHPilePropertiesRequest(_message.Message):
    __slots__ = ("session_id", "model_id", "pile_id", "hpile_props")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PILE_ID_FIELD_NUMBER: _ClassVar[int]
    HPILE_PROPS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    model_id: str
    pile_id: str
    hpile_props: HPileProperties
    def __init__(self, session_id: _Optional[str] = ..., model_id: _Optional[str] = ..., pile_id: _Optional[str] = ..., hpile_props: _Optional[_Union[HPileProperties, _Mapping]] = ...) -> None: ...

class SetHPilePropertiesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HPileProperties(_message.Message):
    __slots__ = ("H_pile_type_m", "H_pile_type_i", "H_pile_perimeter", "H_pile_area")
    H_PILE_TYPE_M_FIELD_NUMBER: _ClassVar[int]
    H_PILE_TYPE_I_FIELD_NUMBER: _ClassVar[int]
    H_PILE_PERIMETER_FIELD_NUMBER: _ClassVar[int]
    H_PILE_AREA_FIELD_NUMBER: _ClassVar[int]
    H_pile_type_m: HPileTypeMetric
    H_pile_type_i: HPileTypeImperial
    H_pile_perimeter: HPilePerimeter
    H_pile_area: HPileArea
    def __init__(self, H_pile_type_m: _Optional[_Union[HPileTypeMetric, str]] = ..., H_pile_type_i: _Optional[_Union[HPileTypeImperial, str]] = ..., H_pile_perimeter: _Optional[_Union[HPilePerimeter, str]] = ..., H_pile_area: _Optional[_Union[HPileArea, str]] = ...) -> None: ...
