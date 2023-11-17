from apps.products.models import Product
from .models import Items

# Class Discount Stock
class DiscountStock(object):

    model = Items

    # Method Obtain a Object Product
    def get_object(self, id_product:int):

        try:
            product = Product.objects.get(id_product=id_product)
        except Product.DoesNotExist:
            return None

        return product

    # Method of discounting stock of a product
    def discount_stock_product(self, id_cart:int):

        # Query to get the items from the user's cart
        cartitems_user = self.model.objects.filter(cart=id_cart)

        for items in cartitems_user:

            quantity_item = items.quantity
            product_stock = items.product.stock

            new_stock = product_stock - quantity_item

            product = self.get_object(items.product.id_product)

            product.stock = new_stock

            product.save()

    # Method Clean Cart
    def clean_cart(self, id_cart:int):

        self.model.objects.filter(cart=id_cart).delete()
