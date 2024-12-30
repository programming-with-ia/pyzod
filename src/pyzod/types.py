from . import validators as v
from .getters import Getter
import typing as t
from .helpers import ValidateResponse, MessagesTypes, getUniqueObjects, getCN


class CustomDict(dict):

    def setValue(self, key, value):
        # if value is None:
        #     del self[key]
        #     return
        self[key] = value

    def getValue(self, key):
        return self.get(key, None)


class Base:
    def __init__(self):
        self.type = None
        self._required = False
        self._default = None
        self._onError = None
        self.validators: t.List[v.ValidatorBase] = []
        self.messages = CustomDict()

    def required(self, message="Value is required"):
        self._required = True
        self.messages.setValue(MessagesTypes.Required, message)
        return self

    def isRequired(self):
        return self._required

    def getDefault(self):
        return self._default

    def default(self, value):
        if isinstance(value, Getter):
            value = value.get(self)
        if not isinstance(value, self.type):
            raise ValueError(f"Default value must be of type {self.type.__name__}")
        self._default = value
        return self

    def onError(self, value):
        if isinstance(value, Getter):
            value = value.get(self)
        if not isinstance(value, self.type):
            raise ValueError(
                f"Error value must be of type {self.type} \nValue is: {value}"
            )
        self._onError = value
        return self

    def validate(self, value=None):
        try:
            if value is None:
                if self._required:
                    raise ValueError(self.messages.getValue(MessagesTypes.Required))
                return self._default

            if not isinstance(value, self.type):
                raise TypeError(
                    f"Expected type '{self.type}' for value '{value}', but got '{type(value).__name__}'"
                )

            for validator in self.validators:
                validator.validate(value)

            return value

        except (ValueError, TypeError) as e:
            if self._onError is not None:
                return self._onError
            raise e

    def isValid(self, value=None):

        try:
            self.validate(value)
            return ValidateResponse(True, data=value)
        except (ValueError, TypeError) as e:
            return ValidateResponse(False, e, value)

    def add_validator(self, validator):
        self.validators.append(validator)
        return self


class LengthValidators:
    def min(self, min_length):
        self.add_validator(v.MinLength(min_length))
        return self

    def max(self, max_length):
        self.add_validator(v.MaxLength(max_length))
        return self

    def length(self, length):
        self.add_validator(v.Length(length))
        return self


class List(Base, LengthValidators):
    def __init__(self, *schema):
        super().__init__()
        self.type = list
        self.schema: t.Union[t.List["Base"], t.Tuple["Base"], "Base"] = None
        self.setSchema(*schema)

    def validate(self, value=None):
        value = super().validate(value)
        validatedList = []

        try:
            if isinstance(self.schema, list):
                if len(value) != len(self.schema):
                    raise ValueError(
                        f"Expected list of length {len(self.schema)}, got {len(value)}"
                    )
                for item, sub_schema in zip(value, self.schema):
                    valid_item = sub_schema.validate(item)
                    validatedList.append(valid_item)

            if isinstance(self.schema, tuple):
                for item in value:
                    isValid = False
                    for validator in self.schema:
                        try:
                            valid_item = validator.validate(item)
                            isValid = True
                            validatedList.append(valid_item)
                            break
                        except Exception as e:
                            pass

                    if not isValid:
                        raise ValueError(
                            f"value '{item}' in list, is not valid by these validators '{tuple(getCN(validator) for validator in self.schema)}'"
                        )
            else:  # for single type like: self.schema = z.Str()
                for item in value:
                    valid_item = self.schema.validate(item)
                    validatedList.append(valid_item)

            return validatedList

        except ValueError as e:
            if self._onError:
                return self._onError
            raise e

    def str(self):
        self.schema = Str()

    def setSchema(self, *schema):
        if len(schema) == 1:
            schema = schema[0]
        # self.schema = schema
        self.schema = getUniqueObjects(schema)  # [str, int, str] -> [str, int]


class Dict(Base):
    def __init__(self, schema: dict):
        super().__init__()
        self.type = dict
        self.schema = schema

    def validate(self, value=None):

        value = super().validate(value)
        if value is None:
            return

        try:
            validated_data = {}
            for key, field in self.schema.items():
                if key not in value:
                    if field._default is not None:
                        validated_data[key] = field._default
                    elif field._required:
                        raise ValueError(f"Missing required field: {key}")
                else:
                    validated_data[key] = field.validate(value[key])

            return validated_data

        except ValueError as e:
            if self._onError:
                return self._onError
            raise e

    def default(self, value: dict = None):
        if value is None:  # all fields must have ._default
            value = {}
            for key, val in self.schema.items():
                value[key] = val._default

            super().default(value)
            return self

        super().default(value)
        for key, val in value.items():
            if isinstance(val, Getter):
                self._default[key] = val.get(self.schema[key])
        return self


class Str(Base, LengthValidators):
    def __init__(self):
        super().__init__()
        self.type = str


class MinMaxValidators:

    def min(self, min_value):
        self.add_validator(v.Min(min_value))
        return self

    def max(self, max_value):
        self.add_validator(v.Max(max_value))
        return self

    def minmax(self, min_value, max_value):
        self.add_validator(v.MinMax(min_value, max_value))
        return self


class Number(Base, MinMaxValidators):
    def __init__(self):
        super().__init__()
        self.type = (int, float)  # Support for both int and float types


class Int(Number):
    def __init__(self):
        super().__init__()
        self.type = int


class Float(Number):
    def __init__(self):
        super().__init__()
        self.type = float
