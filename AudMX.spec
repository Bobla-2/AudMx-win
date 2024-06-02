# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AudMX.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\module\\theme\\B_sylete', '.'), ('.\\module\\theme\\W_sylete', '.'), ('.\\module\\theme\\iconTrayB.png', '.'), ('.\\module\\theme\\iconTrayW.png', '.'), ('.\\module\\volume_soket\\msvcp140d.dll', '.'), ('.\\module\\volume_soket\\ucrtbased.dll', '.'), ('.\\module\\volume_soket\\vcruntime140_1d.dll', '.'), ('.\\module\\volume_soket\\vcruntime140d.dll', '.'), ('.\\module\\volume_soket\\volumepid.exe', '.')],
    hiddenimports=['pycaw', 'Pillow', 'ctype', 'pywin32', 'PySide6'],
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
    name='AudMX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\savva\\Documents\\github\\AudMix\\icon.ico'],
)
