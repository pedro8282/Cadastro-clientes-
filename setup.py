import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter"]}

 
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Cadaastro de cliente",
    version="0.1",
    description="casdastro e relatorio de cliente !",
    options={"build_exe": build_exe_options},
    executables=[Executable("cadastro01.py", base=base)]
)