import subprocess
from pathlib import Path


def firmar_xml(xml_path, cert_path, clave_cert, output_path):
    """
    Firma un XML usando xmlsec1 y un certificado .p12/.pfx
    """
    cmd = [
        "xmlsec1",
        "--sign",
        "--pkcs12", cert_path,
        "--pwd", clave_cert,
        "--output", output_path,
        xml_path
    ]
    subprocess.run(cmd, check=True)
    return Path(output_path)
