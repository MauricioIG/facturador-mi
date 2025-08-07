from django.db import models

# Create your models here.


class Cliente(models.Model):
    ruc = models.CharField(max_length=13)
    razon_social = models.CharField(max_length=80, blank=True, null=True)
    nombres = models.CharField(max_length=50, blank=True, null=True)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        if self.razon_social:
            return f"{self.razon_social} - RUC: {self.ruc}"
        else:
            return f"{self.nombres} {self.apellidos} -RUC: {self.ruc}"


class Producto(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    # Usa más decimales si manejas subsidios
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=4)
    stock = models.IntegerField()

    def __str__(self):
        return str(self.nombre)


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    numero_autorizacion = models.CharField(max_length=49)  # Según el ejemplo
    clave_acceso = models.CharField(max_length=49)
    ambiente = models.CharField(max_length=20, choices=[(
        'PRUEBA', 'PRUEBA'), ('PRODUCCIÓN', 'PRODUCCIÓN')])
    emision = models.CharField(max_length=20, default='NORMAL')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura #{self.pk} - Cliente: {self.cliente}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    detalle_adicional = models.CharField(max_length=200, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subsidio = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    precio_sin_subsidio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
