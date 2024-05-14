from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, update_session_auth_hash, views as auth_views,
)
from apps.customers.forms import CustomerSignUpForm, CustomerUpdateForm
from apps.customers.decorators import customer_verified

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

@customer_verified
def customerWishlistAndFollowedStore(request):
    ''' customer wishlist and followed store.'''
    return render(request, 'wishlist.html')


# @customer_verified
# def CustomerProfile(request):
#     ''' customer profile '''

#     order = OrderItem.objects.filter(order__customer=request.user.customer)

#     context = {
#         'customer': request.user.customer,
#         'orders': order,
#     }

#     return render(request, 'customer/customer_profile.html', context)

# Create your views here.
@customer_verified
def CustomerProfileUpdate(request):
    ''' Update customer profile '''
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('customer_profile')
    else:
        form = CustomerUpdateForm(instance=request.user.customer)
        context = {
            'form': form,
        }
        return render(request, 'customer/customer_profile_edit.html', context)

def CustomerSignUpView(request):
    ''' Sign up view for new customer account.'''
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = CustomerSignUpForm()
        return render(request, 'customer/sign-up.html', {'form': form})

@customer_verified
def change_password_view(request):
    '''A form for allowing customer to change with old password '''
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Change Successfully!")
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, "customer/password_change.html", {"form": form})


class SignInView(auth_views.LoginView):
    ''' Sign in for customer '''
    form_class = AuthenticationForm
    template_name = 'customer/sign-in.html'