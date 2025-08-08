from lxml import etree
import datetime
from ventas.sri.clave_acceso import generar_clave_acceso


def crear_factura_xml(factura, detalles, salida_path):
    fecha_emision = datetime.date.today()
    clave = generar_clave_acceso(
        fecha_emision,
        "01",  # Factura
        "1790012345001",  # RUC emisor
        "1",   # Ambiente pruebas
        "001001",  # Establecimiento + Punto de Emisión
        str(factura.id).zfill(9),
        "12345678"  # Código numérico
    )

    root = etree.Element("factura", id="comprobante", version="1.1.0")

    # infoTributaria
    info_t = etree.SubElement(root, "infoTributaria")
    etree.SubElement(info_t, "ambiente").text = "1"
    etree.SubElement(info_t, "tipoEmision").text = "1"
    etree.SubElement(info_t, "razonSocial").text = "MI EMPRESA S.A."
    etree.SubElement(info_t, "nombreComercial").text = "MI EMPRESA"
    etree.SubElement(info_t, "ruc").text = "1790012345001"
    etree.SubElement(info_t, "claveAcceso").text = clave
    etree.SubElement(info_t, "codDoc").text = "01"
    etree.SubElement(info_t, "estab").text = "001"
    etree.SubElement(info_t, "ptoEmi").text = "001"
    etree.SubElement(info_t, "secuencial").text = str(factura.id).zfill(9)
    etree.SubElement(info_t, "dirMatriz").text = "Av. Ejemplo y Calle"

    # infoFactura
    info_f = etree.SubElement(root, "infoFactura")
    etree.SubElement(
        info_f, "fechaEmision").text = fecha_emision.strftime("%d/%m/%Y")
    etree.SubElement(info_f, "dirEstablecimiento").text = "Av. Ejemplo y Calle"
    etree.SubElement(info_f, "obligadoContabilidad").text = "SI"
    etree.SubElement(info_f, "tipoIdentificacionComprador").text = "05"
    etree.SubElement(
        info_f, "razonSocialComprador").text = factura.cliente.nombre
    etree.SubElement(
        info_f, "identificacionComprador").text = factura.cliente.cedula
    etree.SubElement(info_f, "totalSinImpuestos").text = str(factura.subtotal)
    etree.SubElement(info_f, "totalDescuento").text = "0.00"

    total_imp = etree.SubElement(info_f, "totalConImpuestos")
    ti = etree.SubElement(total_imp, "totalImpuesto")
    etree.SubElement(ti, "codigo").text = "2"
    etree.SubElement(ti, "codigoPorcentaje").text = "2"
    etree.SubElement(ti, "baseImponible").text = str(factura.subtotal)
    etree.SubElement(ti, "valor").text = str(factura.iva)

    etree.SubElement(info_f, "propina").text = "0.00"
    etree.SubElement(info_f, "importeTotal").text = str(factura.total)
    etree.SubElement(info_f, "moneda").text = "DOLAR"

    # detalles
    detalles_tag = etree.SubElement(root, "detalles")
    for d in detalles:
        det_tag = etree.SubElement(detalles_tag, "detalle")
        etree.SubElement(det_tag, "codigoPrincipal").text = d.producto.codigo
        etree.SubElement(det_tag, "descripcion").text = d.producto.nombre
        etree.SubElement(det_tag, "cantidad").text = str(d.cantidad)
        etree.SubElement(det_tag, "precioUnitario").text = str(
            d.precio_unitario)
        etree.SubElement(det_tag, "descuento").text = "0.00"
        etree.SubElement(
            det_tag, "precioTotalSinImpuesto").text = str(d.subtotal)
        impuestos_tag = etree.SubElement(det_tag, "impuestos")
        imp_tag = etree.SubElement(impuestos_tag, "impuesto")
        etree.SubElement(imp_tag, "codigo").text = "2"
        etree.SubElement(imp_tag, "codigoPorcentaje").text = "2"
        etree.SubElement(imp_tag, "tarifa").text = "12.00"
        etree.SubElement(imp_tag, "baseImponible").text = str(d.subtotal)
        etree.SubElement(imp_tag, "valor").text = str(d.iva)

    tree = etree.ElementTree(root)
    tree.write(salida_path, encoding="UTF-8",
               xml_declaration=True, pretty_print=True)
    return salida_path, clave
