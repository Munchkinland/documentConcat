import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
import csv

# Función para generar el dataset
def generate_dataset(pdf_paths, output_folder):
    if not pdf_paths:
        messagebox.showwarning("Advertencia", "No se seleccionaron archivos PDF.")
        return

    os.makedirs(output_folder, exist_ok=True)
    dataset = []

    for pdf_path in pdf_paths:
        # Extraer texto del PDF
        pdf_reader = PdfReader(pdf_path)
        text_content = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"

        # Generar un DOCUMENT_ID único (por ejemplo, el nombre del archivo sin extensión)
        document_id = os.path.splitext(os.path.basename(pdf_path))[0]

        # Obtener DOCUMENT_SOURCE y SOURCE_DESCRIPTION si es posible
        document_source = os.path.abspath(pdf_path)  # Ruta absoluta al archivo
        source_description = f"Archivo PDF: {os.path.basename(pdf_path)}"

        # Obtener METADATA si está disponible
        metadata = pdf_reader.metadata

        # Agregar registro al dataset
        dataset.append({
            'DOCUMENT': text_content,
            'DOCUMENT_ID': document_id,
            'DOCUMENT_SOURCE': document_source,
            'SOURCE_DESCRIPTION': source_description,
            'METADATA': metadata
        })

    # Guardar el dataset en un archivo CSV
    output_csv_path = os.path.join(output_folder, 'dataset.csv')
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['DOCUMENT', 'DOCUMENT_ID', 'DOCUMENT_SOURCE', 'SOURCE_DESCRIPTION', 'METADATA']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in dataset:
            # Convertir METADATA a string para almacenar en CSV
            metadata_str = str(data['METADATA']) if data['METADATA'] else ''
            writer.writerow({
                'DOCUMENT': data['DOCUMENT'],
                'DOCUMENT_ID': data['DOCUMENT_ID'],
                'DOCUMENT_SOURCE': data['DOCUMENT_SOURCE'],
                'SOURCE_DESCRIPTION': data['SOURCE_DESCRIPTION'],
                'METADATA': metadata_str
            })

    messagebox.showinfo("Éxito", f"Dataset generado en:\n{output_csv_path}")

# Función para seleccionar los PDFs
def select_pdfs():
    file_paths = filedialog.askopenfilenames(
        title="Seleccionar archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")])
    
    if file_paths:
        selected_files_label.config(text="\n".join(file_paths))
        global selected_pdfs
        selected_pdfs = list(file_paths)

# Función para seleccionar la carpeta de salida
def select_output_folder():
    folder_path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
    if folder_path:
        output_folder_label.config(text=folder_path)
        global output_folder
        output_folder = folder_path

# Función principal al hacer clic en "Generar Dataset"
def on_generate_dataset_click():
    if selected_pdfs and output_folder:
        generate_dataset(selected_pdfs, output_folder)
    else:
        messagebox.showwarning("Advertencia", "Seleccione archivos PDF y una carpeta de salida.")

# Configurar la ventana principal
root = tk.Tk()
root.title("Generador de Dataset para Chatbot")
root.geometry("600x400")

# Variables globales para almacenar PDFs seleccionados y carpeta de salida
selected_pdfs = []
output_folder = ""

# Botones y etiquetas para la selección de archivos y carpeta de salida
tk.Button(root, text="Seleccionar PDFs", command=select_pdfs, width=20).pack(pady=10)
selected_files_label = tk.Label(root, text="No se han seleccionado archivos PDF", wraplength=580, justify="left")
selected_files_label.pack(pady=10)

tk.Button(root, text="Seleccionar carpeta de salida", command=select_output_folder, width=20).pack(pady=10)
output_folder_label = tk.Label(root, text="No se ha seleccionado carpeta de salida")
output_folder_label.pack(pady=10)

# Botón para generar el dataset
tk.Button(root, text="Generar Dataset", command=on_generate_dataset_click, width=20).pack(pady=20)

# Ejecutar la ventana principal
root.mainloop()
