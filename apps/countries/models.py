from django.db import models

# Region Model
class Region(models.Model):

    id_region = models.BigAutoField(primary_key=True)
    name_region = models.CharField(max_length=255, unique=True)
    initials = models.CharField(max_length=8, unique=True)

    class Meta:

        db_table = "region"
        verbose_name = "region"
        verbose_name_plural = "regions"

    def __str__(self) -> str:
        return self.name_region

# Province Model
class Province(models.Model):

    id_province = models.BigAutoField(primary_key=True)
    name_province = models.CharField(max_length=60, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:

        db_table = "province"
        verbose_name = "province"
        verbose_name_plural = "provinces"

    def __str__(self) -> str:
        return self.name_province

# Commune Model
class Commune(models.Model):

    id_commune = models.BigAutoField(primary_key=True)
    name_commune = models.CharField(max_length=60, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:

        db_table = "commune"
        verbose_name = "commune"
        verbose_name_plural = "communes"

    def __str__(self) -> str:
        return self.name_commune
