from zeep import Client
from zeep.transports import Transport
from requests import Session
import base64

# URLs de los WSDL en ambiente de pruebas
WSDL_RECEPCION_PRUEBAS = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"
WSDL_AUTORIZACION_PRUEBAS = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"


def enviar_comprobante(xml_firmado_path):
    """
    Envía el comprobante firmado al SRI (Recepción).
    xml_firmado_path: Ruta del archivo XML firmado.
    """
    with open(xml_firmado_path, "rb") as f:
        xml_bytes = f.read()
        xml_b64 = base64.b64encode(xml_bytes).decode()

    session = Session()
    transport = Transport(session=session)

    client = Client(wsdl=WSDL_RECEPCION_PRUEBAS, transport=transport)
    respuesta = client.service.validarComprobante(xml_b64)
    return respuesta


def consultar_autorizacion(clave_acceso):
    """
    Consulta la autorización de un comprobante en el SRI.
    clave_acceso: Clave de acceso generada (49 dígitos).
    """
    session = Session()
    transport = Transport(session=session)

    client = Client(wsdl=WSDL_AUTORIZACION_PRUEBAS, transport=transport)
    respuesta = client.service.autorizacionComprobante(clave_acceso)
    return respuesta
