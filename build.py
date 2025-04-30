import os
import subprocess
import shutil
import sys

def main():
    print("Building Capybara Downloader...")
    
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
        if not os.path.exists('images/icon.ico'):
            print("✗ Error: No se encontró images/icon.ico")
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
    ffplay_exe = os.path.join(ffmpeg_dir, 'ffplay.exe')  # Añadido ffplay
    
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir, exist_ok=True)
        print("  Directorio ffmpeg creado")
    
    # Check if FFmpeg files exist
    ffmpeg_present = os.path.exists(ffmpeg_exe)
    ffprobe_present = os.path.exists(ffprobe_exe)
    ffplay_present = os.path.exists(ffplay_exe)  # Comprobar ffplay
    
    if ffmpeg_present and ffprobe_present and ffplay_present:
        print("✓ Todos los archivos FFmpeg encontrados")
    else:
        missing = []
        if not ffmpeg_present:
            missing.append("ffmpeg.exe")
        if not ffprobe_present:
            missing.append("ffprobe.exe")
        if not ffplay_present:
            missing.append("ffplay.exe")
        print(f"! Advertencia: Falta {', '.join(missing)} en la carpeta ffmpeg")
        print("  Por favor descarga FFmpeg desde https://ffmpeg.org/download.html")
        print("  y coloca todos los archivos .exe en la carpeta 'ffmpeg' antes de ejecutar la app")
    
    # Step 3: Building executable with PyInstaller...
    print("Paso 3: Construyendo ejecutable con PyInstaller...")
    
    # Base command
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=Capybara_Downloader',
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
    
    # Añadir carpeta de fuentes
    if os.path.exists('fonts'):
        data_files.append('--add-data=fonts;fonts')
        print("  Añadiendo carpeta de fuentes")
    
    pyinstaller_cmd.extend(data_files)
    
    # Add FFmpeg if present - use --add-binary for .exe files
    if ffmpeg_present:
        pyinstaller_cmd.append(f'--add-binary={ffmpeg_exe};ffmpeg')
    if ffprobe_present:
        pyinstaller_cmd.append(f'--add-binary={ffprobe_exe};ffmpeg')
    if ffplay_present:
        pyinstaller_cmd.append(f'--add-binary={ffplay_exe};ffmpeg')
    
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
        # Posibles dependencias para generación de imágenes
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--hidden-import=PIL.ImageFont',
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
    
    # Step 4: Copy any additional needed files to the dist directory
    print("Paso 4: Copiando archivos adicionales...")
    dist_dir = os.path.join(os.getcwd(), 'dist')
    
    # Asegurarse de que existe la carpeta dist
    if not os.path.exists(dist_dir):
        print("✗ Error: No se encontró el directorio dist generado por PyInstaller")
        sys.exit(1)
    
    # Crear directorio para el instalador (donde copiaremos todos los archivos)
    installer_dir = os.path.join(dist_dir, 'Capybara_Downloader_Installer')
    os.makedirs(installer_dir, exist_ok=True)
    
    # Copiar el ejecutable generado al directorio del instalador
    exe_path = os.path.join(dist_dir, 'Capybara_Downloader.exe')
    if os.path.exists(exe_path):
        shutil.copy(exe_path, os.path.join(installer_dir, 'Capybara_Downloader.exe'))
        print("  Ejecutable copiado al directorio del instalador")
    else:
        print("✗ Error: No se encontró el ejecutable generado")
        sys.exit(1)
    
    # Copiar FFmpeg explícitamente al directorio del instalador
    ffmpeg_dest_dir = os.path.join(installer_dir, 'ffmpeg')
    os.makedirs(ffmpeg_dest_dir, exist_ok=True)
    
    # Lista de archivos FFmpeg a copiar
    ffmpeg_files = {
        ffmpeg_exe: os.path.join(ffmpeg_dest_dir, 'ffmpeg.exe'),
        ffprobe_exe: os.path.join(ffmpeg_dest_dir, 'ffprobe.exe'),
        ffplay_exe: os.path.join(ffmpeg_dest_dir, 'ffplay.exe')
    }
    
    # Copiar cada archivo ffmpeg si existe
    for src, dest in ffmpeg_files.items():
        if os.path.exists(src):
            shutil.copy(src, dest)
            print(f"  Copiado {os.path.basename(src)} al directorio del instalador")
        else:
            print(f"  No se encontró {os.path.basename(src)}, buscando en el PATH...")
            try:
                # Buscar en el PATH
                cmd = "where" if sys.platform == "win32" else "which"
                path_result = subprocess.check_output([cmd, os.path.basename(src)], text=True).strip().split('\n')[0]
                if os.path.exists(path_result):
                    shutil.copy(path_result, dest)
                    print(f"  Copiado {os.path.basename(src)} desde PATH al directorio del instalador")
                else:
                    print(f"  No se pudo encontrar {os.path.basename(src)}")
            except Exception as e:
                print(f"  No se pudo encontrar {os.path.basename(src)} en el PATH: {e}")
    
    # Comprobar y copiar las imágenes necesarias
    images_dest_dir = os.path.join(installer_dir, 'images')
    os.makedirs(images_dest_dir, exist_ok=True)
    
    # Lista de imágenes requeridas para la aplicación
    app_images = ['logo.png', 'icon.png', 'loading.gif', 'icon.ico']
    
    # Lista de imágenes adicionales para el instalador
    installer_images = ['wizard_large.bmp', 'wizard_small.bmp']
    
    # Copiar imágenes de la aplicación
    for img in app_images:
        img_path = os.path.join('images', img)
        if os.path.exists(img_path):
            shutil.copy(img_path, os.path.join(images_dest_dir, img))
            print(f"  Copiado {img_path} a la carpeta del instalador")
        else:
            print(f"  Advertencia: No se encontró {img_path}")
    
    # Verificar y copiar imágenes del instalador
    missing_installer_images = []
    for img in installer_images:
        img_path = os.path.join('images', img)
        if os.path.exists(img_path):
            shutil.copy(img_path, os.path.join(images_dest_dir, img))
            print(f"  Copiado {img_path} a la carpeta del instalador")
        else:
            missing_installer_images.append(img)
    
    # Generar imágenes del instalador si faltan
    if missing_installer_images:
        print("  Algunas imágenes para el instalador no se encontraron:")
        for img in missing_installer_images:
            print(f"    - {img}")
        print("  Se recomienda crear estas imágenes para personalizar el instalador:")
        print("    - wizard_large.bmp: 164x314 píxeles (imagen lateral del asistente)")
        print("    - wizard_small.bmp: 55x58 píxeles (imagen superior del asistente)")
        
        # Verificar si se puede generar imágenes básicas (requiere PIL/Pillow)
        try:
            from PIL import Image, ImageDraw, ImageFont
            print("  Intentando generar imágenes básicas para el instalador...")
            
            # Generar wizard_large.bmp si falta
            if 'wizard_large.bmp' in missing_installer_images:
                try:
                    # Crear una imagen básica
                    img = Image.new('RGB', (164, 314), color=(240, 240, 240))
                    draw = ImageDraw.Draw(img)
                    
                    # Intentar dibujar un texto básico
                    try:
                        # Usar una fuente del sistema si está disponible
                        font_path = os.path.join('fonts', 'levenim-mt.ttf')
                        if os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, 16)
                        else:
                            font = ImageFont.load_default()
                        
                        draw.text((10, 10), "Capybara", fill=(0, 0, 0), font=font)
                        draw.text((10, 40), "Downloader", fill=(0, 0, 0), font=font)
                    except Exception as e:
                        print(f"    Error al añadir texto: {e}")
                    
                    # Guardar la imagen
                    wizard_large_path = os.path.join('images', 'wizard_large.bmp')
                    img.save(wizard_large_path)
                    shutil.copy(wizard_large_path, os.path.join(images_dest_dir, 'wizard_large.bmp'))
                    print("    ✓ Imagen wizard_large.bmp generada")
                except Exception as e:
                    print(f"    Error al generar wizard_large.bmp: {e}")
            
            # Generar wizard_small.bmp si falta
            if 'wizard_small.bmp' in missing_installer_images:
                try:
                    # Crear una imagen básica
                    img = Image.new('RGB', (55, 58), color=(240, 240, 240))
                    draw = ImageDraw.Draw(img)
                    
                    # Intentar dibujar un texto básico
                    try:
                        # Usar una fuente del sistema si está disponible
                        font_path = os.path.join('fonts', 'levenim-mt.ttf')
                        if os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, 10)
                        else:
                            font = ImageFont.load_default()
                        
                        draw.text((5, 5), "Capybara", fill=(0, 0, 0), font=font)
                        draw.text((5, 20), "Downloader", fill=(0, 0, 0), font=font)
                    except Exception as e:
                        print(f"    Error al añadir texto: {e}")
                    
                    # Guardar la imagen
                    wizard_small_path = os.path.join('images', 'wizard_small.bmp')
                    img.save(wizard_small_path)
                    shutil.copy(wizard_small_path, os.path.join(images_dest_dir, 'wizard_small.bmp'))
                    print("    ✓ Imagen wizard_small.bmp generada")
                except Exception as e:
                    print(f"    Error al generar wizard_small.bmp: {e}")
        except ImportError:
            print("  Pillow (PIL) no está instalado. No se pueden generar imágenes automáticamente.")
            print("  Para instalar: pip install Pillow")
            print("  O crea las imágenes manualmente y colócalas en la carpeta 'images'.")
    
    # Copiar archivos de fuentes
    fonts_dir = os.path.join(os.getcwd(), 'fonts')
    if os.path.exists(fonts_dir):
        fonts_dest_dir = os.path.join(installer_dir, 'fonts')
        os.makedirs(fonts_dest_dir, exist_ok=True)
        
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith('.ttf'):
                font_path = os.path.join(fonts_dir, font_file)
                shutil.copy(font_path, os.path.join(fonts_dest_dir, font_file))
                print(f"  Copiado {font_path} a la carpeta del instalador")
    
    # Crear un archivo README o instrucciones
    readme_content = """
    Capybara Downloader
    ===================
    
    Gracias por usar Capybara Downloader!
    
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
    
    Disfruta tu Capybara Downloader!
    """
    
    with open(os.path.join(installer_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
        
    # Crear archivo de licencia
    license_content = """# ACUERDO DE LICENCIA DE USUARIO FINAL (EULA) - CAPYBARA DOWNLOADER

## TÉRMINOS Y CONDICIONES

Última actualización: 29 de abril de 2025

Por favor, lea cuidadosamente este Acuerdo de Licencia de Usuario Final ("EULA", "Licencia") antes de instalar o utilizar Capybara Downloader ("el Software").

Al instalar o utilizar el Software, usted (el "Usuario") acepta estar legalmente obligado por los términos de esta Licencia. Si no está de acuerdo con los términos de esta Licencia, no instale ni utilice el Software.

### 1. CONCESIÓN DE LICENCIA

Este EULA otorga al Usuario una licencia revocable, no exclusiva, intransferible para usar el Software de acuerdo con los términos de este EULA.

El Usuario puede:
- Instalar y utilizar el Software en dispositivos personales.
- Hacer una copia del Software con fines de respaldo.

El Usuario NO puede:
- Modificar, descompilar, realizar ingeniería inversa o desensamblar el Software.
- Alquilar, arrendar, prestar, vender, redistribuir o sublicenciar el Software.
- Utilizar el Software para fines comerciales sin autorización previa por escrito.
- Utilizar el Software para actividades ilegales o que infrinjan los derechos de terceros.

### 2. PROPIEDAD INTELECTUAL

El Software, incluyendo pero no limitado a su código fuente, interfaces, contenido, logos y documentación, es propiedad del titular de los derechos y está protegido por leyes de propiedad intelectual y tratados internacionales.

Esta Licencia no le otorga ningún derecho de propiedad intelectual sobre el Software.

### 3. SOFTWARE DE TERCEROS

El Software utiliza componentes y bibliotecas de terceros, incluyendo pero no limitado a:
- FFmpeg, bajo Licencia GPL/LGPL
- yt-dlp, bajo Licencia Pública

El Usuario acepta cumplir con los términos de licencia aplicables a estos componentes de terceros.

### 4. DESCARGO DE RESPONSABILIDAD Y LIMITACIÓN DE RESPONSABILIDAD

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIABILIDAD, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN.

EN NINGÚN CASO EL TITULAR DE LOS DERECHOS SERÁ RESPONSABLE POR CUALQUIER RECLAMACIÓN, DAÑOS U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O DE OTRO TIPO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.

### 5. USO RESPONSABLE

El Usuario es responsable de usar el Software de manera legal y ética. El Software está diseñado para descargar contenido de plataformas en línea únicamente cuando:
- El Usuario tiene derecho legal a hacerlo
- La descarga cumple con los términos de servicio de la plataforma de origen
- El contenido se utiliza para fines personales y no comerciales, a menos que esté específicamente permitido

### 6. TERMINACIÓN

Esta Licencia es efectiva hasta su terminación. Sus derechos bajo esta Licencia terminarán automáticamente sin previo aviso si no cumple con cualquiera de los términos y condiciones de esta Licencia.

### 7. MODIFICACIONES DEL ACUERDO

El titular de los derechos se reserva el derecho de modificar los términos de este EULA en cualquier momento. Las modificaciones entrarán en vigor inmediatamente después de su publicación.

### 8. LEY APLICABLE

Este EULA se regirá por las leyes del país/estado de residencia del titular de los derechos, sin tener en cuenta los conflictos de principios legales.

---

Al instalar y utilizar Capybara Downloader, usted reconoce que ha leído este EULA, lo entiende y acepta estar obligado por sus términos y condiciones."""
    
    with open(os.path.join(installer_dir, 'LICENSE.txt'), 'w', encoding='utf-8') as f:
        f.write(license_content)
    
    # Crear un archivo básico de script para Inno Setup
# Busca esta sección en el archivo build.py donde se define el script para Inno Setup
# Alrededor de la línea donde dice "Crear un archivo básico de script para Inno Setup"

# Reemplaza la definición de inno_script con esta versión actualizada:
    inno_script = f"""
    #define MyAppName "Capybara Downloader"
    #define MyAppVersion "1.0"
    #define MyAppPublisher "Capybara Downloader"
    #define MyAppURL "https://github.com/Jaacern/Capybara-Downloader"
    #define MyAppExeName "Capybara_Downloader.exe"

    [Setup]
    AppId={{{{CAPY-12345-DOWNLOADER}}}}
    AppName={{#MyAppName}}
    AppVersion={{#MyAppVersion}}
    AppPublisher={{#MyAppPublisher}}
    AppPublisherURL={{#MyAppURL}}
    AppSupportURL={{#MyAppURL}}
    AppUpdatesURL={{#MyAppURL}}
    DefaultDirName={{autopf}}\\{{#MyAppName}}
    DefaultGroupName={{#MyAppName}}
    AllowNoIcons=yes
    LicenseFile=LICENSE.txt
    OutputDir=.
    OutputBaseFilename=Capybara_Downloader_Setup
    Compression=lzma
    SolidCompression=yes
    WizardStyle=modern
    ; Corregir la ruta del icono sin comillas para evitar errores
    SetupIconFile=images\\icon.ico
    WizardImageFile=images\\wizard_large.bmp
    WizardSmallImageFile=images\\wizard_small.bmp

    [Languages]
    Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"

    [Tasks]
    Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

    [Files]
    Source: "Capybara_Downloader.exe"; DestDir: "{{app}}"; Flags: ignoreversion
    Source: "ffmpeg\\*"; DestDir: "{{app}}\\ffmpeg"; Flags: ignoreversion recursesubdirs createallsubdirs
    Source: "images\\*"; DestDir: "{{app}}\\images"; Flags: ignoreversion recursesubdirs createallsubdirs
    Source: "fonts\\*"; DestDir: "{{app}}\\fonts"; Flags: ignoreversion recursesubdirs createallsubdirs
    Source: "README.txt"; DestDir: "{{app}}"; Flags: ignoreversion isreadme
    Source: "LICENSE.txt"; DestDir: "{{app}}"; Flags: ignoreversion

    [Icons]
    ; Añadir IconFilename para asegurar que se use el icono personalizado
    Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; IconFilename: "{{app}}\\images\\icon.ico"
    Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
    Name: "{{commondesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon; IconFilename: "{{app}}\\images\\icon.ico"

    [Run]
    Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
    """


    
    with open(os.path.join(installer_dir, 'Capybara_Downloader.iss'), 'w', encoding='utf-8') as f:
        f.write(inno_script)
    
    print("\n✓ Proceso de build completado con éxito!")
    print(f"Todos los archivos necesarios están en: {installer_dir}")
    print("El ejecutable se encuentra en:", exe_path)
    print("\nAhora puedes usar Inno Setup para crear el instalador con el script generado:")
    print(f"{os.path.join(installer_dir, 'Capybara_Downloader.iss')}")
    print("\nAsegúrate de que los archivos de FFmpeg estén presentes en la carpeta ffmpeg.")

if __name__ == "__main__":
    main()