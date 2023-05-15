from datetime import date
from pydantic import BaseModel, validator
import json
from typing import Type, TypeVar
from util.string import option, str_check

T = TypeVar('T')


class User(BaseModel):
    id: T
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    location: json
    gender: str
    relationship_status: str
    interested_in: str
    hobbies: list[str]
    friends: list[T]
    published_at: date

    @validator('gender')
    def validate(self: Type['User'], gender: str) -> 'User':
        str_check(gender)

        return option(gender, {'male', 'female'})

    @validator('interested_in')
    def validate(self: Type['User'], interested_in: str) -> 'User':
        str_check(interested_in)

        return option(interested_in, {'single', 'in_a_relationship'})