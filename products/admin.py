from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'image_preview']

    def image_preview(self, obj):
        # Kiểm tra nếu có ảnh thì hiện, không thì báo No Image
        if obj.category_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.category_image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1
    # Hiển thị ảnh xem trước trong trang sửa sản phẩm
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        # Sửa lỗi ở đây: Dùng obj.image thay vì obj.image_url
        if obj.image:
            return format_html('<img src="{}" width="200" style="object-fit: contain;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category']
    inlines = [ProductImageAdmin]


class ProductImageStandaloneAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_thumbnail']
    
    # img_preview là hàm bạn đã viết sẵn trong models.py
    readonly_fields = ['img_preview']

    def image_thumbnail(self, obj):
        # Sửa lỗi ở đây: Dùng obj.image thay vì obj.image_url
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Thumbnail'


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price', 'order']
    model = SizeVariant


admin.site.register(Category, CategoryAdmin)
admin.site.register(Coupon)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageStandaloneAdmin)
admin.site.register(ProductReview)