import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfReader
import uuid
import threading

class KnowledgeBaseGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Base de Conocimiento")
        self.root.geometry("600x500")
        self.root.config(bg="#2C3E50")

        # Estilo de los widgets
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#000000", foreground="white")
        style.configure("TLabel", font=("Helvetica", 11), background="#2C3E50", foreground="white")
        
        # Aplicando fondo negro a los botones utilizando 'tk' en lugar de 'ttk' para mayor flexibilidad
        self.select_button = tk.Button(root, text="Seleccionar Archivos", command=self.select_files, bg="#000000", fg="white", font=("Helvetica", 12))
        self.select_button.pack(pady=10)

        # Etiqueta para mostrar el estado
        self.status_label = ttk.Label(root, text="Seleccione los archivos para generar la base de conocimiento", wraplength=500)
        self.status_label.pack(pady=20)

        # Barra de progreso
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        self.progress["value"] = 0

        # Spinner (indicador de carga)
        self.spinner_label = ttk.Label(root, text="", wraplength=500)
        self.spinner_label.pack(pady=10)

        # Botón para generar el dataset
        self.generate_button = tk.Button(root, text="Generar Dataset", command=self.start_generation, state=tk.DISABLED, bg="#000000", fg="white", font=("Helvetica", 12))
        self.generate_button.pack(pady=10)

        # Botón para descargar el dataset
        self.download_button = tk.Button(root, text="Descargar Dataset", command=self.download_dataset, state=tk.DISABLED, bg="#000000", fg="white", font=("Helvetica", 12))
        self.download_button.pack(pady=10)

        # Variable para almacenar archivos seleccionados
        self.selected_files = []
        self.dataset = []
        self.output_file = None

    def select_files(self):
        """Permite seleccionar múltiples archivos PDF o cualquier tipo de documento."""
        files = filedialog.askopenfilenames(filetypes=[("Archivos", "*.pdf;*.txt;*.docx;*.json")])
        if files:
            self.selected_files = files
            self.generate_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Archivos seleccionados: {len(files)}")

    def extract_text_from_pdf(self, file_path):
        """Extrae el texto de un archivo PDF usando list comprehension."""
        return ''.join([page.extract_text() for page in PdfReader(file_path).pages]).strip()

    def generate_document_entry(self, file_path):
        """Genera la entrada del dataset para un documento."""
        document_text = (
            self.extract_text_from_pdf(file_path) if file_path.endswith('.pdf') else 
            open(file_path, 'r', encoding='utf-8').read().strip() if file_path.endswith('.txt') else
            f"Referencia al documento: {os.path.basename(file_path)}"
        )
        
        return {
            "DOCUMENT_ID": str(uuid.uuid4()),
            "DOCUMENT": document_text,
            "DOCUMENT_SOURCE": file_path,
            "SOURCE_DESCRIPTION": f"Descripción de {os.path.basename(file_path)}",
            "METADATA": {
                "file_name": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "file_type": os.path.splitext(file_path)[1]
            }
        }

    def generate_dataset(self):
        """Genera un dataset en formato JSON basado en los archivos seleccionados."""
        self.dataset = [self.generate_document_entry(file_path) for file_path in self.selected_files]

        # Barra de progreso avanzada
        total_files = len(self.selected_files)
        self.progress["maximum"] = total_files
        for idx, _ in enumerate(self.selected_files, 1):
            self.progress["value"] = idx
            self.root.update_idletasks()

        # Guardar el dataset en formato JSON
        self.output_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if self.output_file:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.dataset, f, indent=4, ensure_ascii=False)
            self.status_label.config(text="Dataset generado exitosamente")
            self.download_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Proceso cancelado")

        self.progress["value"] = 0

    def start_generation(self):
        """Inicia el proceso de generación del dataset en un hilo separado."""
        self.spinner_label.config(text="Procesando...", foreground="#F39C12")
        self.generate_button.config(state=tk.DISABLED)
        self.download_button.config(state=tk.DISABLED)

        threading.Thread(target=self._generate_and_complete).start()

    def _generate_and_complete(self):
        """Genera el dataset y actualiza la interfaz al finalizar."""
        self.generate_dataset()
        self.spinner_label.config(text="")
        self.status_label.config(text="Proceso completado", foreground="#2ECC71")

    def download_dataset(self):
        """Permite descargar el archivo JSON generado."""
        if self.output_file:
            # Mostrar diálogo para guardar el archivo
            messagebox.showinfo("Descargar", f"El dataset está guardado en {self.output_file}")
        else:
            messagebox.showerror("Error", "No se ha generado ningún dataset")


# Ejecutar la GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = KnowledgeBaseGenerator(root)
    root.mainloop()
