from fastapi import APIRouter

router = APIRouter()

@router.get("/block/", tags=["block"])
def get_block():
    pass