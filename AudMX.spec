# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AudMX.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\module\\volume_soket\\msvcp140d.dll', '.'), ('.\\module\\volume_soket\\ucrtbased.dll', '.'), ('.\\module\\volume_soket\\vcruntime140_1d.dll', '.'), ('.\\module\\volume_soket\\vcruntime140d.dll', '.'), ('.\\module\\volume_soket\\volumepid.exe', '.')],
    hiddenimports=['pycaw', 'Pillow', 'ctype', 'pywin32'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AudMX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\savva\\Documents\\github\\AudMx-win\\resurce\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AudMX',
)
