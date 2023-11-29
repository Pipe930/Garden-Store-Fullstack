from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError
from .models import Branch, ProductBranch
from apps.products.models import Product

# List Branch Serializer
class ListBranchSerializer(ModelSerializer):

    commune = StringRelatedField()

    class Meta:

        model = Branch
        fields = ("id_branch", "name_branch", "direction", "capacity", "phone", "business_name", "commune")

# Create and Update Serializer
class CreateUpdateSerializer(ModelSerializer):

    class Meta:

        model = Branch
        fields = ("name_branch", "direction", "capacity", "phone", "business_name", "commune")

class ListProductBranchSerializer(ModelSerializer):

    class Meta:

        model = ProductBranch
        fields = ("quantity", "product", "branch")

# Create Product Branch Serializer
class CreateProductBranchSerializer(ModelSerializer):

    class Meta:

        model = ProductBranch
        fields = ("quantity", "product", "branch")

    def save(self, **kwargs):

        branch_id = self.data["branch"]
        quantity = self.validated_data["quantity"]
        product = self.validated_data["product"]

        branch = Branch.objects.get(id_branch=branch_id)
        product = Product.objects.get(id_product= product.id_product)

        try:
            branch_product = ProductBranch.objects.get(product=product, branch=branch)

            new_stock = branch_product.quantity + quantity

            if branch.capacity > new_stock:

                branch.capacity_ocuped += quantity
                branch_product.quantity = new_stock
                product.stock += quantity

                branch.save()
                product.save()
                branch_product.save()

                self.instance = branch_product

                return self.instance

            raise ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"})

        except ProductBranch.DoesNotExist:

            new_stock = quantity + branch.capacity_ocuped

            if branch.capacity > new_stock:

                branch.capacity_ocuped = new_stock
                product.stock += quantity

                if not product.aviable:
                   product.aviable = True

                branch.save()
                product.save()

                self.instance = ProductBranch.objects.create(**self.validated_data)

                return self.instance

            raise ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"})
