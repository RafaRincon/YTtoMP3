"""
YouTube MP3 Downloader (Versión con PyTubeFix)
----------------------------------------------
Aplicación para descargar música de YouTube y convertirla a formato MP3.
Usa pytubefix en lugar de pytube para mayor compatibilidad.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import re
import urllib.request
import urllib.error
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import AudioFileClip

class YouTubeMP3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_path_var = tk.StringVar()
        self.download_path_var.set(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para descargar")
        self.progress_var = tk.DoubleVar()
        
        # Variable para seguir el progreso
        self.bytes_downloaded = 0
        self.file_size = 0
        
        # Crear widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="YouTube MP3 Downloader", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # URL de YouTube
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        url_label = ttk.Label(url_frame, text="URL de YouTube:")
        url_label.pack(anchor=tk.W)
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        url_entry.pack(fill=tk.X, pady=5)
        
        # Directorio de destino
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        path_label = ttk.Label(path_frame, text="Guardar en:")
        path_label.pack(anchor=tk.W)
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, pady=5)
        
        path_entry = ttk.Entry(path_entry_frame, textvariable=self.download_path_var, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(path_entry_frame, text="...", width=3, command=self.browse_directory)
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Barra de progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=450)
        self.progress_bar.pack(pady=5)
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(anchor=tk.W)
        
        # Botón de descarga - versión tk.Button para asegurar visibilidad
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        download_button = tk.Button(
            button_frame, 
            text="DOWNLOAD", 
            font=("Arial", 12, "bold"),
            bg="#FF0000",     # Rojo brillante
            fg="white",       # Texto blanco
            activebackground="#CC0000",  # Rojo más oscuro al hacer clic
            activeforeground="white",
            height=2,         # Altura del botón
            relief=tk.RAISED, # Efecto 3D
            bd=3,             # Borde más grueso
            command=self.start_download
        )
        download_button.pack(pady=10, fill=tk.X)
        
        # Asegurar que el botón tenga tamaño adecuado
        button_frame.pack_propagate(False)
        button_frame.configure(height=60)
    
    def browse_directory(self):
        download_dir = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if download_dir:
            self.download_path_var.set(download_dir)
    
    def is_valid_youtube_url(self, url):
        # Patrón para URLs de YouTube
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        
        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return True
        return False
    
    def check_internet_connection(self):
        try:
            # Intenta conectar a Google
            urllib.request.urlopen('http://www.google.com', timeout=3)
            return True
        except:
            return False
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        """Función de callback para actualizar el progreso de descarga"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        # Limitar a 0-100
        percentage = max(0, min(percentage, 100))
        
        # Actualizar la barra de progreso
        self.progress_var.set(percentage)
        self.status_var.set(f"Descargando: {percentage:.1f}%")
        self.root.update()
            
    def start_download(self):
        url = self.url_var.get().strip()
        download_path = self.download_path_var.get()
        
        # Validar URL
        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL de YouTube válida")
            return
        
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "La URL no parece ser una URL válida de YouTube.\nEjemplo: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            return
        
        # Validar ruta de descarga
        if not os.path.exists(download_path):
            messagebox.showerror("Error", "La carpeta de destino no existe")
            return
        
        # Verificar conexión a internet
        if not self.check_internet_connection():
            messagebox.showerror("Error", "No se detecta conexión a Internet. Por favor, verifica tu conexión.")
            return
        
        # Iniciar descarga en un hilo separado
        threading.Thread(target=self.download_audio, args=(url, download_path), daemon=True).start()
    
    def download_audio(self, url, download_path):
        try:
            # Actualizar estado
            self.progress_var.set(0)
            self.status_var.set("Obteniendo información del video...")
            self.root.update()
            
            # Crear objeto YouTube con pytubefix
            try:
                yt = YouTube(url, on_progress_callback=self.progress_callback)
            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg:
                    raise Exception("Acceso prohibido (Error 403). Este video puede tener restricciones.")
                elif "404" in error_msg:
                    raise Exception("Video no encontrado (Error 404). La URL podría ser incorrecta.")
                elif "400" in error_msg:
                    raise Exception("Solicitud incorrecta (Error 400). Intenta usando otra URL.")
                else:
                    raise Exception(f"Error al conectar con YouTube: {error_msg}")
            
            # Obtener título del video
            video_title = yt.title
            self.status_var.set(f"Video encontrado: {video_title}")
            self.root.update()
            
            # Generar nombre de archivo seguro
            safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c in " ._-"]).rstrip()
            
            # Verificar si hay streams de audio disponibles
            audio_stream = yt.streams.get_audio_only()
            if not audio_stream:
                # Intentar obtener el mejor stream de audio disponible
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                
            if not audio_stream:
                raise Exception("No se encontraron streams de audio para este video. Podría estar protegido.")
            
            # Actualizar estado
            self.status_var.set(f"Descargando: {safe_title}")
            self.root.update()
            
            # Descargar el audio
            try:
                temp_file = audio_stream.download(output_path=download_path, filename=f"{safe_title}.tmp")
            except Exception as e:
                if "404" in str(e) or "403" in str(e):
                    raise Exception("Error al descargar: El video podría tener restricciones regionales o de edad.")
                else:
                    raise Exception(f"Error al descargar el audio: {str(e)}")
            
            # Convertir a MP3
            self.status_var.set("Convirtiendo a MP3...")
            self.root.update()
            
            mp3_file = os.path.join(download_path, f"{safe_title}.mp3")
            try:
                audio_clip = AudioFileClip(temp_file)
                audio_clip.write_audiofile(mp3_file, logger=None)
                audio_clip.close()
                
                # Limpiar el archivo temporal
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                raise Exception(f"Error al convertir a MP3: {str(e)}")
            
            # Completado
            self.progress_var.set(100)
            self.status_var.set(f"Descarga completada: {safe_title}.mp3")
            messagebox.showinfo("Completado", f"La descarga se ha completado con éxito\n{safe_title}.mp3")
            
        except Exception as e:
            error_message = str(e)
            self.status_var.set(f"Error: {error_message}")
            messagebox.showerror("Error", f"Se produjo un error durante la descarga:\n{error_message}")

def main():
    # Crear la ventana principal
    root = tk.Tk()
    
    # Centrar la ventana en la pantalla
    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Crear la aplicación
    app = YouTubeMP3Downloader(root)
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()