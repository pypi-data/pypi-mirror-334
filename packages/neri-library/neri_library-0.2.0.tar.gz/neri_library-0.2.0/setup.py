from setuptools import setup, find_packages

setup(
    name="neri_library",
    version="0.2.0",
    author="Guilherme Neri",
    author_email="gui.neriaz@gmail.com ",
    description="Neri Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NeriAzv/Neri-Library",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nr-find-imports=neri_library.cli:main",
            "nr_find_imports=neri_library.cli:main",
            "nr_find_import=neri_library.cli:main",
            "find_imports=neri_library.cli:main",
            "find_import=neri_library.cli:main",
            "nfi=neri_library.cli:main",
            "fi=neri_library.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'setuptools',
        'selenium'
    ],
    extras_require={
        "full": [
            'undetected-chromedriver',
            'webdriver-manager',
            'opencv-python',
            'pygetwindow',
            'pyscreeze',
            'pyautogui',
            'requests',
            'pymupdf',
            'Pillow',
            'psutil'
        ],
    },
)

