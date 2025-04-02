"""
YouTube MP3 Downloader (Versión Completa)
----------------------------------------------------
Aplicación para descargar música de YouTube y convertirla a formato MP3.
Incluye un menú desplegable para seleccionar la calidad de audio.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import re
import urllib.request
import urllib.error
from pytubefix import YouTube
from moviepy.editor import AudioFileClip

class YouTubeMP3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        # Ventana más alta para acomodar todos los widgets
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_path_var = tk.StringVar()
        self.download_path_var.set(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.status_var = tk.StringVar()
        self.status_var.set("Ingresa una URL de YouTube y haz clic en Buscar")
        self.progress_var = tk.DoubleVar()
        self.quality_var = tk.StringVar()
        
        # YouTube object y streams
        self.yt = None
        self.audio_streams = []
        self.selected_stream = None
        
        # Crear widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz de usuario."""
        # Marco principal con scroll por si es necesario
        main_canvas = tk.Canvas(self.root)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar por si fuera necesaria
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        
        # Frame dentro del canvas
        self.main_frame = ttk.Frame(main_canvas, padding="20")
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw", width=480)
        
        # Título
        title_label = ttk.Label(self.main_frame, text="YouTube MP3 Downloader", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # URL de YouTube
        self.url_frame = ttk.Frame(self.main_frame)
        self.url_frame.pack(fill=tk.X, pady=5)
        
        url_label = ttk.Label(self.url_frame, text="URL de YouTube:")
        url_label.pack(anchor=tk.W)
        
        url_entry_frame = ttk.Frame(self.url_frame)
        url_entry_frame.pack(fill=tk.X, pady=5)
        
        url_entry = ttk.Entry(url_entry_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botón de búsqueda
        search_button = tk.Button(
            url_entry_frame, 
            text="Buscar", 
            font=("Arial", 10),
            bg="#F5F5DC",  # Beige claro
            activebackground="#E8E8D0",
            height=1,
            width=10,
            relief=tk.RAISED,
            bd=2,
            command=self.search_video
        )
        search_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Frame para la selección de calidad (inicialmente oculto)
        self.quality_frame = ttk.Frame(self.main_frame)
        
        # Etiqueta para el dropdown
        quality_label = ttk.Label(self.quality_frame, text="Calidad de Audio:")
        quality_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Combobox (dropdown) para seleccionar calidad
        self.quality_dropdown = ttk.Combobox(
            self.quality_frame, 
            textvariable=self.quality_var, 
            state="readonly",
            width=40
        )
        self.quality_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Directorio de destino
        path_frame = ttk.Frame(self.main_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        path_label = ttk.Label(path_frame, text="Guardar en:")
        path_label.pack(anchor=tk.W)
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, pady=5)
        
        path_entry = ttk.Entry(path_entry_frame, textvariable=self.download_path_var, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(path_entry_frame, text="...", width=3, command=self.browse_directory)
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Barra de progreso
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=450)
        self.progress_bar.pack(pady=5)
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(anchor=tk.W)
        
        # Espacio adicional para asegurar que hay suficiente espacio para el botón
        spacer = ttk.Frame(self.main_frame, height=10)
        spacer.pack(fill=tk.X)
        
        # Frame para el botón de descarga (siempre visible al final)
        download_button_frame = ttk.Frame(self.main_frame)
        download_button_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)
        
        # Frame interno para centrar el botón
        button_center_frame = ttk.Frame(download_button_frame)
        button_center_frame.pack(anchor=tk.CENTER)
        
        # Botón de descarga - beige, más pequeño y centrado
        self.download_button = tk.Button(
            button_center_frame, 
            text="DOWNLOAD", 
            font=("Arial", 10, "bold"),
            bg="#F5F5DC",     # Beige
            activebackground="#E8E8D0",  # Beige más oscuro al hacer clic
            height=2,
            width=15,
            relief=tk.RAISED,
            bd=2,
            command=self.start_download,
            state=tk.DISABLED  # Inicialmente deshabilitado
        )
        self.download_button.pack(pady=5)
        
        # Configurar evento para cuando se selecciona una calidad en el dropdown
        self.quality_dropdown.bind('<<ComboboxSelected>>', self.on_quality_selected)
    
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
    
    def on_quality_selected(self, event):
        """Maneja el evento de selección de una calidad en el dropdown"""
        selected_index = self.quality_dropdown.current()
        if selected_index >= 0 and selected_index < len(self.audio_streams):
            self.selected_stream = self.audio_streams[selected_index]
            # Habilitar el botón de descarga
            self.download_button.config(state=tk.NORMAL)
    
    def search_video(self):
        """Busca el video y muestra las opciones de calidad disponibles"""
        url = self.url_var.get().strip()
        
        # Validar URL
        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL de YouTube válida")
            return
        
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "La URL no parece ser una URL válida de YouTube.\nEjemplo: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            return
        
        # Verificar conexión a internet
        if not self.check_internet_connection():
            messagebox.showerror("Error", "No se detecta conexión a Internet. Por favor, verifica tu conexión.")
            return
        
        # Iniciar búsqueda en un hilo separado
        threading.Thread(target=self.fetch_video_info, args=(url,), daemon=True).start()
    
    def fetch_video_info(self, url):
        """Obtiene información del video en un hilo separado"""
        try:
            # Actualizar estado
            def update_status_searching():
                self.status_var.set("Buscando información del video...")
                self.progress_var.set(0)
                self.download_button.config(state=tk.DISABLED)
            
            self.root.after(0, update_status_searching)
            
            # Crear objeto YouTube con pytubefix
            try:
                self.yt = YouTube(url)
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
            video_title = self.yt.title
            
            # Obtener streams de audio disponibles
            self.audio_streams = self.yt.streams.filter(only_audio=True).order_by('abr').desc()
            
            if not self.audio_streams:
                raise Exception("No se encontraron streams de audio para este video. Podría estar protegido.")
            
            # Preparar datos para el dropdown menu
            quality_options = []
            for i, stream in enumerate(self.audio_streams):
                abr = stream.abr if stream.abr else "Unknown"
                mime_type = stream.mime_type.split('/')[1] if stream.mime_type else "Unknown"
                text = f"Calidad: {abr}, Formato: {mime_type}, Tamaño: {self.get_size_text(stream.filesize)}"
                quality_options.append(text)
            
            # Actualizar UI desde el hilo principal
            def update_ui():
                # Actualizar estado
                self.status_var.set(f"Video encontrado: {video_title}")
                
                # Actualizar dropdown con las opciones
                self.quality_dropdown['values'] = quality_options
                
                # Seleccionar la primera opción por defecto
                if len(quality_options) > 0:
                    self.quality_dropdown.current(0)
                    self.selected_stream = self.audio_streams[0]
                
                # Mostrar el frame de calidad si no está visible
                self.quality_frame.pack(fill=tk.X, pady=10, after=self.url_frame)
                
                # Habilitar el botón de descarga
                self.download_button.config(state=tk.NORMAL)
            
            self.root.after(0, update_ui)
            
        except Exception as e:
            error_message = str(e)
            
            def update_error():
                self.status_var.set(f"Error: {error_message}")
                messagebox.showerror("Error", f"Se produjo un error al buscar el video:\n{error_message}")
            
            self.root.after(0, update_error)
    
    def get_size_text(self, bytes_size):
        """Convierte bytes a texto legible (KB, MB)"""
        if bytes_size is None:
            return "Desconocido"
        
        kb_size = bytes_size / 1024
        if kb_size < 1024:
            return f"{kb_size:.1f} KB"
        else:
            mb_size = kb_size / 1024
            return f"{mb_size:.1f} MB"
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        """Función de callback para actualizar el progreso de descarga"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        # Limitar a 0-100
        percentage = max(0, min(percentage, 100))
        
        # Usar after para actualizar UI con seguridad
        def update_progress():
            self.progress_var.set(percentage)
            self.status_var.set(f"Descargando: {percentage:.1f}%")
        
        self.root.after(0, update_progress)
            
    def start_download(self):
        """Inicia la descarga con la calidad seleccionada"""
        download_path = self.download_path_var.get()
        
        # Validar ruta de descarga
        if not os.path.exists(download_path):
            messagebox.showerror("Error", "La carpeta de destino no existe")
            return
        
        # Verificar que se haya seleccionado una calidad
        if self.selected_stream is None:
            messagebox.showerror("Error", "Por favor, selecciona una calidad de audio")
            return
        
        # Iniciar descarga en un hilo separado
        threading.Thread(target=self.download_audio, args=(download_path,), daemon=True).start()
    
    def download_audio(self, download_path):
        try:
            # Actualizar estado
            def update_start():
                self.progress_var.set(0)
                self.status_var.set("Preparando la descarga...")
                self.download_button.config(state=tk.DISABLED)
            
            self.root.after(0, update_start)
            
            # Obtener título del video
            video_title = self.yt.title
            safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c in " ._-"]).rstrip()
            
            # Configurar callback de progreso
            self.yt.register_on_progress_callback(self.progress_callback)
            
            # Actualizar estado
            def update_status():
                self.status_var.set(f"Descargando: {safe_title}")
            
            self.root.after(0, update_status)
            
            # Descargar el audio
            try:
                temp_file = self.selected_stream.download(output_path=download_path, filename=f"{safe_title}.tmp")
            except Exception as e:
                if "404" in str(e) or "403" in str(e):
                    raise Exception("Error al descargar: El video podría tener restricciones regionales o de edad.")
                else:
                    raise Exception(f"Error al descargar el audio: {str(e)}")
            
            # Convertir a MP3
            def update_converting():
                self.status_var.set("Convirtiendo a MP3...")
            
            self.root.after(0, update_converting)
            
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
            def update_complete():
                self.progress_var.set(100)
                self.status_var.set(f"Descarga completada: {safe_title}.mp3")
                self.download_button.config(state=tk.NORMAL)
                messagebox.showinfo("Completado", f"La descarga se ha completado con éxito\n{safe_title}.mp3")
            
            self.root.after(0, update_complete)
            
        except Exception as e:
            error_message = str(e)
            
            def update_error():
                self.status_var.set(f"Error: {error_message}")
                self.download_button.config(state=tk.NORMAL)
                messagebox.showerror("Error", f"Se produjo un error durante la descarga:\n{error_message}")
            
            self.root.after(0, update_error)

def main():
    # Crear la ventana principal
    root = tk.Tk()
    
    # Centrar la ventana en la pantalla
    window_width = 500
    window_height = 400
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