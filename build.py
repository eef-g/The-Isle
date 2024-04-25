import os
import shutil
import PyInstaller.__main__

# Delete directories if they exist
for dir_path in ['build', 'dist']:
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)

PyInstaller.__main__.run([
    '--name=Doom',
    '--onefile',
    '--add-data=src/resources:resources',
    '-i src/resources/doom_clone.png'
    '--paths=./src',
    'src/main.py',
    '--noconfirm'
])
