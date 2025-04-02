"""
YouTube MP3 Downloader
----------------------
Una aplicación para descargar música de YouTube y convertirla a formato MP3.

Autor: Tu Nombre
"""

import tkinter as tk
from ui.app import YouTubeMP3App

def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = YouTubeMP3App(root)
    root.mainloop()

if __name__ == "__main__":
    main()