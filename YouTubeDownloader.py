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

def descargar_video():
    # Función para descargar un video de YouTube

    url_video = input("Ingresa la URL del video: ")

    try:
        yt = YouTube(url_video)
        
        # Mostrar los detalles del video
        print("Detalles del video:")
        print("Título:", yt.title)
        print("Duración:", yt.length, "segundos")
        
        # Menú de selección
        print("Elige el formato de descarga:")
        print("1 - MP3 Audio")
        print("2 - MP4 Video")
        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion == "1":
            # Descargar y convertir a MP3
            audio = yt.streams.filter(only_audio=True).first()
            ruta_descarga = input("Ingresa la ruta para guardar el audio: ")
            print("Descargando audio...")
            audio_file = audio.download(ruta_descarga)
            
            # Convertir a formato MP3
            audio_mp4 = AudioSegment.from_file(audio_file)
            ruta_mp3 = os.path.join(ruta_descarga, f"{yt.title}.mp3")
            audio_mp4.export(ruta_mp3, format="mp3")
            print("Descarga del audio listo:", ruta_mp3)
            
            # Eliminar el archivo MP4
            os.remove(audio_file)
            
        elif opcion == "2":
            # Descargar video en formato MP4
            video = yt.streams.filter(progressive=True, file_extension='mp4').first()
            ruta_descarga = input("tipiar ruta para guardar la descarga: ")
            print("Descargando video...")
            video.download(ruta_descarga, filename='temp')
            video.register_on_complete_callback(lambda: print("\nDescarga del video listo:", ruta_descarga))

            def on_progress(stream, chunk, file_handle, bytes_remaining):
                # Mostrar progreso de descarga
                size = stream.filesize
                progress = round(100 * (1 - bytes_remaining / size), 1)
                print(f"\rDescargando... [{progress}%]", end='')

            video.register_on_progress_callback(on_progress)
        else:
            print("Opción no válida. elige 1 para MP3 o 2 para MP4.")
    except Exception as e:
        print("Ocurrió un error al descargar:", str(e))

descargar_video()
