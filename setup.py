from setuptools import setup

APP=['main.py']

OPTIONS = {
    'iconfile':'images/icon.icns',
    'argv_emulation': True,
    'packages': ['pandas']
}

setup(
    app=APP,
    options={'py2app':OPTIONS},
    setup_requires=['py2app']
)