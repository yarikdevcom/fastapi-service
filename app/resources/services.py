# import inspect


# import inspect
# class SomeClass:
#     boom = 1


# @inject_with_connection
# async def some_func(blah_service, connection):
#     service = blah_service(connection)
#     return service.all_shit()

#     async with engine.connection() as connection:
#         service = blah_service(connection)
#         result = service.all_shit()

#     return result

# def inject_connection(func):
#     inject_kwargs = {}
#     for kwarg, type_ in func.__annotations__.items():
#         if isinstance(type_, SomeClass):
#             inject_kwargs[kwarg] =
#     print(func.__annotations__)
#     # inspect.spec(func)
#     return func


# @inject_connection
# def somefunc(asd: SomeClass):
#     print(asd.boom)


# class SimpleCRUDService:
#     def __init__(self, cursor: ConnectionService, table):
#         self.cursor = cursor
#         self.table = table

#     def get(self, id_):
#         return self.cursor.one(self.table.select(self.table.c.id == id_))

#     def filter(self):
#         pass

#     def create():
#         pass

#     def update():
#         pass

#     def delete():
#         pass
