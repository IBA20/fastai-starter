from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr, Field, HttpUrl, PositiveInt, StringConstraints
from pydantic.alias_generators import to_camel

from src.settings import settings

DEFAULT_SITE_EXAMPLE = {
    'id': 1,
    'title': 'Фан клуб Домино',
    'prompt': 'Сайт любителей играть в домино',
    'htmlCodeUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/index.html',
    'htmlCodeDownloadUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}'
    f'/data/index.html?response-content-disposition=attachment',
    'screenshotUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/screenshot.png',
    'createdAt': '2025-06-15T18:29:56+00:00',
    'updatedAt': '2025-06-15T18:29:56+00:00',
}


UserName = Annotated[
    str,
    StringConstraints(max_length=254, strip_whitespace=True),
    Field(
        description='Unique user name',
        examples=['ivan', 'alex123'],
    ),
]


class UserDetailsResponse(BaseModel):
    username: UserName
    email: EmailStr = Field(..., description='User email')
    is_active: bool = Field(..., description='Active user or not')
    profile_id: int = Field(..., gt=0, description='User profile ID')
    registered_at: AwareDatetime = Field(..., description='Time of registration')
    updated_at: AwareDatetime = Field(..., description='Time of last user data change')

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


class CreateSiteRequest(BaseModel):
    title: str | None = None
    prompt: str

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'prompt': 'Сайт любителей играть в домино',
                    'title': 'Фан клуб игры в домино',
                },
            ],
        },
    )


class SiteResponse(BaseModel):
    id: PositiveInt
    title: str
    prompt: str
    html_code_url: HttpUrl | None
    html_code_download_url: HttpUrl | None
    screenshot_url: HttpUrl | None
    created_at: AwareDatetime
    updated_at: AwareDatetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            'examples': [DEFAULT_SITE_EXAMPLE],
        },
    )


class SitesGenerationRequest(BaseModel):
    prompt: str

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'prompt': 'Сайт любителей играть в домино',
                },
            ],
        },
    )


class GeneratedSitesResponse(BaseModel):
    sites: list[SiteResponse]

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'sites': [DEFAULT_SITE_EXAMPLE],
                },
            ],
        },
    )
