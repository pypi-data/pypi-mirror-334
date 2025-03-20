from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')

setup(
    name="flask-startproject",
    version="0.2.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    py_modules=["flask_startproject"],
    entry_points={
        "console_scripts": [
            "flask-startproject=flask_startproject:main"
        ]
    },
)
