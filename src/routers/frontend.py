from fastapi import APIRouter

router = APIRouter(prefix='/frontend-api')


@router.get('/hello')
async def hello():
    return {'message': 'Привет из бекенда!'}
