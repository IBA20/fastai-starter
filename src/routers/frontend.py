from fastapi import APIRouter

router = APIRouter(prefix='/frontend-api')


@router.get(
    '/hello',
    summary='Поиск пользователей по имени',
    response_description='Список найденных пользователей',
    tags=['Hello'],
)
async def hello():
    return {'message': 'Привет из бекенда!'}
