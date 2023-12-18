from fastapi import APIRouter


router = APIRouter(prefix='/progress_bar', tags=['progress_bar'])


@router.get('/')
async def progress_bar():
    pass