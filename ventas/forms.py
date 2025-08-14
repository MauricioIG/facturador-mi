from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Producto, Factura, DetalleFactura


# 🔹 Formulario de Registro de Usuario sin confirmación de contraseña
class RegistroForm(forms.ModelForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# 🔹 Formulario de Login Personalizado
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Clave de acceso",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# 🔹 Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['ruc', 'razon_social', 'direccion']
        widgets = {
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if len(ruc) != 13 or not ruc.isdigit():
            raise forms.ValidationError(
                "El RUC debe tener 13 dígitos numéricos.")
        return ruc


# 🔹 Formulario para Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio_unitario', 'stock']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# 🔹 Formulario para Factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'cliente', 'numero_autorizacion', 'clave_acceso',
            'ambiente', 'emision', 'total'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'numero_autorizacion': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_acceso': forms.TextInput(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'emision': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# 🔹 Formulario para Detalle de Factura
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = [
            'producto', 'cantidad', 'descripcion', 'detalle_adicional',
            'precio_unitario', 'subsidio', 'precio_sin_subsidio',
            'descuento', 'precio_total'
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'detalle_adicional': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'subsidio': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_sin_subsidio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
