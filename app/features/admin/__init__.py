from fastapi import APIRouter

API = APIRouter()

# /admin/ depends on token
# /admin/login POST -> redis as store backend
# /admin/logout POST -> redis as tore backend
# /admin/<model-name>/ GET -> list of items with pagination
# -> GET /:id -> get item for edit
# -> PATCH /:id -> update item if exists
# -> POST /:id -> create item
# -> DELETE /:id -> delete item
