from django.http import JsonResponse
import graphene
from graphene_django import DjangoListField

from product.models import Product
from .object_types import ProductType




class Query(graphene.ObjectType):
    products = DjangoListField(ProductType)
    product = graphene.Field(ProductType, id=graphene.String(required=True))


    def resolve_product(root, info, id):
        # checks to see if the product exist in the db
        if Product.objects.filter(id=id).exists():

            # fetches the product from the db and return the object
            product = Product.objects.get(id=id)
            return product
        else:
            # returns an error if the product does not exist in the db
            return JsonResponse(
                {
                    "Error": "Product with id does not exist."
                }
            )