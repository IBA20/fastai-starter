from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/frontend-api')


@router.get(
    '/hello',
    summary='Greetings string',
    response_description='json containing "Hello World!"',
    tags=['Hello'],
)
async def hello(current_user: str | None = None):
    """
    Returns Hello string\n
    **current_user**: Current user name
    """
    return {'message': 'Привет из бекенда!'}


@router.post(
    '/users/me',
    summary='Получить учетные данные пользователя',
    tags=['user'],
)
async def show_current_user():
    user_data = {
        'email': 'example@example.com',
        'isActive': True,
        'profileId': '1',
        'registeredAt': '2025-06-15T18:29:56+00:00',
        'updatedAt': '2025-06-15T18:29:56+00:00',
        'username': 'user123',
    }
    return JSONResponse(content=user_data, status_code=200)
