# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('DateTimeWidget.py', '.'), ('HoroscopeWidget.py', '.'), ('Natura.mp4', '.'), ('last_file.txt', '.'), ('Samson.ttf', '.'), ('Update.py', '.'), ('WeatherWidget.py', '.'), ('icon.jpg', '.'), ('ohota.jpg', '.'), ('1.jpg', '.'), ('3.jpg', '.'), ('bul.jpg', '.'), ('clock.jpg', '.'), ('double.jpg', '.'), ('fish.jpg', '.'), ('graf 2.jpg', '.'), ('graf.jpg', '.'), ('koz.jpg', '.'), ('ledy.jpg', '.'), ('lion.jpg', '.'), ('o.png', '.'), ('oven.jpg', '.'), ('rak.jpg', '.'), ('s.png', '.'), ('scorp.jpg', '.'), ('ss.png', '.'), ('strel.jpg', '.'), ('water.jpg', '.'), ('record.txt', '.'), ('release_version.txt', '.'), ('requirements.txt', '.'), ('main.spec', '.')],
    hiddenimports=[],
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
    name='main',
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
    icon=['icon.ico'],
)
