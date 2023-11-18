from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError
from rest_framework import status
from .models import Category, Product, Offer, Store, StoreProduct
from .discount import discount

# List Categories Serializer
class ListCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id_category", "name_category"]

# Create and Update Categories Serializer
class CreateUpdateCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["name_category"]

    def create(self, validated_data):

        category = Category.objects.create(**validated_data)

        return category

    def update(self, instance, validated_data):

        instance.name_category = validated_data.get("name_category", instance.name_category)
        instance.save()

        return instance

class OfferSerializer(ModelSerializer):

    class Meta:

        model = Offer
        fields = ["id_offer", "name_offer", "percentage_discount"]

# List Products Serializer
class ListProductsSerializer(ModelSerializer):

    category = StringRelatedField()
    offer = OfferSerializer(many=False)

    class Meta:

        model = Product
        fields = [
            "id_product",
            "name_product",
            "price",
            "discount_price",
            "stock",
            "image",
            "slug",
            "aviable",
            "created",
            "description",
            "category",
            "offer"]

# Create and Update Products Serializer
class CreateUpdateProductSerializer(ModelSerializer):

    class Meta:

        model = Product
        exclude = ("id_product", "slug", "created", "aviable", "discount_price")

    def create(self, validated_data):

        try:
            offer = validated_data["offer"]

            if offer is not None:
                discount_price = discount(product.price, offer.percentage_discount)
        except KeyError:
            discount_price = 0

        product = Product.objects.create(discount_price=discount_price,**validated_data)

        return product

    def update(self, instance, validated_data):

        try:
            offer = validated_data["offer"]

            if offer is not None:
                discount_price = discount(instance.price, offer.percentage_discount)
                instance.discount_price = discount_price
                instance.offer = validated_data.get("offer", instance.offer)
            else:
                instance.offer = None

        except KeyError:
            instance.offer = None
            discount_price = 0

        instance.name_product = validated_data.get("name_product", instance.name_product)
        instance.price = validated_data.get("price", instance.price)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.aviable = validated_data.get("aviable", instance.aviable)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get("description", instance.description)
        instance.category = validated_data.get("category", instance.category)

        instance.save()

        return instance

# List Offers Serializer
class ListOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = ["id_offer", "name_offer", "state", "start_date", "end_date", "percentage_discount"]

# Create and Update Offer Serializer
class CreateUpdateOfferSerializer(ModelSerializer):

    class Meta:
        model = Offer
        fields = ["name_offer", "end_date", "percentage_discount"]

    def create(self, validated_data):

        offer = Offer.objects.create(**validated_data)

        return offer

    def update(self, instance, validated_data):

        instance.name_offer = validated_data.get("name_offer", instance.name_offer)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.percentage_discount = validated_data.get("percentage_discount", instance.percentage_discount)

        instance.save()

        return instance

# List Store Serializer
class ListStoreSerializer(ModelSerializer):

    class Meta:

        model = Store
        fields = ["id_store","name_store", "direction", "temperature", "capacity", "ocupied_capacity"]

# Create Store Serializer
class CreateStoreSerializer(ModelSerializer):

    class Meta:

        model = Store
        fields = ["name_store", "direction", "temperature", "capacity"]

    def create(self, validated_data):

        store = Store.objects.create(**validated_data)

        return store

# Stock Store Serializer
class StockStoreSerializer(ModelSerializer):

    product = StringRelatedField()
    store = StringRelatedField()

    class Meta:

        model = StoreProduct
        fields = ["quantity", "product", "store"]

# Create Stock Store Serializer
class CreateStockStoreSerializer(ModelSerializer):

    class Meta:

        model = StoreProduct
        fields = ["quantity", "store", "product"]

    def save(self, **kwargs):

        id_store = self.data["store"]
        quantity = self.validated_data["quantity"]
        id_product = self.validated_data["product"]

        store = Store.objects.get(id_store=id_store)

        try:
            product = StoreProduct.objects.get(product=id_product, store=id_store)

            sum_stock = product.quantity + quantity
            product.quantity = sum_stock
            new_stock = quantity + store.ocupied_capacity

            if store.capacity > new_stock:

                store.ocupied_capacity = new_stock

                store.save()
                product.save()

                self.instance = product

                return self.instance

            raise ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)

        except StoreProduct.DoesNotExist:

            new_stock = quantity + store.ocupied_capacity

            if store.capacity > new_stock:

                store.ocupied_capacity = new_stock
                store.save()

                self.instance = StoreProduct.objects.create(**self.validated_data)

                return self.instance

            raise ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)
