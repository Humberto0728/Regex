import pdfplumber
import re

with pdfplumber.open("archivo.pdf") as pdf:
    texto = ""

    for pagina in pdf.pages:
        texto += pagina.extract_text()

print("Texto extraído:")
print(texto[:300])

# Regex de prueba (correos)
patron = r"[\w\.-]+@[\w\.-]+"

resultados = re.findall(patron, texto)

print("\nResultados:")
for r in resultados:
    print(r)