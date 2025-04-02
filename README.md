# YouTube MP3 Downloader

Una aplicación de escritorio desarrollada en Python que permite descargar música de YouTube y convertirla a formato MP3 de manera sencilla.

## Características

- Interfaz gráfica intuitiva y fácil de usar
- Descarga de audio en la mejor calidad disponible
- Conversión automática a formato MP3
- Selección de carpeta de destino personalizada
- Barra de progreso para visualizar el avance de la descarga
- Manejo de errores robusto

## Requisitos

- Python 3.6 o superior
- Bibliotecas de Python (instalables mediante `pip`):
  - pytube (para la descarga de videos de YouTube)
  - moviepy (para la conversión de audio)
  - tkinter (incluido con Python)

## Instalación

1. Clona este repositorio o descárgalo como archivo ZIP
2. Navega hasta la carpeta del proyecto
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:

```bash
python main.py
```

2. Ingresa la URL del video de YouTube que deseas descargar
3. Selecciona la carpeta donde quieres guardar el archivo MP3
4. Haz clic en "Descargar MP3"
5. ¡Listo! La aplicación descargará el audio y lo convertirá a MP3 automáticamente

## Estructura del Proyecto

```
youtube_mp3_downloader/
│
├── requirements.txt
├── main.py                   # Punto de entrada de la aplicación
├── README.md                 # Documentación del proyecto
│
├── downloader/
│   ├── __init__.py
│   ├── youtube_client.py     # Clase para interactuar con YouTube
│   ├── converter.py          # Clase para convertir audio
│   └── download_manager.py   # Orquestador del proceso de descarga
│
└── ui/
    ├── __init__.py
    ├── app.py                # Clase principal de la aplicación
    ├── main_window.py        # Ventana principal
    └── styles.py             # Estilos de la UI
```

## Posibles Mejoras Futuras

- Añadir soporte para listas de reproducción
- Implementar opciones de calidad de audio
- Agregar metadatos al archivo MP3 (artista, título, etc.)
- Permitir descargas simultáneas
- Soporte para otros formatos de audio (WAV, FLAC, etc.)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Descargo de Responsabilidad

Esta aplicación está diseñada con fines educativos y personales. Asegúrate de cumplir con los términos de servicio de YouTube y respetar los derechos de autor al utilizar este software.