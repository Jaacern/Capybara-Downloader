import os
import subprocess
import shutil
import sys

def main():
    print("Building Claude Downloader...")
    
    # Step 1: Compiling resources...
    print("Paso 1: Compilando recursos...")
    try:
        # Verificar que existan los archivos de recursos
        if not os.path.exists('resources.qrc'):
            print("✗ Error: El archivo resources.qrc no existe")
            sys.exit(1)
            
        # Verificar que existan las imágenes referenciadas
        if not os.path.exists('images/logo.png'):
            print("✗ Error: No se encontró images/logo.png")
            sys.exit(1)
        if not os.path.exists('images/icon.png'):
            print("✗ Error: No se encontró images/icon.png")
            sys.exit(1)
        if not os.path.exists('images/loading.gif'):
            print("✗ Error: No se encontró images/loading.gif")
            sys.exit(1)
        
        # Compilar resources.qrc
        subprocess.run(['pyrcc5', 'resources.qrc', '-o', 'resources_rc.py'], check=True)
        print("✓ Recursos compilados exitosamente")
        
        # Verificar que el archivo se generó correctamente
        if not os.path.exists('resources_rc.py'):
            print("✗ El archivo resources_rc.py no se generó")
            sys.exit(1)
        
    except Exception as e:
        print(f"✗ Error compilando recursos: {e}")
        sys.exit(1)
    
    # Step 2: Ensure ffmpeg exists in the correct location
    print("Paso 2: Verificando FFmpeg...")
    ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg')
    ffmpeg_exe = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    ffprobe_exe = os.path.join(ffmpeg_dir, 'ffprobe.exe')
    
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir, exist_ok=True)
        print("  Directorio ffmpeg creado")
    
    # Check if FFmpeg files exist
    ffmpeg_present = os.path.exists(ffmpeg_exe)
    ffprobe_present = os.path.exists(ffprobe_exe)
    
    if ffmpeg_present and ffprobe_present:
        print("✓ Archivos FFmpeg encontrados")
    else:
        missing = []
        if not ffmpeg_present:
            missing.append("ffmpeg.exe")
        if not ffprobe_present:
            missing.append("ffprobe.exe")
        print(f"! Advertencia: Falta {', '.join(missing)} en la carpeta ffmpeg")
        print("  Por favor descarga FFmpeg desde https://ffmpeg.org/download.html")
        print("  y coloca ffmpeg.exe y ffprobe.exe en la carpeta 'ffmpeg' antes de ejecutar la app")
    
    # Step 3: Building executable with PyInstaller...
    print("Paso 3: Construyendo ejecutable con PyInstaller...")
    
    # Base command
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=Claude_Downloader',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',  # Skip confirmation for overwriting
    ]
    
    # Add icon if exists
    icon_path = os.path.join('images', 'icon.ico')
    if os.path.exists(icon_path):
        pyinstaller_cmd.append(f'--icon={icon_path}')
        print("  Usando archivo de icono:", icon_path)
    else:
        # Try looking for .png version to convert
        png_icon = os.path.join('images', 'icon.png')
        if os.path.exists(png_icon):
            print(f"  Icono .ico no encontrado, pero se encontró {png_icon}")
            print("  Usando el icono PNG directamente")
            pyinstaller_cmd.append(f'--icon={png_icon}')
        else:
            print("  No se encontró archivo de icono")
    
    # Add data files - make sure we include all necessary resources
    data_files = [
        '--add-data=images;images',
        '--add-data=resources_rc.py;.',  # Añadir el archivo de recursos compilado
    ]
    
    # Explicitly add each required file in images folder
    for img_file in ['logo.png', 'icon.png', 'loading.gif', 'icon.ico']:
        img_path = os.path.join('images', img_file)
        if os.path.exists(img_path):
            data_files.append(f'--add-data={img_path};images')
    
    pyinstaller_cmd.extend(data_files)
    
    # Add FFmpeg if present - use --add-binary for .exe files
    if ffmpeg_present:
        pyinstaller_cmd.append(f'--add-binary={ffmpeg_exe};ffmpeg')
    if ffprobe_present:
        pyinstaller_cmd.append(f'--add-binary={ffprobe_exe};ffmpeg')
    
    # Add the hidden imports needed for yt-dlp
    pyinstaller_cmd.extend([
        '--hidden-import=yt_dlp',
        '--hidden-import=yt_dlp.extractor',
        # Añadir importaciones ocultas específicas para funcionalidad de formatos de calidad
        '--hidden-import=yt_dlp.extractor.youtube',
        '--hidden-import=yt_dlp.extractor.common',
        '--hidden-import=yt_dlp.downloader',
        '--hidden-import=yt_dlp.downloader.fragment',
        '--hidden-import=yt_dlp.options',
        '--hidden-import=yt_dlp.postprocessor',
        '--hidden-import=yt_dlp.postprocessor.ffmpeg',
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
    ])
    
    # Add the main script
    pyinstaller_cmd.append('main.py')
    
    # Run PyInstaller
    try:
        print("  Ejecutando PyInstaller...")
        print(f"  Comando: {' '.join(pyinstaller_cmd)}")
        subprocess.run(pyinstaller_cmd, check=True)
        print("✓ Construcción del ejecutable completada")
    except Exception as e:
        print(f"✗ Error construyendo ejecutable: {e}")
        sys.exit(1)
    
    # Step 4: Copy any additional needed files
    print("Paso 4: Copiando archivos adicionales...")
    dist_dir = os.path.join(os.getcwd(), 'dist')
    
    # Copiar FFmpeg explícitamente al directorio dist
    if ffmpeg_present or ffprobe_present:
        os.makedirs(os.path.join(dist_dir, 'ffmpeg'), exist_ok=True)
        if ffmpeg_present:
            shutil.copy(ffmpeg_exe, os.path.join(dist_dir, 'ffmpeg', 'ffmpeg.exe'))
            print("  FFmpeg copiado al directorio dist/ffmpeg")
        if ffprobe_present:
            shutil.copy(ffprobe_exe, os.path.join(dist_dir, 'ffmpeg', 'ffprobe.exe'))
            print("  FFprobe copiado al directorio dist/ffmpeg")
    # Si no está presente en el proyecto, buscar
    # Si FFmpeg no está en la carpeta del proyecto, intenta buscarlo en el PATH
    else:
        try:
            print("  Buscando FFmpeg en el PATH del sistema...")
            # En Windows usamos 'where', en Unix/Linux sería 'which'
            ffmpeg_path = subprocess.check_output(["where", "ffmpeg"], text=True).strip().split('\n')[0]
            if os.path.exists(ffmpeg_path):
                os.makedirs(os.path.join(dist_dir, 'ffmpeg'), exist_ok=True)
                shutil.copy(ffmpeg_path, os.path.join(dist_dir, 'ffmpeg', 'ffmpeg.exe'))
                print(f"  FFmpeg copiado desde {ffmpeg_path} a dist/ffmpeg")
                
                # Intentar encontrar ffprobe también
                try:
                    ffprobe_path = subprocess.check_output(["where", "ffprobe"], text=True).strip().split('\n')[0]
                    if os.path.exists(ffprobe_path):
                        shutil.copy(ffprobe_path, os.path.join(dist_dir, 'ffmpeg', 'ffprobe.exe'))
                        print(f"  FFprobe copiado desde {ffprobe_path} a dist/ffmpeg")
                except Exception:
                    print("  FFprobe no encontrado en el PATH")
            else:
                print("  FFmpeg encontrado pero el archivo no existe")
        except Exception as e:
            print(f"  FFmpeg no encontrado en el PATH: {e}")
            print("  ¡ADVERTENCIA! El ejecutable no funcionará sin FFmpeg")
    
    # Comprobar y copiar las imágenes necesarias
    images_dist_dir = os.path.join(dist_dir, 'images')
    os.makedirs(images_dist_dir, exist_ok=True)
    
    for img in ['logo.png', 'icon.png', 'loading.gif', 'icon.ico']:
        img_path = os.path.join('images', img)
        if os.path.exists(img_path):
            shutil.copy(img_path, os.path.join(images_dist_dir, img))
            print(f"  Copiado {img_path} a la carpeta dist/images")
    
    # Crear un archivo README o instrucciones
    readme_content = """
    Claude Downloader
    ===================
    
    Gracias por usar Claude Downloader!
    
    Instrucciones:
    1. Pega el enlace de YouTube en el campo de URL
    2. Haz clic en "Seleccionar calidad" para elegir una resolución específica:
       - 144p (muy baja calidad)
       - 240p (baja calidad)
       - 360p (calidad media-baja)
       - 480p (calidad estándar/DVD)
       - 720p (HD)
       - 1080p (Full HD)
       - 1440p (2K/QHD)
       - 2160p (4K/UHD)
       - 4320p (8K)
       - Solo audio (MP3)
       - Solo audio (M4A)
    3. O haz clic en "Agregar a lista" para usar la mejor calidad disponible
    4. Haz clic en "Descargar todo" para comenzar las descargas
    5. Los archivos se guardarán en la ubicación seleccionada
    
    Requisito: FFmpeg debe estar instalado o presente en la carpeta 'ffmpeg'
    
    Disfruta tu Claude Downloader!
    """
    
    with open(os.path.join(dist_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Check if build was successful
    exe_path = os.path.join(dist_dir, 'Claude_Downloader.exe')
    if os.path.exists(exe_path):
        print(f"\n¡Proceso de build completado con éxito!")
        print(f"El ejecutable se encuentra en: {exe_path}")
        print("\nVerifica que FFmpeg esté disponible en la carpeta 'ffmpeg' junto al ejecutable.")
    else:
        print("\n✗ Error: No se encontró el ejecutable generado")
        print("  Revisa los mensajes de error anteriores")

if __name__ == "__main__":
    main()