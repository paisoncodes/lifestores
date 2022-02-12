from django.http import JsonResponse
from django.views import View
import graphene
from product.models import Product

from product.object_types import ProductInput, ProductType
from mock_data import mock_data





# A mutation class to add products in units to the db
class ProductMutation(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        sku = graphene.String(required=True)
        price = graphene.Int(required=True)
        image = graphene.String(required=True)
    
    @staticmethod
    def mutate(info, name, description, sku, price, image):
        try:
            product = Product.objects.create(
                name = name,
                description = description,
                sku = sku,
                price = price,
                image = image
            )
            
            return ProductMutation(
                status = True,
                message = "Product created",
                product = product
            )

        except Exception as e:
            return ProductMutation(
                status = False,
                message = e
            )

# a mutation to add products in bulk to the db by sending a list of objects
class BulkProductMutation(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        product_list = graphene.List(ProductInput, required=True)
    
    @staticmethod
    def mutate(self, info, product_list: list):
        try:
            for object in product_list:
                Product.objects.create(
                    name = object["name"],
                    description = object["description"],
                    sku = object["sku"],
                    price = object["price"],
                    image = object["image"]
                )
            
            return BulkProductMutation(
                status = True,
                message = "Products created"
            )

        except Exception as e:
            return ProductMutation(
                status = False,
                message = e
            )

# this function loops through a list of dictionary objects(this will be provided manually) and adds each product that has its data provided to the db.
def migrate_products(data: list) -> dict:
    for object in data:
        try:
            Product.objects.create(
                name = object["name"],
                description = object["description"],
                sku = object["sku"],
                price = object["price"],
                image = object["image"]
            )
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }
    return {
        "status": True,
        "message": "Product(s) migrated"
    }

# this is an exposed get REST endpoint that adds the products that are in the mock data to the db when accessed.
class MigrateProducts(View):
    def get(self, request):
        for object in mock_data:
            Product.objects.create(
                name = object["name"],
                description = object["description"],
                sku = object["sku"],
                price = object["price"],
                image = object["image"]
            )
        return JsonResponse(
            {
                "status": True,
                "message": "Product(s) migrated"
            }
        )

class Mutation(graphene.ObjectType):
    add_product = ProductMutation.Field()
    bulk_add_product = BulkProductMutation.Field()