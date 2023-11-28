from apps.products.models import Product
from .models import VoucherItem

# Class Discount Stock
class DiscountStock:

    model = VoucherItem

    # Method Obtain a Object Product
    def get_object(self, id_product:int):

        try:
            product = Product.objects.get(id_product=id_product)
        except Product.DoesNotExist:
            return None

        return product

    # Method of discounting stock of a product
    def discount_stock_product(self, voucher):

        # Query to get the items from the user's cart
        items = self.model.objects.filter(voucher=voucher)

        for item in items:

            new_stock = item.product.stock - item.quantity

            product = self.get_object(item.product.id_product)

            product.sold = item.quantity
            product.stock = new_stock

            product.save()
