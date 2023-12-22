from cx_Freeze import setup, Executable

setup(
    name="NombreEjecutable",
    version="1.0",
    description="Descripción del programa",
    executables=[Executable("Franklin.py")],
)