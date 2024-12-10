import test_init

import pyzod as z

schema = z.Dict(
    {
        "name": z.Str().required().min(2),
        "age": z.Int().required().minmax(18, 40),
        "password": z.Str().required().min(8),
        "id": z.Str().required().length(10),
        "learn": z.List(z.Dict({"a": z.Str().required(), "b": z.Int().required()})),
        "fixedList": z.List([z.Str(), z.Str(), z.Str()]),
        "fullName": z.Str().default(
            "this is fullName"
        ),  # use default value when fullName is not provide
    }
)

data = {
    "name": "Jhon",
    "age": 18,
    "password": "amcoamcoamcoma",
    "id": "1234567890",
    "learn": [{"a": "", "b": 1}],
    "fixedList": [
        "item1",
        "item2",
        "name",
    ],
}

validated_data = schema.validate(data)
print(
    "Validated data:", validated_data
)  # fix: fullName is not exist make it to use default

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# ----------------------------------- test 2 ----------------------------------------
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

schema = z.Dict(
    {
        "name": z.Str().required().min(2),
        "age": z.Int().required().minmax(18, 40),
        "password": z.Str().required().min(8),
        "id": z.Str().required().length(10),
        "learn": z.List(z.Str()),
        "fixedList": z.List(z.List([z.Str(), z.Str()])),
        "fullName": z.Str().default(
            "this is fullName"
        ),  # use default value when fullName is not provide
    }
)

data = {
    "name": "Jhon",
    "age": 18,
    "password": "amcoamcoamcoma",
    "id": "1234567890",
    "learn": ["name"],
    "fixedList": [["item1", "item2"], ["item1", "item2"]],
}

validated_data = schema.validate(data)
print(
    "Validated data:", validated_data
)  # fix: fullName is not exist make it to use default
