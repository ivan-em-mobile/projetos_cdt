# -*- mode: python ; coding: utf-8 -*-

import os
import streamlit
from PyInstaller.utils.hooks import copy_metadata, collect_submodules

# Coleta metadados essenciais
datas = copy_metadata('streamlit')
datas += copy_metadata('pandas')
datas += copy_metadata('altair')

# Inclui a pasta estática do Streamlit
streamlit_path = os.path.dirname(streamlit.__file__)
datas += [(os.path.join(streamlit_path, 'static'), 'streamlit/static')]

# Coleta todos os submódulos do Streamlit e Altair automaticamente
hidden_imports = collect_submodules('streamlit')
hidden_imports += collect_submodules('altair')
hidden_imports += [
    'pandas',
    'requests',
    'sqlite3',
    'json',
]

# Inclui os arquivos Python do projeto
datas += [
    ('app_web.py', '.'),
    ('services.py', '.'),
    ('database.py', '.'),
]

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SistemaFinanceiro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SistemaFinanceiro',
)