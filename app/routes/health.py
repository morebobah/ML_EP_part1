from fastapi import APIRouter, Request

router = APIRouter(tags=['Health page'])

@router.get("/health", summary='Are you ok?')
def home_page():
    return {'message': 'I am OK!'}