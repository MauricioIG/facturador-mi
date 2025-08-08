import datetime


def generar_clave_acceso(fecha_emision, tipo_comprobante, ruc, ambiente, serie, secuencial, codigo_numerico):
    """
    Genera la clave de acceso según el formato del SRI.
    fecha_emision: datetime.date
    tipo_comprobante: '01' (factura), '04' (nota crédito), etc.
    ambiente: '1' pruebas, '2' producción
    serie: '001001' (establecimiento+punto de emisión)
    secuencial: '000000123'
    codigo_numerico: hasta 8 dígitos
    """
    fecha_str = fecha_emision.strftime("%d%m%Y")
    base = f"{fecha_str}{tipo_comprobante}{ruc}{ambiente}{serie}{secuencial}{codigo_numerico}1"
    digito = _calcular_digito_modulo11(base)
    return f"{base}{digito}"


def _calcular_digito_modulo11(numero):
    factores = [2, 3, 4, 5, 6, 7]
    suma = 0
    factor_idx = 0
    for n in reversed(numero):
        suma += int(n) * factores[factor_idx]
        factor_idx = (factor_idx + 1) % len(factores)
    resto = suma % 11
    if resto == 0:
        return 0
    elif resto == 1:
        return 1
    else:
        return 11 - resto
