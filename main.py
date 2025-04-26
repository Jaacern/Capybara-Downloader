import os
import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, 
                    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QProgressBar, 
                            QFileDialog, QListWidget, QListWidgetItem, QDialog,
                            QTableWidget, QTableWidgetItem, QHeaderView, QComboBox)
from PyQt5.QtGui import QIcon, QPixmap, QMovie, QFont, QFontDatabase, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject, QThread, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import QRect
import yt_dlp

# Importar correctamente el archivo de recursos
try:
    import resources_rc
except ImportError:
    print("Error al importar resources_rc.py. Verifica que se haya compilado correctamente.")
    sys.exit(1)

# Nuevos colores según los requisitos
color_primary = "#d79c2b"     # Dorado - Botones principales
color_hover = "#f6bb8d"       # Melocotón claro - Hover states
color_text_dark = "#6f5015"   # Marrón oscuro - Texto principal
color_secondary = "#ab8258"   # Marrón medio - Elementos secundarios
color_background = "#d2c4a8"  # Beige - Fondo
color_border = "#525347"      # Gris verdoso - Bordes

# Colores adicionales para estados especiales
color_accent = "#d79c2b"      # Mismo que primary para acentos
color_text_light = "#ffffff"  # Blanco para texto sobre fondos oscuros
color_warning = "#f6bb8d"     # Usar melocotón claro para advertencias
color_warning_hover = "#f8c9a3"  # Versión más clara para hover
color_warning_pressed = "#e5a87a"  # Versión más oscura para pressed
color_secondary_hover = "#b99168"  # Versión más clara del secundario
color_secondary_pressed = "#9d7348"  # Versión más oscura del secundario
color_dark = "#6f5015"        # Usar el marrón oscuro como color dark


