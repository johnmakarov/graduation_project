from faker.proxy import Faker
from pydantic import BaseModel
# Можно так же такие вещи использовать.
# from pydantic import EmailStr

fake = Faker("ru_RU")


class UserOut(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: str
    phone: str
    birth: str


def created_user() -> UserOut:
    return UserOut(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        middle_name=fake.middle_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        birth=birth.strftime("%d.%m.%Y"),
    )