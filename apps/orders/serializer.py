from rest_framework.serializers import StringRelatedField, ModelSerializer, ValidationError
from rest_framework import status
from .models import DispatchGuide, GuieProduct, Bill
from core.messages import validator_errors_message

class ListDispatchGuideSerializer(ModelSerializer):

    grocer = StringRelatedField()

    class Meta:

        model = DispatchGuide
        fields = (
            "code_uuid",
            "dispatch_date",
            "deliver_date",
            "created",
            "state",
            "destination",
            "grocer")

class ProductDispatchGuideSerializer(ModelSerializer):

    class Meta:
        model = GuieProduct
        fields = ("product", "quantity")

class CreateDispatchGuieSerializer(ModelSerializer):

    products = ProductDispatchGuideSerializer(many=True, required=False)

    class Meta:

        model = DispatchGuide
        fields = ("destination", "grocer", "products")

    def validate(self, attrs):

        products = attrs.get("products")

        if products is None:
            raise ValidationError(
                validator_errors_message("Tiene que haber un campo products"),
                status.HTTP_400_BAD_REQUEST)

        if products == []:

            raise ValidationError(
                validator_errors_message("La lista no puede quedar vacia"),
                status.HTTP_400_BAD_REQUEST)

        for product in products:

            if product["quantity"] <= 0:
                raise ValidationError(
                    validator_errors_message("La cantidad no puede ser menor ni igual a cero"),
                    status.HTTP_400_BAD_REQUEST)

        return attrs

    def create(self, validated_data):

        office_guie = DispatchGuide.objects.create(
            destination = validated_data["destination"],
            grocer = validated_data["grocer"]
        )

        for product in validated_data["products"]:

            GuieProduct.objects.create(
                office_guie = office_guie,
                quantity = product["quantity"],
                product = product["product"]
            )

        return office_guie

class UpdateDispatchGuideSerializer(ModelSerializer):

    class Meta:

        model = DispatchGuide
        fields = ("dispatch_date", "deliver_date", "state")

    def update(self, instance, validated_data):

        instance.dispatch_date = validated_data.get("dispatch_date", instance.dispatch_date)
        instance.deliver_date = validated_data.get("deliver_date", instance.deliver_date)
        instance.state = validated_data.get("state", instance.state)

        instance.save()

        return instance

class ListBillSerializer(ModelSerializer):

    supplier = StringRelatedField()
    grocer = StringRelatedField()

    class Meta:

        model = Bill
        fields = (
            "code_uuid",
            "created",
            "active",
            "total_price",
            "products",
            "total_quantity",
            "supplier",
            "grocer")

class CreateBillSerializer(ModelSerializer):

    class Meta:

        model = Bill
        fields = ("products", "supplier", "grocer")

    def validate(self, attrs):

        products = attrs.get("products")

        if type(products) != dict:
            raise ValidationError(
                validator_errors_message("El formato tiene que ser json"),
                status.HTTP_400_BAD_REQUEST)

        if products == {}:
            raise ValidationError(
                validator_errors_message("El json no puede quedar vacio"),
                status.HTTP_400_BAD_REQUEST)

        try:

            if type(products["products"]) != list:
                raise ValidationError(
                    validator_errors_message("Products tiene que ser una lista"),
                    status.HTTP_400_BAD_REQUEST)

            if products["products"] == []:
                raise ValidationError(
                    validator_errors_message("La lista no puede quedar vacia"),
                    status.HTTP_400_BAD_REQUEST)

            for product in products["products"]:

                try:

                    name_product = product["name_product"]
                    price = product["price"]
                    quantity = product["quantity"]

                    if type(name_product) != str or type(price) != int or type(quantity) != int:
                        raise ValidationError(
                            validator_errors_message("El nombre tiene que ser string y el precio y la cantidad tiene que ser numerica"),
                            status.HTTP_400_BAD_REQUEST)

                    if name_product == "":
                        raise ValidationError(
                            validator_errors_message("El nombre no puede quedar vacio"),
                            status.HTTP_400_BAD_REQUEST)

                    if price < 1000:
                        raise ValidationError(
                            validator_errors_message("El precio tiene que ser mayor o igual a 1000"),
                            status.HTTP_400_BAD_REQUEST)

                    if quantity == 0:
                        raise ValidationError(
                            validator_errors_message("La cantidad tiene que ser mayo a 0"),
                            status.HTTP_400_BAD_REQUEST)

                except KeyError:
                    raise ValidationError(
                        validator_errors_message("Los productos deben tener nombre, precio y cantidad"),
                        status.HTTP_400_BAD_REQUEST)

        except KeyError:
            raise ValidationError(
                validator_errors_message("Tiene que haber un campo products"),
                status.HTTP_400_BAD_REQUEST)

        return attrs

    def create(self, validated_data):

        products = validated_data["products"]

        total_quantity = 0
        total_price = 0

        for product in products["products"]:

            total_quantity += product["quantity"]
            total_price += product["price"]

        bill = Bill.objects.create(
            total_quantity=total_quantity,
            total_price=total_price,
            **validated_data
            )

        return bill
