# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Milivoj\\Documents\\GitHub\\HT15_AI_Project_Group43'],
             binaries=None,
             datas=None,
             hiddenimports=['language_check'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='storyteller',
          debug=False,
          strip=None,
          upx=True,
          console=True )
