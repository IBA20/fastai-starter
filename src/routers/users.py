from fastapi import APIRouter

from src.models import UserDetailsResponse

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    '/me',
    summary='Получить учетные данные пользователя',
    response_description='json containing user data',
    response_model=UserDetailsResponse,
)
async def show_current_user() -> UserDetailsResponse:
    """
    Returns current user data\n
    **no params**
    """
    user_data = {
        'username': 'user123',
        'email': 'example@example.com',
        'isActive': True,
        'profileId': '1',
        'registeredAt': '2025-06-15T18:29:56+03:00',
        'updatedAt': '2025-06-15T18:29:56+03:00',
    }
    user = UserDetailsResponse(**user_data)
    return user
