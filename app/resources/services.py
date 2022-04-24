import sqlalchemy as sa


class ModelCursorService:
    """Provides simple interface for excecuting raw query in db with
    output data wrapped into models row -> model or list[model]."""

    def __init__(self, connection, model):
        self.connection = connection
        self.model = model
        self.commit = connection.commit
        self.rollback = connection.rollback

    async def execute(self, query):
        try:
            return await self.connection.execute(query)
        except:  # noqa
            await self.rollback()
            raise

    async def one(self, query):
        result = (await self.execute(query)).fetchone()
        if result:
            return self.model.validate(result)

    async def many(self, query):
        result = (await self.execute(query)).fetchall()
        return (self.model.validate(item) for item in result)


class ModelQueryService:
    """Using model and linked table, provides general fetching methods:
    all, get, create, update, delete. Always accepting and returning model
    objects.
    """

    def __init__(self, connection, table: sa.Table, model):
        self.cursor = ModelCursorService(connection, model)
        self.table = table
        self.commit = self.cursor.commit
        self.rollback = self.cursor.rollback

    async def all(self):
        return await self.cursor.many(self.table.select())

    async def get(self, id_or_query):
        if isinstance(id_or_query, (int, str)):
            query = self.table.c.id == id_or_query
        else:
            query = id_or_query
        return await self.cursor.one(self.table.select(query))

    async def filter(
        self,
        query,
        limit: int = None,
        offset: int = None,
        first: bool = False,
        order_by: list = None,
    ):
        query = self.table.select(query)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if order_by is not None:
            query = query.order_by(order_by)
        return (
            await self.cursor.one(query)
            if first
            else await self.cursor.many(query)
        )

    async def create(self, model, exclude: tuple = ("id",)):
        return await self.cursor.one(
            self.table.insert()
            .values(model.dict(exclude=set(exclude)))
            .returning(self.table)
        )

    async def update(self, model, exclude: tuple = ("id",), query=None):
        query = query or (self.table.c.id == model.id)
        return await self.cursor.one(
            self.table.update(query)
            .values(model.dict(exclude=set(exclude)))
            .returning(self.table)
        )

    async def delete(self, id_: int = None, query=None):
        query = query or (self.table.c.id == id_)
        await self.cursor.one(self.table.delete(query))
