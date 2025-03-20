from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetHPileUserSelectedAreaPropertiesRequest(_message.Message):
    __slots__ = ("session_id", "model_id", "pile_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PILE_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    model_id: str
    pile_id: str
    def __init__(self, session_id: _Optional[str] = ..., model_id: _Optional[str] = ..., pile_id: _Optional[str] = ...) -> None: ...

class GetHPileUserSelectedAreaPropertiesResponse(_message.Message):
    __slots__ = ("hpile_user_selected_area_props",)
    HPILE_USER_SELECTED_AREA_PROPS_FIELD_NUMBER: _ClassVar[int]
    hpile_user_selected_area_props: HPileUserSelectedAreaProperties
    def __init__(self, hpile_user_selected_area_props: _Optional[_Union[HPileUserSelectedAreaProperties, _Mapping]] = ...) -> None: ...

class SetHPileUserSelectedAreaPropertiesRequest(_message.Message):
    __slots__ = ("session_id", "model_id", "pile_id", "hpile_user_selected_area_props")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PILE_ID_FIELD_NUMBER: _ClassVar[int]
    HPILE_USER_SELECTED_AREA_PROPS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    model_id: str
    pile_id: str
    hpile_user_selected_area_props: HPileUserSelectedAreaProperties
    def __init__(self, session_id: _Optional[str] = ..., model_id: _Optional[str] = ..., pile_id: _Optional[str] = ..., hpile_user_selected_area_props: _Optional[_Union[HPileUserSelectedAreaProperties, _Mapping]] = ...) -> None: ...

class SetHPileUserSelectedAreaPropertiesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HPileUserSelectedAreaProperties(_message.Message):
    __slots__ = ("H_pile_area_user_select",)
    H_PILE_AREA_USER_SELECT_FIELD_NUMBER: _ClassVar[int]
    H_pile_area_user_select: float
    def __init__(self, H_pile_area_user_select: _Optional[float] = ...) -> None: ...
