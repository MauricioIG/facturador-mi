from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('factura/nueva/', views.crear_factura, name='crear_factura'),
    path('factura/<int:factura_id>/',
         views.detalle_factura, name='detalle_factura'),

    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='ventas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
