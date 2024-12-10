from dataclasses import _POST_INIT_NAME
from .types import Base as BaseType

POST_INIT_NAME = _POST_INIT_NAME
POST_INIT_FINISHED = "_pyzod_finished"


class PyZodBaseDataclass:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        setattr(
            PyZodBaseDataclass, POST_INIT_NAME, PyZodBaseDataclass.__pyzod_post_init__
        )
        cls.__post_init__ = lambda self, org_post_init=getattr(
            cls, POST_INIT_NAME, None
        ): PyZodBaseDataclass.__post_init__(self, org_post_init)

    def __post_init__(self):
        raise NotImplementedError

    def __pyzod_post_init__(self, org_post_init=None):
        if getattr(self, POST_INIT_FINISHED, False):
            return
        for field_name, field_def in self.__dataclass_fields__.items():

            Type = field_def.default
            value = getattr(self, field_name)

            if not isinstance(Type, BaseType):
                raise f"invalid pyzod type {type(Type)}"

            if value == Type:  #  and isinstance(Type, BaseType)
                if Type._default is not None:
                    value = Type._default
                elif Type._required:
                    raise Exception(
                        f"Field '{field_name}' as type {Type.type} is Required"
                    )
                else:
                    value = None

            setattr(self, field_name, Type.validate(value))

        setattr(self, POST_INIT_FINISHED, True)

        # call original or user defined `__post_init__`
        if callable(org_post_init):
            org_post_init(self)
