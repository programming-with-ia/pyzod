from .validators import *
from .getters import Getter


class Base:
    def __init__(self):
        self.type = None
        self._required = False
        self._default = None
        self._onError = None
        self.validators = []

    def required(self):
        self._required = True
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
                    raise ValueError("Value is required")
                return self._default

            if not isinstance(value, self.type):
                raise TypeError(
                    f"Expected type {self.type}, got {type(value).__name__}"
                )

            for validator in self.validators:
                validator.validate(value)

            return value

        except (ValueError, TypeError) as e:
            if self._onError:
                return self._onError
            raise e

    def add_validator(self, validator):
        self.validators.append(validator)
        return self


class List(Base):
    def __init__(self, schema):
        super().__init__()
        self.type = list
        self.schema = schema

    def validate(self, value=None):
        value = super().validate(value)

        try:
            if isinstance(self.schema, list):
                if len(value) != len(self.schema):
                    raise ValueError(
                        f"Expected list of length {len(self.schema)}, got {len(value)}"
                    )
                for item, sub_schema in zip(value, self.schema):
                    sub_schema.validate(item)
            else:
                for item in value:
                    self.schema.validate(item)

            return value

        except ValueError as e:
            if self._onError:
                return self._onError
            raise e


class Dict(Base):
    def __init__(self, schema: dict):
        super().__init__()
        self.type = dict
        self.schema = schema

    def validate(self, value=None):
        try:
            value = super().validate(value)
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


class Str(Base):
    def __init__(self):
        super().__init__()
        self.type = str

    def min(self, min_length):
        self.add_validator(MinLength(min_length))
        return self

    def max(self, max_length):
        self.add_validator(MaxLength(max_length))
        return self

    def length(self, length):
        self.add_validator(Length(length))
        return self


class Number(Base):
    def __init__(self):
        super().__init__()
        self.type = (int, float)  # Support for both int and float types

    def min(self, min_value):
        self.add_validator(Min(min_value))
        return self

    def max(self, max_value):
        self.add_validator(Max(max_value))
        return self

    def minmax(self, min_value, max_value):
        self.add_validator(MinMax(min_value, max_value))
        return self


class Int(Number):
    def __init__(self):
        super().__init__()
        self.type = int  # Restrict to integers only


class Float(Number):
    def __init__(self):
        super().__init__()
        self.type = float  # Restrict to floats only
