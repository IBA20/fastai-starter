from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr, Field, StringConstraints
from pydantic.alias_generators import to_camel
from pydantic.functional_validators import AfterValidator


def strip_whitespace(value: str) -> str:
    return value.strip()


PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=30)]


UserName = Annotated[
    str,
    AfterValidator(strip_whitespace),
    Field(
        max_length=254,
        description='Unique user name',
        examples=['ivan', 'alex123'],
    ),
]


class UserDetailsResponse(BaseModel):
    username: UserName
    email: EmailStr = Field(..., description='User email')
    isActive: bool = Field(..., description='Active user or not')
    profileId: int = Field(..., description='User profile ID')
    registeredAt: AwareDatetime = Field(..., description='Time of registration')
    updatedAt: AwareDatetime = Field(..., description='Time of last user data change')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            'examples': [
                {
                    'username': 'johndoe',
                    'email': 'john.doe@example.com',
                    'isActive': True,
                    'profileId': 12132,
                    'registeredAt': '2025-06-15T18:29:56+00:00',
                    'updatedAt': '2025-06-15T18:29:56+00:00',
                },
            ],
        },
    )
