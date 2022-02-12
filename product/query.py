import graphene
from graphene_django import DjangoListField
from .object_types import ProductType




class Query(graphene.ObjectType):
    products = DjangoListField(ProductType)