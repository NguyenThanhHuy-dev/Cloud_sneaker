import random
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Import Models & Forms
from accounts.models import Cart, CartItem
from products.models import Product, SizeVariant, ProductReview, Wishlist
from .forms import ReviewForm

# ==========================
# 1. PRODUCT DETAILS VIEW
# ==========================
def get_product(request, slug):
    # Lấy sản phẩm, nếu không có thì báo lỗi 404
    product = get_object_or_404(Product, slug=slug)

    # 1. Sắp xếp Size theo thứ tự logic (Dùng trường 'order' thay vì tên)
    sorted_size_variants = product.size_variant.all().order_by('order')

    # 2. Lấy sản phẩm liên quan (Cùng danh mục, trừ chính nó)
    related_products = list(
        Product.objects.filter(category=product.category)
        .exclude(uid=product.uid)
    )
    # Random lấy 4 sản phẩm
    if len(related_products) >= 4:
        related_products = random.sample(related_products, 4)

    # 3. Xử lý Review Form (Thêm/Sửa review)
    review_form = ReviewForm()
    user_review = None
    
    if request.user.is_authenticated:
        # Kiểm tra xem user đã review chưa
        user_review = ProductReview.objects.filter(product=product, user=request.user).first()

        if request.method == 'POST':
            # Nếu đã có review thì update, chưa thì tạo mới
            if user_review:
                review_form = ReviewForm(request.POST, instance=user_review)
            else:
                review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.product = product
                new_review.user = request.user
                new_review.save()
                messages.success(request, "Review submitted successfully!")
                return redirect('get_product', slug=slug)

    # 4. Tính toán Rating để hiển thị thanh phần trăm
    rating_percentage = 0
    if product.get_rating():
        rating_percentage = (product.get_rating() / 5) * 100

    # 5. Kiểm tra Wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    # 6. Context cơ bản
    context = {
        'product': product,
        'sorted_size_variants': sorted_size_variants,
        'related_products': related_products,
        'review_form': review_form,
        'rating_percentage': rating_percentage,
        'in_wishlist': in_wishlist,
    }

    # 7. Logic cập nhật giá khi chọn Size (Query Param ?size=...)
    if request.GET.get('size'):
        size_name = request.GET.get('size')
        # Tìm size object để lấy giá chính xác
        size_obj = SizeVariant.objects.filter(size_name=size_name).first()
        if size_obj:
            price = product.get_product_price_by_size(size_name)
            context['selected_size'] = size_name
            context['updated_price'] = price

    return render(request, 'product/product.html', context=context)


# ==========================
# 2. REVIEW MANAGEMENT VIEWS
# ==========================

@login_required
def product_reviews(request):
    """Hiển thị tất cả review của user hiện tại"""
    reviews = ProductReview.objects.filter(
        user=request.user).select_related('product').order_by('-date_added')
    return render(request, 'product/all_product_reviews.html', {'reviews': reviews})


@login_required
def edit_review(request, review_uid):
    """Chỉnh sửa review (Dùng cho Modal AJAX hoặc Form thường)"""
    review = get_object_or_404(ProductReview, uid=review_uid, user=request.user)
    
    if request.method == "POST":
        stars = request.POST.get("stars")
        content = request.POST.get("content")
        
        if stars and content:
            review.stars = stars
            review.content = content
            review.save()
            messages.success(request, "Your review has been updated.")
        else:
            messages.error(request, "Please fill in all fields.")
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return JsonResponse({"detail": "Method not allowed"}, status=405)


@login_required
def delete_review(request, slug, review_uid):
    """Xóa review"""
    review = get_object_or_404(ProductReview, uid=review_uid, user=request.user)
    review.delete()
    messages.success(request, "Your review has been deleted.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def like_review(request, review_uid):
    """AJAX Like Review"""
    review = get_object_or_404(ProductReview, uid=review_uid)

    if request.user in review.likes.all():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
        review.dislikes.remove(request.user) # Bỏ dislike nếu like
        
    return JsonResponse({'likes': review.like_count(), 'dislikes': review.dislike_count()})


@login_required
def dislike_review(request, review_uid):
    """AJAX Dislike Review"""
    review = get_object_or_404(ProductReview, uid=review_uid)

    if request.user in review.dislikes.all():
        review.dislikes.remove(request.user)
    else:
        review.dislikes.add(request.user)
        review.likes.remove(request.user) # Bỏ like nếu dislike
        
    return JsonResponse({'likes': review.like_count(), 'dislikes': review.dislike_count()})


# ==========================
# 3. WISHLIST VIEWS
# ==========================

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product', 'size_variant')
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, uid):
    variant = request.GET.get('size')
    if not variant:
        messages.warning(request, 'Please select a size before adding to wishlist!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    product = get_object_or_404(Product, uid=uid)
    size_variant = get_object_or_404(SizeVariant, size_name=variant)
    
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user, 
        product=product, 
        size_variant=size_variant
    )

    if created:
        messages.success(request, "Added to Wishlist!")
    else:
        messages.info(request, "Item already in Wishlist.")

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, uid):
    # Logic xóa: Xóa theo UID sản phẩm và Size (nếu có)
    product = get_object_or_404(Product, uid=uid)
    size_variant_name = request.GET.get('size')

    if size_variant_name:
        Wishlist.objects.filter(
            user=request.user, 
            product=product, 
            size_variant__size_name=size_variant_name
        ).delete()
    else:
        # Fallback: Xóa tất cả size của sản phẩm này trong wishlist
        Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.success(request, "Removed from wishlist!")
    return redirect('wishlist')


@login_required
def move_to_cart(request, uid):
    # Chuyển từ Wishlist sang Cart
    product = get_object_or_404(Product, uid=uid)
    
    # Tìm item trong wishlist (Lấy item đầu tiên khớp product)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if not wishlist_item:
        messages.error(request, "Item not found in wishlist.")
        return redirect('wishlist')

    size_variant = wishlist_item.size_variant
    
    # 1. Xóa khỏi wishlist
    wishlist_item.delete()

    # 2. Thêm vào giỏ hàng
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product, 
        size_variant=size_variant
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Moved to cart successfully!")
    return redirect('cart')