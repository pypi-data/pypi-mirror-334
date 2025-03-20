#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
import platform

# Leer README desde el directorio raíz usando ruta relativa
with open(os.path.join("..", "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Dependencias específicas de la plataforma
install_requires = [
    "psutil",  # Para información del sistema
]

# En Windows, agregar pyreadline3
if platform.system() == "Windows":
    install_requires.append("pyreadline3")

# Determinar dependencias condicionales
extras_require = {
    'win': ['python-magic-bin'],  # Para Windows
    'unix': ['python-magic'],      # Para Unix/Linux/Mac
}

# Crear enlace simbólico (o copia) temporal de qzx.py para incluirlo
import shutil
if not os.path.exists('qzx.py'):
    src = os.path.join('..', 'qzx.py')
    if os.path.exists(src):
        shutil.copy2(src, 'qzx.py')
        # Registrar para limpieza
        import atexit
        atexit.register(lambda: os.remove('qzx.py') if os.path.exists('qzx.py') else None)

setup(
    name="qzx",
    version="0.02.1",
    author="Alejandro Sánchez",
    author_email="alesangreat@gmail.com",
    description="QZX - Quick Zap Exchange - Command line tool for automating common tasks across platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alesanGreat/QZX-Quick-Zap-Exchange",
    packages=["Core", "Commands", "Commands.FileCommands", "Commands.SystemCommands"],
    py_modules=["qzx"],  # Ahora buscará qzx.py en la carpeta PyPi (la copia)
    package_dir={
        "": "..",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "qzx=qzx:main",  # Esto permitirá ejecutar 'qzx' en la terminal
        ],
    },
    include_package_data=True,
) 