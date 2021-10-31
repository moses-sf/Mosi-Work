from graphene import ObjectType, Schema
import projects.schema
import vendor.schema


class Query(projects.schema.Query, vendor.schema.Query, ObjectType):
    pass


schema = Schema(query=Query)
