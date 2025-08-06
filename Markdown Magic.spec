# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launch_markdown_magic.py'],
    pathex=[],
    binaries=[],
    datas=[('document_converter.py', '.'), ('batch_processor.py', '.'), ('image_processor.py', '.'), ('markdown_magic_gui.py', '.')],
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
    [],
    exclude_binaries=True,
    name='Markdown Magic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Markdown Magic',
)
app = BUNDLE(
    coll,
    name='Markdown Magic.app',
    icon='app_icon.icns',
    bundle_identifier=None,
)
