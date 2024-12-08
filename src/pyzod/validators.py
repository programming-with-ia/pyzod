class ValidatorBase:
    def validate(self, value):
        raise NotImplementedError


# Specific Validators
class Min(ValidatorBase):
    def __init__(self, min_value):
        self.min_value = min_value

    def validate(self, value):
        if value < self.min_value:
            raise ValueError(f"Value {value} is less than the minimum {self.min_value}")


class Max(ValidatorBase):
    def __init__(self, max_value):
        self.max_value = max_value

    def validate(self, value):
        if value > self.max_value:
            raise ValueError(
                f"Value {value} is greater than the maximum {self.max_value}"
            )


class MinMax(ValidatorBase):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Value {value} must be between {self.min_value} and {self.max_value}"
            )


class Length(ValidatorBase):
    def __init__(self, length):
        self.length = length

    def validate(self, value):
        if len(value) != self.length:
            raise ValueError(f"Length of {value} must be {self.length}")


class MinLength(ValidatorBase):
    def __init__(self, min_length):
        self.min_length = min_length

    def validate(self, value):
        if len(value) < self.min_length:
            raise ValueError(
                f"Length of {value} is less than the minimum {self.min_length}"
            )


class MaxLength(ValidatorBase):
    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self, value):
        if len(value) > self.max_length:
            raise ValueError(f"Length of {value} exceeds the maximum {self.max_length}")


class MinMaxLength(ValidatorBase):
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        if not (self.min_length <= len(value) <= self.max_length):
            raise ValueError(
                f"Length of {value} must be between {self.min_length} and {self.max_length}"
            )
