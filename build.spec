# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Inclui a pasta assets completa
        ('data', 'data'),      # Inclui a pasta data
    ],
    hiddenimports=[
        'code.game',
        'code.menu',
        'code.options',
        'code.player',
        'code.bullet',
        'code.enemy',
        'code.boss',
        'code.boss_bullet',
        'code.asteroid',
        'code.database',
        'code.game_over',
        'code.settings',
        'code.powerup',
        'code.enemy_bullet',
        'code.missile'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SpaceShooter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para não mostrar console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icon.ico'  # Se você tiver um ícone
)

def get_asset_path(relative_path):
    try:
        # Obtém o caminho base do executável
        if getattr(sys, 'frozen', False):
            # Se estiver rodando como executável
            base_path = sys._MEIPASS
        else:
            # Se estiver rodando como script
            base_path = os.path.dirname(os.path.dirname(__file__))
            
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Erro ao localizar asset: {e}")
        return relative_path 