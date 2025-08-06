from setuptools import setup

APP = ['launch_markdown_magic.py']
DATA_FILES = [
    'document_converter.py',
    'batch_processor.py', 
    'image_processor.py',
    'markdown_magic_gui.py'
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': 'Markdown Magic',
        'CFBundleDisplayName': 'Markdown Magic',
        'CFBundleIdentifier': 'com.yourname.markdownmagic',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2025',
    },
    # Only include the essential packages
    'packages': ['PyQt5'],
    'includes': ['sip'],
    # Exclude unnecessary packages to reduce build issues
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas', 'jupyter']
}

setup(
    name='Markdown Magic',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
