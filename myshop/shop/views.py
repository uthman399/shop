from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    object_list = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category)
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'page': page, 'products': products})


from .recommender import Recommender

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products})

def search_product(request):
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Product.objects.filter(name__contains=query_name)
            return render(request, 'shop/product/search_product.html', {"results":results, 'query_name': query_name,})

    return render(request, 'shop/product/search_product.html')