# PDF and TXT Concatenator

Este proyecto consiste en un script de Python que lee todos los archivos PDF de una carpeta, los concatena en un único documento PDF y TXT, y guarda los resultados en una carpeta de salida. Es útil para combinar múltiples documentos en un solo archivo para facilitar la gestión y lectura.

## Requisitos

Asegúrate de tener instalado Python en tu sistema. Este proyecto requiere la biblioteca `PyPDF2`. Puedes instalarla utilizando pip:

pip install PyPDF2

## Estructura de Carpetas

La estructura de carpetas debe ser la siguiente:

project/
│
├── input/          # Carpeta donde colocar los archivos PDF
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
│
├── output/         # Carpeta donde se guardarán los documentos concatenados
│
└── concatenate_pdfs.py  # Archivo del script de Python

## Uso

Prepara las carpetas:

    Crea una carpeta llamada input y coloca en ella los archivos PDF que deseas concatenar.
    Asegúrate de que exista una carpeta llamada output para almacenar los archivos resultantes.

Ejecuta el script:

    Abre una terminal o símbolo del sistema y navega a la carpeta del proyecto.
    Ejecuta el script con el siguiente comando:

python concatenate_pdfs.py

## Resultados:

    Después de ejecutar el script, encontrarás un archivo PDF y un archivo TXT concatenados en la carpeta output con los nombres concatenated_document.pdf y concatenated_document.txt.
    
## Contribuciones

Si deseas contribuir a este proyecto, no dudes en abrir un issue o enviar un pull request.
Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
