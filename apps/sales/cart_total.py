from .models import Cart
from django.conf import settings

# Method calculate cart total

class CalculateCart:

    model = Cart
    iva_porcentage = settings.IVA_PORCENTAGE

    def cart_total(self, id_cart):

        cart = self.model.objects.get(id_cart=int(id_cart.id_cart))

        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])

        cart.total = total
        cart.save()

    # Method calculate total price
    def calculate_total_price(self, items) -> int:

        total_price = 0

        for item in items:

            if item.product.offer is not None:

                discount = item.product.offer.discount
                price_product = item.product.price

                discount_decimal = discount / 100
                price_discount = price_product * discount_decimal

                price = price_product - price_discount

            else:

                price = item.product.price

            total_price += item.quantity * price

        return total_price

    def calculate_total_quality(self, id_cart):

        cart = self.model.objects.get(id_cart=id_cart)

        items = cart.items.all()

        total_quantity = 0

        for item in items:
            total_quantity += item.quantity

        cart.total_quantity = total_quantity
        cart.save()

        return total_quantity

    def calculate_total_products(self, id_cart):

        cart = self.model.objects.get(id_cart=id_cart)

        items = cart.items.all()

        quality_products = 0
        for item in items:
            quality_products += 1

        cart.total_products = quality_products
        cart.save()

        return quality_products


    def calculate_net_mount(self, items) -> int:

        total_price = self.calculate_total_price(items)
        porcentage_iva = self.iva_porcentage / 100
        net_mount = total_price - total_price * porcentage_iva

        return net_mount

    def calculate_iva_price(self, id_cart):

        cart = self.model.objects.get(id_cart=id_cart)
        items = cart.items.all()
        net_mount = self.calculate_net_mount(items)
        iva_prive = cart.total - net_mount

        return iva_prive
