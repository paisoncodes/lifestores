import graphene
from graphene_django import DjangoObjectType

from .models import Product



class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    sku = graphene.String(required=True)
    price = graphene.Int(required=True)
    image = graphene.String(required=True)