class QualityOptionsDialog(QDialog):
    format_selected = pyqtSignal(str, str)  # Señal para el ID de formato seleccionado y la URL
    
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Opciones de Calidad Disponibles")
        self.setMinimumSize(500, 350)
        self.url = url
        
        # Configurar interfaz
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título con fuente personalizada
        title_label = QLabel("Selecciona la calidad de descarga:")
        title_font = QFont("Levenim MT Bold", 16)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"font-weight: bold; color: {color_text_dark};")
        layout.addWidget(title_label)

        # Descripción
        desc_label = QLabel("Elige una de las siguientes opciones de calidad para tu descarga:")
        desc_font = QFont("Levenim MT", 12)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet(f"color: {color_text_dark};")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Espacio
        layout.addSpacing(10)
        
        # Combo para opciones predefinidas
        preset_layout = QVBoxLayout()
        
        self.preset_combo = QComboBox()
        # Cambio en la opción de mejor calidad para asegurar la máxima resolución disponible
        self.preset_combo.addItem("Mejor calidad disponible (automático)", "bestvideo+bestaudio/best")
        # Opciones de calidad específicas
        self.preset_combo.addItem("144p - Muy baja calidad", "bestvideo[height<=144][ext=mp4]+bestaudio[ext=m4a]/best[height<=144][ext=mp4]")
        self.preset_combo.addItem("240p - Baja calidad", "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[height<=240][ext=mp4]")
        self.preset_combo.addItem("360p - Calidad media-baja", "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]")
        self.preset_combo.addItem("480p - Calidad estándar/DVD", "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]")
        self.preset_combo.addItem("720p - HD", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]")
        self.preset_combo.addItem("1080p - Full HD", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]")
        self.preset_combo.addItem("1440p - 2K/QHD", "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440][ext=mp4]")
        self.preset_combo.addItem("2160p - 4K/UHD", "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160][ext=mp4]")
        self.preset_combo.addItem("4320p - 8K", "bestvideo[height<=4320][ext=mp4]+bestaudio[ext=m4a]/best[height<=4320][ext=mp4]")
        # Opciones de solo audio
        self.preset_combo.addItem("Solo audio (MP3)", "bestaudio[ext=mp3]")
        self.preset_combo.addItem("Solo audio (M4A)", "bestaudio[ext=m4a]")
        
        combo_font = QFont("Levenim MT", 14)
        self.preset_combo.setFont(combo_font)
        self.preset_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {color_dark};
                color: {color_text_light};
                border: 1px solid {color_border};
                border-radius: 5px;
                padding: 10px;
                min-width: 400px;
                margin: 10px 0;
            }}
            QComboBox:hover {{
                border: 1px solid {color_hover};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: {color_border};
                border-left-style: solid;
            }}
            QComboBox QAbstractItemView {{
                background-color: {color_dark};
                color: {color_text_light};
                selection-background-color: {color_primary};
                selection-color: #121212;
                padding: 8px;
            }}
        """)

        preset_layout.addWidget(self.preset_combo)
        layout.addLayout(preset_layout)

        # Información adicional
        info_label = QLabel("La resolución final dependerá de lo disponible en el video original. Si seleccionas una calidad más alta que la disponible, se descargará la mejor calidad disponible.")
        info_font = QFont("Levenim MT", 11)
        info_label.setFont(info_font)
        info_label.setStyleSheet(f"color: {color_text_dark}; font-style: italic;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Espacio flexible
        layout.addStretch()

        # Botones
        button_layout = QHBoxLayout()

        download_button = QPushButton("Aceptar")
        button_font = QFont("Levenim MT Bold", 14)
        download_button.setFont(button_font)
        download_button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 30px;
                background-color: {color_primary};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary};
            }}
        """)
        download_button.clicked.connect(self.download_selected)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setFont(button_font)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 30px;
                background-color: {color_secondary};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_secondary_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary_pressed};
            }}
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(download_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
                
        # Aplicar estilo general
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {color_background};
                color: {color_text_dark};
            }}
        """)

    def download_selected(self):
        # Usar el preset seleccionado
        preset_format = self.preset_combo.currentData()
        preset_text = self.preset_combo.currentText()
        # Emitir señal con formato y nombre legible
        self.format_selected.emit(preset_format, self.url)
        self.accept()


class DownloadWorker(QObject):
    progress = pyqtSignal(float)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    info = pyqtSignal(str)

    def __init__(self, url, output_dir, ffmpeg_path, format_id=None, format_name=None):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.ffmpeg_path = ffmpeg_path
        self.is_cancelled = False
        self.format_id = format_id
        self.format_name = format_name

    def cancel(self):
        self.is_cancelled = True
        self.info.emit("Descarga cancelada")

    def progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("Descarga cancelada por el usuario")
            
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress.emit(percent)
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                self.progress.emit(percent)
            
            # Actualizar información de descarga
            if 'downloaded_bytes' in d:
                downloaded_mb = d['downloaded_bytes'] / 1024 / 1024
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / 1024 / 1024
                    self.info.emit(f"Descargando: {downloaded_mb:.1f} MB | Velocidad: {speed_mb:.1f} MB/s")
                
        elif d['status'] == 'finished':
            self.info.emit(f"Descarga completada {self.url}")
            self.progress.emit(100)

    def run(self):
        try:
            # Verificar que FFmpeg exista
            ffmpeg_exe = os.path.join(self.ffmpeg_path, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_exe):
                self.info.emit(f"FFmpeg no encontrado en {ffmpeg_exe}. Buscando alternativas...")
                
                # Buscar en ubicaciones alternativas
                if getattr(sys, 'frozen', False):
                    # Si es un ejecutable compilado
                    base_path = os.path.dirname(sys.executable)
                else:
                    # Si es el script Python normal
                    base_path = os.path.abspath(os.path.dirname(__file__))
                
                possible_paths = [
                    os.path.join(base_path, 'ffmpeg', 'ffmpeg.exe'),
                    os.path.join(base_path, 'ffmpeg.exe'),
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        self.ffmpeg_path = os.path.dirname(path) if os.path.dirname(path) else base_path
                        self.info.emit(f"FFmpeg encontrado en {path}")
                        break
            
            # Configurar opciones yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(self.output_dir, '%(title).200s.%(ext)s'),
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self.progress_hook],
                'noplaylist': True
            }
            
            # Si se especificó un formato, usarlo
            if self.format_id:
                # Independientemente del formato, asegurar que se use MP4 como contenedor final cuando sea posible
                ydl_opts['format'] = self.format_id
                ydl_opts['merge_output_format'] = 'mp4'
                
                # Para la mejor calidad, asegurarse de no imponer restricciones innecesarias
                if "bestvideo+bestaudio" in self.format_id:
                    # Garantizar que no se restrinja el formato de salida para la mejor calidad
                    ydl_opts['format'] = self.format_id
                elif self.format_id.startswith("best") or "[" in self.format_id:
                    # Es un formato compuesto o una expresión con restricciones
                    ydl_opts['format'] = self.format_id
                else:
                    # Es un ID de formato específico
                    ydl_opts['format'] = self.format_id
            else:
                # Formato predeterminado (mejor calidad)
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
            
            # Añadir post-procesador para convertir a MP3 si el formato lo específica
            if self.format_id and "bestaudio[ext=mp3]" in self.format_id:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            self.info.emit(f"Empezando descarga: {self.url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            if not self.is_cancelled:
                self.finished.emit()
        except Exception as e:
            self.error.emit(f"Error en descarga {self.url}: {str(e)}")


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Hacer el fondo transparente
        self.setFixedSize(600, 450)  # Aumentamos el tamaño para tener más espacio
        
        # Center on screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Creamos un layout con márgenes para evitar cortes en los bordes
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Añadir márgenes para evitar cortes
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Manejo más robusto de recursos
        logo_paths = [":/images/logo.png", "images/logo.png"]
        for path in logo_paths:
            try:
                logo_pixmap = QPixmap(path)
                if not logo_pixmap.isNull():
                    self.logo_label.setPixmap(logo_pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    break
            except Exception as e:
                continue
        
        # Contenedor para el título y "by Javier Cerna" - MODIFICADO
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)  # Cambiado a layout vertical
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(5)  # Reducido el espacio entre elementos
        
        # Título principal
        app_name = QLabel("Capybara Downloader")
        app_name_font = QFont("Levenim MT Bold", 22, QFont.Bold)
        app_name.setFont(app_name_font)
        app_name.setStyleSheet(f"color: {color_accent}; background-color: transparent;")
        app_name.setAlignment(Qt.AlignCenter)  # Centrado
        
        # Subtítulo "by Javier Cerna"
        by_label = QLabel("by Javier Cerna")
        by_font = QFont("Levenim MT", 10)
        by_label.setFont(by_font)
        by_label.setStyleSheet(f"color: white; background-color: transparent;")
        by_label.setAlignment(Qt.AlignCenter)  # Centrado
        
        # Añadir ambas etiquetas al contenedor vertical
        title_layout.addWidget(app_name)
        title_layout.addWidget(by_label)
        
        # Añadir espaciado vertical
        layout.addStretch()
        layout.addWidget(self.logo_label)
        layout.addSpacing(10)  # Espacio adicional entre el logo y el título
        layout.addWidget(title_container, 0, Qt.AlignCenter)  # Centrar horizontalmente
        layout.addStretch()

        self.setLayout(layout)
        
        # Eliminar el estilo de fondo y borde pero añadir un debug visual si es necesario
        self.setStyleSheet("""
            background-color: transparent;
            /*border: 1px solid red;*/  /* Descomentar para debug visual */
        """)
        
        # Configurar efecto de fade in
        self.setWindowOpacity(0.0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(1500)  # 1.5 segundos para el fade in
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Iniciar el fade in cuando el splash screen se muestre
        QTimer.singleShot(100, self.fade_in_animation.start)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capybara Downloader")
        
        # Manejo más robusto del icono
        icon_paths = [":/images/icon.png", "images/icon.png"]
        for path in icon_paths:
            try:
                icon = QIcon(path)
                if not icon.isNull():
                    self.setWindowIcon(icon)
                    break
            except Exception:
                continue
        
        self.setMinimumSize(800, 600)
        
        # Center on screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Default output directory
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Claude")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Localizar ffmpeg de manera robusta
        self.setup_ffmpeg_path()
        
        # Cargar las fuentes personalizadas
        self.load_custom_fonts()
        
        # Inicializar la interfaz de usuario
        self.setup_ui()
    
    def load_custom_fonts(self):
        """Carga las fuentes personalizadas desde los archivos en la carpeta fonts"""
        # Determinar ruta base según si es ejecutable compilado o script
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        
        # Rutas relativas a la aplicación
        font_paths = [
            os.path.join(base_path, 'fonts', 'levenim-mt-bold.ttf'),
            os.path.join(base_path, 'fonts', 'levenim-mt.ttf')
        ]
        
        fonts_loaded = False
        
        for font_path in font_paths:
            print(f"Intentando cargar fuente desde: {font_path}")
            if os.path.exists(font_path):
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id >= 0:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"Fuente cargada con éxito. Familia: {font_families}")
                    fonts_loaded = True
                else:
                    print(f"Error al cargar la fuente: {font_path}")
            else:
                print(f"Archivo de fuente no encontrado: {font_path}")
        
        # Si no se pudieron cargar las fuentes, usar alternativas del sistema
        if not fonts_loaded:
            print("No se pudieron cargar las fuentes personalizadas. Usando fuentes alternativas.")
            # Definir fuentes alternativas
            self.title_font_name = "Arial"
            self.text_font_name = "Arial"
            print(f"Usando fuentes alternativas: {self.title_font_name} y {self.text_font_name}")
        else:
            self.title_font_name = "Levenim MT Bold"
            self.text_font_name = "Levenim MT"
            print(f"Usando fuentes personalizadas: {self.title_font_name} y {self.text_font_name}")
                
        # Mostrar todas las familias de fuentes disponibles
        print("Familias de fuentes disponibles:")
        # Crear una instancia de QFontDatabase para llamar a families()
        font_db = QFontDatabase()
        available_families = font_db.families()
        for i, family in enumerate(available_families):
            print(f"{i+1}. {family}")

        
    def setup_ffmpeg_path(self):
        # Determinar la ruta base según si es ejecutable compilado o script
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        
        # Lista de posibles ubicaciones de FFmpeg
        possible_paths = [
            os.path.join(base_path, 'ffmpeg'),
            base_path,
            os.path.join(base_path, 'dist', 'ffmpeg'),
            os.path.dirname(base_path)
        ]
        
        self.ffmpeg_path = None
        
        # Buscar ffmpeg.exe en las ubicaciones posibles
        for path in possible_paths:
            ffmpeg_exe = os.path.join(path, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_exe):
                self.ffmpeg_path = path
                print(f"FFmpeg encontrado en {ffmpeg_exe}")
                break
        
        # Si no se encuentra en ninguna ruta específica, usar el directorio base
        if not self.ffmpeg_path:
            print("FFmpeg no encontrado en rutas específicas. Usando directorio base.")
            self.ffmpeg_path = base_path
    
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        logo_label = QLabel()
        logo_paths = [":/images/logo.png", "images/logo.png"]
        for path in logo_paths:
            try:
                logo_pixmap = QPixmap(path)
                if not logo_pixmap.isNull():
                    logo_label.setPixmap(logo_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    break
            except Exception:
                continue
        
      # Layout para el título y el subtítulo (horizontal)
        title_container = QHBoxLayout()
        title_container.setSpacing(5)  # Espacio entre el título y el subtítulo
        title_container.setContentsMargins(0, 0, 0, 0)
        title_container.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Alineación a la izquierda

        # Título principal
        title_label = QLabel("Capybara Downloader")
        title_font = QFont(self.title_font_name, 25, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"font-weight: bold; color: {color_accent};")

        # Subtítulo "by Javier Cerna"
        subtitle_label = QLabel("by Javier Cerna")
        subtitle_font = QFont(self.text_font_name, 10)  # Tamaño más visible
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: white;")
        subtitle_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)

        # Añadimos las etiquetas al contenedor
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)

        # Contenedor para mantenerlos juntos
        title_widget = QWidget()
        title_widget.setLayout(title_container)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_widget)
        header_layout.addStretch()

        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("YouTube URL:")
        url_font = QFont("Levenim MT", 14)
        url_label.setFont(url_font)
        url_label.setStyleSheet(f"color: {color_text_dark};")

        self.url_input = QLineEdit()
        input_font = QFont("Levenim MT", 12)
        self.url_input.setFont(input_font)
        self.url_input.setPlaceholderText("Pega tu link de youtube...")
        self.url_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px;
                border-radius: 5px;
                background-color: {color_dark};
                color: {color_text_light};
                border: 1px solid {color_border};
            }}
            QLineEdit:focus {{
                border: 2px solid {color_accent};
            }}
        """)

        add_button = QPushButton("Agregar a lista")
        button_font = QFont("Levenim MT Bold", 12)
        add_button.setFont(button_font)
        add_button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px 20px;
                background-color: {color_primary};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary};
            }}
        """)
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.add_url_to_queue)

        
        # Botón para seleccionar calidad
        quality_button = QPushButton("Seleccionar calidad")
        quality_button.setFont(button_font)
        quality_button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px 20px;
                background-color: {color_accent};
                color: {color_text_dark};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary};
            }}
        """)
        quality_button.setCursor(Qt.PointingHandCursor)
        quality_button.clicked.connect(self.show_quality_options)

        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(quality_button)
        url_layout.addWidget(add_button)

        # Output directory selection
        output_layout = QHBoxLayout()
        output_label = QLabel("Guardado en:")
        output_label.setFont(url_font)
        output_label.setStyleSheet(f"color: {color_text_dark};")

        self.output_display = QLineEdit(self.output_dir)
        self.output_display.setFont(input_font)
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px;
                border-radius: 5px;
                background-color: {color_dark};
                color: {color_text_light};
                border: 1px solid {color_border};
            }}
        """)

        browse_button = QPushButton("Buscar")
        browse_button.setFont(button_font)
        browse_button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px 20px;
                background-color: {color_border};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary};
            }}
        """)
        browse_button.setCursor(Qt.PointingHandCursor)
        browse_button.clicked.connect(self.browse_output_dir)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_display)
        output_layout.addWidget(browse_button)

        # Queue
        queue_label = QLabel("Descargar!:")
        queue_label.setFont(url_font)
        queue_label.setStyleSheet(f"color: {color_text_dark};")

        self.queue_list = QListWidget()
        list_font = QFont("Levenim MT", 12)
        self.queue_list.setFont(list_font)
        self.queue_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {color_dark};
                border-radius: 5px;
                padding: 5px;
                color: {color_text_light};
                border: 1px solid {color_border};
            }}
            QListWidget::item {{
                padding: 5px;
                border-bottom: 1px solid {color_border};
            }}
            QListWidget::item:selected {{
                background-color: {color_primary};
                color: {color_text_light};
            }}
        """)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {color_border};
                border-radius: 5px;
                background-color: {color_dark};
                color: {color_text_light};
                height: 25px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                stop:0 {color_secondary}, stop:1 {color_accent});
                border-radius: 5px;
            }}
        """)

        # Status label
        self.status_label = QLabel("Listo!!!")
        status_font = QFont("Levenim MT", 12)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet(f"color: {color_text_dark}; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Action buttons
        button_layout = QHBoxLayout()

        action_font = QFont("Levenim MT Bold", 14)
        self.download_button = QPushButton("Descargar todo")
        self.download_button.setFont(action_font)
        self.download_button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 30px;
                background-color: {color_primary};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary};
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
        """)
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.start_downloads)

        # Nuevo botón de cancelar
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setFont(action_font)
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 30px;
                background-color: {color_warning};
                color: {color_text_dark};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_warning_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_warning_pressed};
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
        """)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.cancel_current_download)
        self.cancel_button.setEnabled(False)

        clear_button = QPushButton("Limpiar")
        clear_button.setFont(action_font)
        clear_button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 30px;
                background-color: {color_secondary};
                color: {color_text_light};
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_secondary_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_secondary_pressed};
            }}
        """)
        clear_button.setCursor(Qt.PointingHandCursor)
        clear_button.clicked.connect(self.clear_queue)

        button_layout.addStretch()
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()

        # Add everything to main layout
        main_layout.addWidget(header)
        main_layout.addLayout(url_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(queue_label)
        main_layout.addWidget(self.queue_list)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(button_layout)

        # Set the central widget
        self.setCentralWidget(main_widget)

        # Apply theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {color_background};
            }}
            QWidget {{
                background-color: {color_background};
                color: {color_text_dark};
            }}
        """)

        
        # Initialize download queue and format options
        self.download_queue = []
        self.format_options = {}  # Para guardar opciones de formato por URL
        self.format_names = {}   # Para guardar nombres legibles de los formatos
        self.current_download = None
        self.download_thread = None
        self.worker = None
    
    def show_quality_options(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("¡Ingresa una URL primero!")
            return
        
        # Mostrar diálogo simplificado de opciones de calidad
        dialog = QualityOptionsDialog(url, self)
        dialog.format_selected.connect(self.add_url_with_format)
        dialog.exec_()
        
    def add_url_with_format(self, format_id, url):
        # Guardar formato seleccionado para esta URL
        self.format_options[url] = format_id
        
        # Determinar nombre legible para el formato
        format_name = self.get_format_display_name(format_id)
        self.format_names[url] = format_name
        
        # Añadir a la lista con formato
        self.download_queue.append(url)
        self.queue_list.addItem(f"{url} ({format_name})")
        self.url_input.clear()
        self.status_label.setText(f"Agregado {url} con calidad {format_name}")
    
    def get_format_display_name(self, format_id):
        """Convierte el ID del formato en un nombre legible"""
        if "height<=144" in format_id:
            return "144p - Muy baja calidad"
        elif "height<=240" in format_id:
            return "240p - Baja calidad"
        elif "height<=360" in format_id:
            return "360p - Calidad media-baja"
        elif "height<=480" in format_id:
            return "480p - Calidad estándar/DVD"
        elif "height<=720" in format_id:
            return "720p - HD"
        elif "height<=1080" in format_id:
            return "1080p - Full HD"
        elif "height<=1440" in format_id:
            return "1440p - 2K/QHD"
        elif "height<=2160" in format_id:
            return "2160p - 4K/UHD"
        elif "height<=4320" in format_id:
            return "4320p - 8K"
        elif "bestaudio[ext=mp3]" in format_id:
            return "Solo audio (MP3)"
        elif "bestaudio[ext=m4a]" in format_id:
            return "Solo audio (M4A)"
        elif "bestvideo+bestaudio" in format_id or format_id == "best":
            return "Mejor calidad disponible"
        else:
            return format_id
        
    def add_url_to_queue(self):
        url = self.url_input.text().strip()
        if url:
            self.download_queue.append(url)
            # Por defecto, usamos la mejor calidad disponible
            self.format_options[url] = "bestvideo+bestaudio/best"
            self.format_names[url] = "Mejor calidad disponible"
            self.queue_list.addItem(f"{url} (Mejor calidad disponible)")
            self.url_input.clear()
            self.status_label.setText(f"Agregados Total: {len(self.download_queue)}")
    
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Seleciona salida", self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.output_display.setText(dir_path)
    
    def start_downloads(self):
        if not self.download_queue or self.download_thread is not None:
            return
            
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.process_next_download()
    
    def cancel_current_download(self):
        if self.worker:
            self.worker.cancel()
            self.cancel_button.setEnabled(False)
            self.status_label.setText("Cancelando descarga...")
    
    def process_next_download(self):
        if not self.download_queue:
            self.status_label.setText("Tamos listeilor")
            self.download_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.progress_bar.setValue(0)
            return
            
        self.current_download = self.download_queue.pop(0)
        self.queue_list.takeItem(0)
        
        # Obtener formato seleccionado si existe
        format_id = None
        format_name = None
        if self.current_download in self.format_options:
            format_id = self.format_options[self.current_download]
            format_name = self.format_names.get(self.current_download, "Formato personalizado")
        
        # Create thread and worker
        self.download_thread = QThread()
        self.worker = DownloadWorker(
            url=self.current_download, 
            output_dir=self.output_dir, 
            ffmpeg_path=self.ffmpeg_path,
            format_id=format_id,
            format_name=format_name
        )
        self.worker.moveToThread(self.download_thread)
        
        # Connect signals
        self.download_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.info.connect(self.update_status)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.download_thread.quit)
        self.download_thread.finished.connect(self.download_thread.deleteLater)
        self.download_thread.finished.connect(self.worker.deleteLater)
        self.download_thread.finished.connect(self.on_download_finished)
        
        # Start the thread
        self.download_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(int(value))
    
    def update_status(self, message):
        self.status_label.setText(message)
    
    def handle_error(self, message):
        self.status_label.setText(message)
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.quit()
    
    def on_download_finished(self):
        self.download_thread = None
        self.worker = None
        self.process_next_download()
    
    def clear_queue(self):
        self.download_queue.clear()
        self.queue_list.clear()
        self.status_label.setText("limpiado")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create main window
    main_window = MainWindow()
    
    # Close splash and show main window after 2 seconds
    def finish_splash():
        splash.close()
        main_window.show()
    
    QTimer.singleShot(2000, finish_splash)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()