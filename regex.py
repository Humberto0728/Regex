import pdfplumber
import re


def extraer_texto_pdf(ruta_pdf):
    texto = ""

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()
            if contenido:
                texto += contenido + "\n"

    return texto


def limpiar_texto(texto):
    texto = texto.replace("\xa0", " ")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def extraer_datos_pdf(ruta_pdf):
    texto = extraer_texto_pdf(ruta_pdf)
    texto = limpiar_texto(texto)

    patrones = {
        "numero": r"No\.\s*(\d+)",

        "vigencia_desde": (
            r"Vigencia\s*desde\s*[:\-]?\s*"
            r"([a-zA-ZáéíóúñÁÉÍÓÚÑ]+\s+\d{1,2},\s+\d{4})"
        ),

        "razon_social": (
            r"1\.1\s*Raz[oó]n\s*social\s*del\s*oferente\s*[:\-]?\s*(.+?)\s*1\.2"
        ),

        "nit": r"1\.2\s*NIT\s*[:\-]?\s*(\d+)",

        "cod": r"1\.4\s*COD\s*[:\-]?\s*(\d+)",

        "sector_seccion": (
            r"Sector\s*[-–]\s*Secci[oó]n\s*[:\-]?\s*(.+?)\s*C[oó]digo"
        ),

        "codigo_proveedor": r"C[oó]digo\s*Proveedor\s*[:\-]?\s*(\d+)",

        "tipo_compra": (
            r"Tipo\s*de\s*Compra\s*[:\-]?\s*(.+?)\s*(3\.3|$)"
        ),

        "descuento_volumen": (
            r"3\.3\s*Descuento\s*por\s*escala\s*de\s*volumen\s*de\s*compra\s*[:\-]?\s*(\d+%)"
        ),

        "descuento_primera_compra": (
            r"5\.3\s*Descuento\s*en\s*primera\s*compra.*?(\d+%)"
        ),

        "valor_servicio": (
            r"6\.1\s*SOLICITUD\s*DE\s*PRESTACI[oó]N\s*DE\s*SERVICIOS"
            r".*?Valor\s*[:\-]?\s*\$?\s*([\d\.,]+)"
        ),

        "comentarios": r"Comentarios\s*adicionales\s*[:\-]?\s*(.+)"
    }

    datos = {}

    for campo, patron in patrones.items():
        match = re.search(patron, texto, re.IGNORECASE)
        datos[campo] = match.group(1).strip() if match else None

    return datos


if __name__ == "__main__":
    ruta_pdf = "P2.pdf"
    resultado = extraer_datos_pdf(ruta_pdf)

    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")