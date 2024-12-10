from dataclasses import dataclass
import pyzod as z


@dataclass
class User(z.PyZodBaseDataclass):
    id: int = z.Number().required()
    name: str = z.Str().default("No Name")
    email: str = z.Str().required()

    def __post_init__(self):
        print("child post init")
        return super().__post_init__()  # * doesn't matter


# Example usage
try:
    user = User(id=1, name="immi", email="email")
    # user = User(id=1, email="email") #* use Default `name` value
    # user = User(id=1, name="immi") #! `email` is required
    # user = User(id='2', name="immi", email="email") #! invalid Type
    print(user)


except ValueError as e:
    print(e)
