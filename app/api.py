import sqlalchemy as sa

from fastapi import APIRouter, Depends

from .db import ENGINE

router = APIRouter()


async def get_db():
    async with ENGINE.connect() as conn:
        yield conn


@router.get("/")
async def health(conn=Depends(get_db)):
    result = (await conn.execute(sa.text("SELECT 1;"))).fetchone()
    return {"result": str(result)}
