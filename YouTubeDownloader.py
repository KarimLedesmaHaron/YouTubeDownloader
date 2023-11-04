# ===================================================
# YouTubeDownloader
# Autor: "K" kharon.it@gmail.com
# Fecha: 4 de Noviembre 2023 / Córdoba - Argentina
#
# pip install pytube
# pip install pydub
# ===================================================
logo = """

╭╮╱╱╭╮╱╱╱╭━━━━╮╱╭╮╱╱╱╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╱╭╮
┃╰╮╭╯┃╱╱╱┃╭╮╭╮┃╱┃┃╱╱╱╱╰╮╭╮┃╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱┃┃
╰╮╰╯╭┻━┳╮┣┫┃┃┣┫╭┫╰━┳━━╮┃┃┃┣━━┳╮╭╮╭┳━╮┃┃╭━━┳━━┳━╯┣━━╮
╱╰╮╭┫╭╮┃┃┃┃┃┃┃┃┃┃╭╮┃┃━┫┃┃┃┃╭╮┃╰╯╰╯┃╭╮┫┃┃╭╮┃╭╮┃╭╮┃┃━┫
╱╱┃┃┃╰╯┃╰╯┃┃┃┃╰╯┃╰╯┃┃━╋╯╰╯┃╰╯┣╮╭╮╭┫┃┃┃╰┫╰╯┃╭╮┃╰╯┃┃━┫
╱╱╰╯╰━━┻━━╯╰╯╰━━┻━━┻━━┻━━━┻━━╯╰╯╰╯╰╯╰┻━┻━━┻╯╰┻━━┻━━╯
                                        Creado por "K"
    """
print(logo)

from pytube import YouTube
from pydub import AudioSegment
import os

def duracion_formateada(segundos):
    # Función para convertir segundos a formato horas:minutos:segundos
    minutos, segundos = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    if horas > 0:
        return f"{horas}:{minutos:02d}:{segundos:02d}"
    else:
        return f"{minutos:02d}:{segundos:02d}"

def descargar_video():
    # Función para descargar un video de YouTube

    url_video = input("URL del video: ")

    try:
        yt = YouTube(url_video)
        
        # Mostrar los detalles del video
        print("Detalles del video:")
        print("Título:", yt.title)
        print("Autor:", yt.author)
        print("Visualizaciones:", yt.views)
        # Formatear la fecha de publicación
        fecha_publicacion = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'No disponible'
        print("Fecha de Publicación:", fecha_publicacion)
        print("Duración:", duracion_formateada(yt.length))  # Muestra la duración formateada

        # Obtener todos los formatos disponibles
        all_streams = yt.streams.filter(only_video=True).order_by('resolution').desc()
        
        # Seleccionar el formato con el bitrate más alto
        formato_descarga = all_streams.first()

        # Mostrar detalles del formato seleccionado
        print("\nFormato con más alta definición encontrado:")
        print(f"Resolución: {formato_descarga.resolution if formato_descarga.resolution else 'Audio only'}, Format: {formato_descarga.mime_type}, Bitrate: {formato_descarga.bitrate / 1000} Kbps")
        
        # Menú de selección
        print("\nElige el formato que descargar en Alta definición:")
        print("1 - MP3 Audio")
        print("2 - MP4 Video")
        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion == "1":
            # Descargar y convertir a MP3
            audio = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
            ruta_descarga = input("Ingresa la ruta para guardar el audio o solo dale al ENTER: ")
            audio_file_path = os.path.join(ruta_descarga, f"{yt.title}.mp3")

            # Verificar si el archivo ya existe y renombrar si es necesario
            if os.path.exists(audio_file_path):
                count = 1
                while os.path.exists(audio_file_path):
                    audio_file_path = os.path.join(ruta_descarga, f"{yt.title}_{count}.mp3")
                    count += 1

            print("Descargando audio...")
            audio_file = audio.download(output_path=ruta_descarga, filename=audio_file_path)
            os.rename(audio_file, audio_file_path)

            print("Descarga del audio listo:", audio_file_path)
            
        elif opcion == "2":
            # Descargar video en formato MP4
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            ruta_descarga = input("Ingresa la ruta para guardar o solo dale al ENTER: ")
            video_file_path = os.path.join(ruta_descarga, f"{yt.title}.mp4")

            # Verificar si el archivo ya existe y renombrar si es necesario
            if os.path.exists(video_file_path):
                count = 1
                while os.path.exists(video_file_path):
                    video_file_path = os.path.join(ruta_descarga, f"{yt.title}_{count}.mp4")
                    count += 1

            print("Descargando video...")
            video_file = video.download(output_path=ruta_descarga, filename=video_file_path)
            os.rename(video_file, video_file_path)

            print("Descarga del video listo:", video_file_path)
        else:
            print("Opción no válida. Elige 1 para MP3 o 2 para MP4.")
    except Exception as e:
        print("Ocurrió un error al descargar:", str(e))

descargar_video()
