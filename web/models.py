from django.db import models
from django.template.defaultfilters import slugify
import uuid

stocks = [
    ("in-stock", "In Stock"),
    ("stock-out", "Out of Stock"),
]
specials = [
    ("hot-offer", "Hot Offer"),
    ("featured-product", "Featured Product")
]
catego = [
    ("visible", "Visible"),
    ("hidden", "Hidden")
]

from io import BytesIO
from django.core.files import File
from PIL import Image


def make_thumbnail(image, size=(220, 220)):
    im = Image.open(image)
    im.convert('RGB') # convert mode
    im.thumbnail(size) # resize image
    thumb_io = BytesIO() # create a BytesIO object
    im.save(thumb_io, 'JPEG', quality=85) # save image to BytesIO object
    thumbnail = File(thumb_io, name=image.name) # create a django friendly File object
    return thumbnail


def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=70)
    new_image = File(im_io, name=image.name)
    return new_image

# ------------------


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    status = models.CharField(max_length=255, null=False, blank=False, default=None)
    image = models.ImageField(null=False, blank=False, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Units(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.unit

    class Meta:
        db_table = 'units'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    image = models.ImageField()
    thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbs', editable=False)
    description = models.TextField(null=True, blank=True)
    category_id = models.ForeignKey(Categories, db_column='category_id', on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Units, db_column='unit_id', null=True, blank=True, on_delete=models.CASCADE)
    # quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=catego, null=True, blank=True)
    stock = models.CharField(max_length=100, choices=stocks, null=True, blank=True)
    # old_price = models.IntegerField(null=True, blank=True)
    final_price = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)+'-'+uuid.uuid4().hex[:6]
        self.new_image = compress(self.image)
        self.image = self.new_image
        self.thumbnail = make_thumbnail(self.new_image, size=(220,220))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'products'


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    cart_no = models.CharField(max_length=10)
    product_id = models.ForeignKey(Products, db_column='product_id', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.IntegerField(null=True)

    class Meta:
        db_table = 'cart'


class SpecialProducts(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, db_column='product_id', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=specials)

    class Meta:
        db_table = 'specialproducts'
