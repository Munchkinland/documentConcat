import os
from PyPDF2 import PdfWriter, PdfReader

def concatenate_pdfs(input_folder, output_folder):
    # Crear el directorio de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Inicializar el escritor de PDF y el contenido de texto
    pdf_writer = PdfWriter()
    text_content = ""

    # Listar todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            # Leer el archivo PDF
            pdf_reader = PdfReader(pdf_path)

            # Concatenar las páginas del PDF
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Extraer texto y concatenar
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"  # Extraer texto de cada página

    # Guardar el PDF concatenado
    output_pdf_path = os.path.join(output_folder, 'concatenated_document.pdf')
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    # Guardar el contenido de texto en un archivo TXT
    output_txt_path = os.path.join(output_folder, 'concatenated_document.txt')
    with open(output_txt_path, 'w', encoding='utf-8') as output_txt:
        output_txt.write(text_content)

    print(f'Archivos concatenados guardados en: {output_pdf_path} y {output_txt_path}')

# Definir las rutas de las carpetas de entrada y salida
input_folder = 'input'
output_folder = 'output'

# Ejecutar la función
concatenate_pdfs(input_folder, output_folder)
