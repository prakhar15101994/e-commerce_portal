from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views 
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    
    path('',views.ProductView.as_view(), name='home'),
    path('productdetail/<int:pk>/',views.ProductdetailView.as_view(), name='productdetail'),
    path('mobile/',views.mobileView, name='mobile'),
    path('mobile/<slug:data>/',views.mobileView, name='mobiledata'),
    path('topwear/',views.TopWearView, name='topwear'),
    path('topwear/<slug:data>/',views.TopWearView, name='topweardata'),
    path('bottomwear/',views.BottomWearView, name='bottomwear'),
    path('bottomwear/<slug:data>/',views.BottomWearView, name='bottomweardata'),


    path('registration/', views.CustomerRegisterView.as_view(), name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='loginpage.html', authentication_form=LoginForm), name='login'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/',views.address, name='address'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirmation.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/',views.checkout_view, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.order_done, name='orders'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removescart')
]
