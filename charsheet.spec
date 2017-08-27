# -*- mode: python -*-
import os
from kivy.deps import sdl2, glew
block_cipher = None


my_hidden_modules = []

a = Analysis(['charsheet.py'],
             pathex=['D:\\Programming\\CharSheet'],
             binaries=None,
             datas=my_hidden_modules,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
			 
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='CharSheet',
          debug=True,
          strip=False,
          upx=True,
          console=True)
		  
coll = COLLECT(exe,Tree('D:\\Programming\\CharSheet'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='CharSheet')