# 🌟 Capybara Downloader 🌟

<div align="center">
  <img src="images/logo.png" alt="Capybara Downloader Logo" width="200"/>
  
  <h3>Un downloader de YouTube potente, rápido y amigable</h3>

  [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
  [![yt-dlp](https://img.shields.io/badge/yt--dlp-Latest-red.svg)](https://github.com/yt-dlp/yt-dlp)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Índice

- [✨ Características](#-características)
- [🖥️ Capturas de pantalla](#️-capturas-de-pantalla)
- [🔧 Instalación](#-instalación)
- [🚀 Uso](#-uso)
- [📚 Opciones de calidad](#-opciones-de-calidad)
- [🔍 Requisitos](#-requisitos)
- [💾 Compilación](#-compilación)
- [📝 Notas](#-notas)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

## ✨ Características

- 🎥 **Descarga vídeos de YouTube** en diversas calidades
- 🎯 **Selección de calidad intuitiva** desde 144p hasta 8K
- 🎧 **Opción de sólo audio** (MP3/M4A)
- 📂 **Selección de directorio** de salida personalizable
- 📋 **Cola de descargas** para procesar múltiples vídeos
- 📊 **Barra de progreso** en tiempo real
- 🏃 **Interfaz rápida y ligera** con PyQt5
- 🔔 **Notificaciones de estado** detalladas
- 🎨 **Tema oscuro** para reducir la fatiga visual
- 🌐 **Basado en yt-dlp** para máxima compatibilidad

## 🖥️ Capturas de pantalla

<div align="center">
  <img src="docs/screenshots/main_screen.png" alt="Pantalla principal" width="600"/>
  <p><i>Pantalla principal de Capybara Downloader</i></p>
  
  <img src="docs/screenshots/quality_selection.png" alt="Selección de calidad" width="600"/>
  <p><i>Selección de calidad de video</i></p>
</div>

## 🔧 Instalación

### Opción 1: Descarga el ejecutable precompilado

1. Ve a la sección [Releases](https://github.com/tu-usuario/capybara-downloader/releases)
2. Descarga la última versión para tu sistema operativo
3. Extrae el archivo zip
4. Ejecuta `Capybara_Downloader.exe`

### Opción 2: Instalación desde el código fuente

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/capybara-downloader.git
cd capybara-downloader

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 🚀 Uso

### Paso 1: Inicia la aplicación
Abre Capybara Downloader haciendo doble clic en el ejecutable o ejecutando `python main.py`.

### Paso 2: Pega la URL del video
Copia la URL del video de YouTube que deseas descargar y pégala en el campo de texto.

### Paso 3: Selecciona la calidad
- Haz clic en **"Seleccionar calidad"** para elegir entre varias opciones de resolución
- O haz clic en **"Agregar a lista"** para usar la mejor calidad disponible automáticamente

### Paso 4: Configura el directorio de salida (opcional)
Haz clic en **"Buscar"** junto a "Guardado en:" para seleccionar dónde se guardarán tus videos.

### Paso 5: Inicia la descarga
Haz clic en **"Descargar todo"** para comenzar a descargar todos los videos en la cola.

### Paso 6: ¡Disfruta tus videos!
Los videos descargados estarán disponibles en la carpeta seleccionada.

## 📚 Opciones de calidad

Capybara Downloader ofrece una amplia gama de opciones de calidad:

| Calidad | Resolución | Descripción |
|---------|------------|-------------|
| **Mejor calidad** | Automática | Obtiene la mejor calidad disponible para el video |
| **144p** | 256x144 | Muy baja calidad, útil para conexiones extremadamente lentas |
| **240p** | 426x240 | Baja calidad, ideal para ahorrar datos |
| **360p** | 640x360 | Calidad media-baja, buena para dispositivos antiguos |
| **480p** | 854x480 | Calidad estándar/DVD, equilibrio de calidad y tamaño |
| **720p** | 1280x720 | HD, buena calidad para la mayoría de usos |
| **1080p** | 1920x1080 | Full HD, alta calidad para pantallas grandes |
| **1440p** | 2560x1440 | 2K/QHD, muy alta calidad |
| **2160p** | 3840x2160 | 4K/UHD, calidad ultra alta para pantallas 4K |
| **4320p** | 7680x4320 | 8K, calidad máxima (pocos videos disponibles) |
| **Solo audio (MP3)** | - | Extrae solo la pista de audio en formato MP3 |
| **Solo audio (M4A)** | - | Extrae solo la pista de audio en formato M4A |

## 🔍 Requisitos

- **Python 3.7+**
- **FFmpeg** (incluido en la versión precompilada)
- **Dependencias Python**:
  - PyQt5
  - yt-dlp

Para instalar todas las dependencias:
```bash
pip install PyQt5 yt-dlp
```

## 💾 Compilación

Si deseas compilar tu propia versión ejecutable:

1. Asegúrate de tener todas las dependencias instaladas
2. Instala PyInstaller:
   ```bash
   pip install pyinstaller
   ```
3. Compila el ejecutable:
   ```bash
   python build.py
   ```
4. El ejecutable se creará en la carpeta `dist`

## 📝 Notas

- **FFmpeg es necesario** para la conversión de formato y fusión de audio/video. Asegúrate de que esté instalado en tu sistema o en la carpeta `ffmpeg` junto al ejecutable.
- **Para la mejor experiencia**, usa Python 3.8 o superior.
- **Las descargas de YouTube** están sujetas a los términos y condiciones de YouTube. Esta herramienta está destinada para uso personal y educativo.

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si quieres mejorar Capybara Downloader:

1. Haz fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add amazing feature'`)
4. Sube tu rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

