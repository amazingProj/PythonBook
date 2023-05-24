from datetime import datetime
from pydantic import BaseModel, validator, Field
from typing import TypeVar, List, Dict, Any
from util.string import option, str_check

T = TypeVar('T')


class User(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    location: Dict[str, Any]
    gender: str
    relationship_status: str
    interested_in: str
    hobbies: List[str]
    friends: List[T] = Field(default=[])
    published_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('gender', 'interested_in')
    def validate_gender(cls, gender: str) -> str:
        str_check(gender)
        return option(gender, {'male', 'female'})

    @validator('relationship_status')
    def validate_relationship_status(cls, interested_in: str) -> str:
        str_check(interested_in)
        return option(interested_in, {'single', 'in_a_relationship'})
