# YouTube MP3 Downloader

Una aplicación de escritorio desarrollada en Python que permite descargar música de YouTube y convertirla a formato MP3 de manera sencilla.

## Características

- Interfaz gráfica intuitiva y fácil de usar
- Descarga de audio en la mejor calidad disponible
- Conversión automática a formato MP3
- Selección de carpeta de destino personalizada
- Barra de progreso para visualizar el avance de la descarga
- Manejo de errores robusto
- Compatible con los cambios recientes en la API de YouTube

## Requisitos

- Python 3.6 o superior
- Bibliotecas de Python (instalables mediante `pip`):
  - pytubefix (para la descarga de videos de YouTube)
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
python youtube_downloader.py
```

2. Ingresa la URL del video de YouTube que deseas descargar
3. Selecciona la carpeta donde quieres guardar el archivo MP3
4. Haz clic en "DOWNLOAD"
5. ¡Listo! La aplicación descargará el audio y lo convertirá a MP3 automáticamente

## Notas Importantes

- Esta aplicación usa `pytubefix` en lugar de `pytube` debido a que esta última ha dejado de funcionar correctamente con los cambios recientes en YouTube.
- La aplicación está diseñada para uso personal y educativo.
- Respeta los derechos de autor y los términos de servicio de YouTube al utilizar esta herramienta.

## Solución de Problemas

Si experimentas algún problema, verifica lo siguiente:

1. Asegúrate de tener instalada la versión más reciente de pytubefix:
   ```
   pip install --upgrade pytubefix
   ```

2. Verifica que la URL sea correcta y que el video no tenga restricciones (edad, región, etc.)

3. Comprueba que tienes conexión a Internet

4. Para detalles específicos sobre un error, revisa el mensaje que se muestra en la aplicación.
