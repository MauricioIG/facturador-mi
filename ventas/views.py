from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Producto, Factura, DetalleFactura
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal

# Autenticación
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# ========================
#     AUTENTICACIÓN
# ========================


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_productos')
    else:
        form = UserCreationForm()
    return render(request, 'ventas/registro.html', {'form': form})


# ========================
#     VISTAS PROTEGIDAS
# ========================

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/productos.html', {'productos': productos})


@login_required
def crear_factura(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)

        factura = Factura.objects.create(
            cliente=cliente,
            total=Decimal('0.00')
        )

        total = Decimal('0.00')

        for key in request.POST:
            if key.startswith('producto_'):
                producto_id = key.split('_')[1]
                cantidad = Decimal(request.POST.get(key))  # usar Decimal
                producto = get_object_or_404(Producto, pk=producto_id)

                precio_unitario = producto.precio_unitario
                subsidio = Decimal('0.00')  # o un valor calculado si aplica
                precio_sin_subsidio = precio_unitario + subsidio
                # puedes calcularlo si lo estás usando
                descuento = Decimal('0.00')

                precio_total = (precio_unitario * cantidad) - descuento

                DetalleFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subsidio=subsidio,
                    precio_sin_subsidio=precio_sin_subsidio,
                    descuento=descuento,
                    precio_total=precio_total,
                    descripcion=producto.descripcion if hasattr(
                        producto, 'descripcion') else '',
                    detalle_adicional=''  # O llena desde POST si lo usas en el formulario
                )

                total += precio_total

        factura.total = total
        factura.save()

        return redirect('detalle_factura', factura_id=factura.id)

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()

    return render(request, 'ventas/crear_factura.html', {
        'clientes': clientes,
        'productos': productos
    })


@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    return render(request, 'ventas/detalle_factura.html', {'factura': factura})
