from rest_framework.serializers import ModelSerializer, ValidationError, StringRelatedField, SerializerMethodField, IntegerField
from .models import Cart, Items, Voucher, VoucherItem
from apps.users.models import Subscription
from apps.products.models import Product
from django.http import Http404
from apps.products.discount import discount
from .cart_total import CalculateCart
from .discount_stock import DiscountStock

calulate_cart = CalculateCart()

class CreateVoucherSerializer(ModelSerializer):

    class Meta:

        model = Voucher
        fields = (
            "total_price",
            "quantity_products",
            "withdrawal",
            "direction",
            "num_deparment",
            "user",
            "commune",
            "branch")

    def validate(self, attrs):

        if attrs.get('branch') is None and attrs.get('commune') is None:
            raise ValidationError('Debe especificar al menos la sucursal o la comuna.')

        if attrs.get('branch') is not None and attrs.get('commune') is not None:
            raise ValidationError('Solo debe especificar uno, sucursal o la comuna.')

        if attrs.get('commune') and attrs.get('direction') is None:
            raise ValidationError('Si eligio envio a domicilio, tiene que indicar una direccion')

        return attrs

    def create(self, validated_data):


        id_user = self.validated_data["user"]
        cart = calulate_cart.obtain_cart_user(id_user)

        if cart is None:
            raise ValidationError({"status": "Bad Request", "message": "Este usuario no tiene carrito"})

        if not Items.objects.filter(cart=cart).exists():
            raise ValidationError({"status": "Bad Request","message": "Este carrito esta vacio"})

        discount_stock = DiscountStock() # We instantiate the object DiscountStock
        discount_stock.discount_stock_product(cart.id_cart)

        items = Items.objects.filter(cart=cart)

        value_net = calulate_cart.calculate_net_mount(items)
        iva_price = calulate_cart.calculate_iva_price(cart.id_cart)

        try:
          voucher = Voucher.objects.create(
              **validated_data,
              net_mount = value_net,
              iva_price = iva_price
              )
        except:
            raise ValidationError({"status": "Bad Request", "message":"El pedido no fue creado con exito"})

        for item in items:
            try:
                product = Product.objects.get(id_product = item.product.id_product)

                VoucherItem.objects.create(
                    product = product,
                    voucher = voucher,
                    name_product = product.name_product,
                    price = item.product.price,
                    quantity = item.quantity
                )
            except:
                raise ValidationError({"status": "Bad Request", "message":"El producto no fue encontrado"})

        discount_stock.clean_cart(cart.id_cart)

        calulate_cart.cart_total(cart)

        return voucher

class ListVouchersSerializer(ModelSerializer):

    user = StringRelatedField()
    branch = StringRelatedField()
    commune = StringRelatedField()

    class Meta:

        model = Voucher
        fields = (
            "code_uuid",
            "state",
            "net_mount",
            "iva_price",
            "total_price",
            "quantity_products",
            "condition",
            "withdrawal",
            "direction",
            "num_deparment",
            "user",
            "commune",
            "branch")

class CancelVoucherSerializer(ModelSerializer):

    class Meta:

        model = Voucher
        fields = ("state",)

    def update(self, instance, validated_data):

        instance.state = validated_data.get('state', instance.state)

        instance.save()

        return instance

# Simple product serializer
class SimpleProductSerializer(ModelSerializer):

    class Meta:

        model = Product
        fields = ("id_product", "name_product", "price")

# Cart items serializer
class CartItemsSerializer(ModelSerializer):

    product = SimpleProductSerializer(many=False)
    price = SerializerMethodField(method_name="total")

    class Meta:

        model = Items
        fields = ("product", "quantity", "price")

    # Method to calculate the total price
    def total(self, cartItem: Items):

        if cartItem.product.offer is not None:

            price = discount(cartItem.product.price, cartItem.product.offer.discount)

        else:
            price = cartItem.product.price

        result = cartItem.quantity * price

        cartItem.price = result
        cartItem.save()

        return result

