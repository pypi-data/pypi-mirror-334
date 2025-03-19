import os

GH_API_ELONA = "https://api.github.com/repos/vichmartins/ElonaPlusCGXDownload/releases/latest"
GH_API_CGX = "https://api.github.com/repos/JianmengYu/ElonaPlusCustom-GX/releases/latest"
ELONA_FILE_NAME = 'Elona.zip'
CGX_FILE_NAME = 'Custom-GX.zip'
EXE = 'elonapluscgx.exe'
SHORTCUT_NAME = 'ElonaPlusCustom-GX'
INSTALL_PATH = os.getenv('APPDATA')

import download
import extract  
import desktop  
import move  
import cleanup  
import start_menu

