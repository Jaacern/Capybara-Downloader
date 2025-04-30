# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('C:\\Users\\javie\\OneDrive\\Desktop\\PROGRAMA\\Capybara-Downloader\\ffmpeg\\ffmpeg.exe', 'ffmpeg'), ('C:\\Users\\javie\\OneDrive\\Desktop\\PROGRAMA\\Capybara-Downloader\\ffmpeg\\ffprobe.exe', 'ffmpeg'), ('C:\\Users\\javie\\OneDrive\\Desktop\\PROGRAMA\\Capybara-Downloader\\ffmpeg\\ffplay.exe', 'ffmpeg')],
    datas=[('images', 'images'), ('resources_rc.py', '.'), ('images\\logo.png', 'images'), ('images\\icon.png', 'images'), ('images\\loading.gif', 'images'), ('images\\icon.ico', 'images'), ('fonts', 'fonts')],
    hiddenimports=['yt_dlp', 'yt_dlp.extractor', 'yt_dlp.extractor.youtube', 'yt_dlp.extractor.common', 'yt_dlp.downloader', 'yt_dlp.downloader.fragment', 'yt_dlp.options', 'yt_dlp.postprocessor', 'yt_dlp.postprocessor.ffmpeg', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Capybara_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\icon.ico'],
)