# Cart serializer
class CartSerializer(ModelSerializer):

    items = CartItemsSerializer(many=True, read_only=True)
    total = SerializerMethodField(method_name="main_total")
    total_quantity = SerializerMethodField(method_name="calculate_total_quantity")
    total_products = SerializerMethodField(method_name="calculate_total_products")

    class Meta:

        model = Cart
        fields = ("id_cart", "items", "total", "user", "total_quantity", "total_products")

    def calculate_total_quantity(self, cart: Cart):

        total_quantity = calulate_cart.calculate_total_quality(cart.id_cart)

        return total_quantity

    def calculate_total_products(self, cart: Cart):

        quality_products = calulate_cart.calculate_total_products(cart.id_cart)

        return quality_products

    def main_total(self, cart: Cart):

        items = cart.items.all()
        total = calulate_cart.calculate_total_price(items)

        if get_subscription(cart.user):

            discount_total = total * 0.05

            price_total_discount = total - discount_total

            cart.total = price_total_discount
            cart.save()

            return int(price_total_discount)

        cart.total = total
        cart.save()

        return int(total)

    def create(self, validated_data):

        cart = Cart.objects.create(**validated_data)
        return cart

def get_subscription(id_user):

    try:
        Subscription.objects.get(user = id_user)
    except Subscription.DoesNotExist:
        return False

    return True


# Add Cart serializer
class AddItemCartSerializer(ModelSerializer):

    user = IntegerField()

    class Meta:

        model = Items
        fields = ("product", "quantity", "user")

    def save(self, **kwargs):

        product = self.validated_data["product"]
        quantity = self.validated_data["quantity"]
        id_user = self.validated_data["user"]

        cart = calulate_cart.obtain_cart_user(id_user)

        if cart is None:
            raise ValidationError("Carrito no encontrado")

        id_cart = cart.id_cart

        try:

            cartitem = Items.objects.get(product=product, cart=id_cart)

            quantity_total = cartitem.quantity + quantity

            if cartitem.product.stock >= quantity_total:

                cartitem.quantity += quantity
                cartitem.price = cartitem.quantity * cartitem.product.price

                cartitem.save()

                calulate_cart.cart_total(cart)
                calulate_cart.calculate_total_quality(cart.id_cart)
                calulate_cart.calculate_total_products(cart.id_cart)

                self.instance = cartitem

        except Items.DoesNotExist:

            product2 = Product.objects.get(id_product=int(product.id_product))

            if product2.stock >= quantity:

                newPrice = product2.price * quantity

                self.instance = Items.objects.create(
                    product=product,
                    cart=cart,
                    quantity=quantity,
                    price=newPrice
                    )

                calulate_cart.cart_total(cart)
                calulate_cart.calculate_total_products(cart.id_cart)
                calulate_cart.calculate_total_quality(cart.id_cart)

        return self.instance

# Delete Product Cart
class DeleteProductCart(ModelSerializer):

    class Meta:

        model = Items
        fields = ("id_cart", "product")

# Substract Cart serializer
class SubtractItemCartSerializer(ModelSerializer):

    user = IntegerField()

    class Meta:
        model = Items
        fields = ("product", "user")

    def save(self, **kwargs):
        try:

            product = self.validated_data["product"]
            id_user = self.validated_data["user"]

            cart = calulate_cart.obtain_cart_user(id_user)

            if cart is None:
                raise ValidationError("Carrito no encontrado")

            id_cart = cart.id_cart

        except KeyError:
            raise Http404

        try:
            cartitem = Items.objects.get(product=product, cart=id_cart)
        except Items.DoesNotExist:
            raise ValidationError("Items no encontrado")

        if cartitem.quantity == 1:

            cartitem.delete()

            calulate_cart.cart_total(cartitem.cart)
            calulate_cart.calculate_total_products(cartitem.cart.id_cart)
            calulate_cart.calculate_total_quality(cartitem.cart.id_cart)

            return self.instance

        cartitem.quantity -= 1
        cartitem.price = cartitem.quantity * cartitem.product.price
        cartitem.save()

        calulate_cart.cart_total(cartitem.cart)
        calulate_cart.calculate_total_products(cartitem.cart.id_cart)
        calulate_cart.calculate_total_quality(cartitem.cart.id_cart)

        return self.instance
