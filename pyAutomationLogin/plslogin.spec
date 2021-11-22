# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['plslogin.py', 'login_by_selenium.py', 'click_window_login_page_test.py'],
             pathex=['C:\\Users\\Administrator\\Documents\\pyAutomationLogin'],
             binaries=[],
             datas=[
             ('main.ui', '.'),
             ('id_pw.json', '.'),
             (r'.\dist\login_by_selenium\login_by_selenium.exe', '.'),
             (r'D:\pythonDemo\driver\chromedriver_win32\chromedriver_75.0.3770.90.exe', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='plslogin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='plslogin')
