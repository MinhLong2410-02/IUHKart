from django.shortcuts import redirect, render
from apps.product.models import Product
from apps.vendor.decorators import vendor_verified
from apps.vendor.forms import ProductForm
from apps.vendor.models import Vendor


@vendor_verified
def create_product_view(request):
    """Add a product to the vendor's product list."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = Vendor.objects.get(user=request.user)
            product.save()
            return redirect('vendor:root_path')
    else:
        form = ProductForm()
    return render(request, 'add_product_form.html', {'form': form})


@vendor_verified
def edit_product_view(request, product_id):
    """Edit a product in the vendor's product list."""
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = Vendor.objects.get(user=request.user)
            product.save()
            return redirect('vendor:root_path')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product_form.html', {'form': form})
