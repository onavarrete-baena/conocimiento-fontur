import pypdfium2 as pdfium
from pathlib import Path
from PIL import Image
import img2pdf
import os

# Ruta al archivo que pesa 132MB
input_path = "Caja de Herramientas para la Planificación Estratégica de Destinos Turísticos/03. Documentos de consulta/Ficha 5/Manual_Parte_2.pdf"
output_path = "Caja de Herramientas para la Planificación Estratégica de Destinos Turísticos/03. Documentos de consulta/Ficha 5/Manual_Parte_2_REDUCIDO.pdf"

escala = 1.5 # Balance entre legibilidad y peso
calidad = 50 # Compresión agresiva para bajar de 100MB

if not os.path.exists(input_path):
    print(f"Error: No encontré el archivo en {input_path}")
    exit()

print(f"Abriendo PDF: {input_path}")
pdf = pdfium.PdfDocument(input_path)
n_paginas = len(pdf)
imagenes = []

for i in range(n_paginas):
    print(f"Procesando página {i+1} de {n_paginas}...", end="\r")
    pagina = pdf.get_page(i)
    # Renderizamos a imagen
    bitmap = pagina.render(scale=escala)
    img = bitmap.to_pil()
    
    nombre_img = f"temp_pag_{i}.jpg"
    img.save(nombre_img, optimize=True, quality=calidad)
    imagenes.append(nombre_img)

print("\nUniendo imágenes en PDF final...")
with open(output_path, "wb") as f:
    f.write(img2pdf.convert(imagenes))

# Limpieza de basura temporal
for img in imagenes:
    os.remove(img)

print(f"¡Listo! Archivo guardado en: {output_path}")
