import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.rst").read_text()

setup(
    name="IPythonClipboard",
    version="1.0b2",
    packages=["ipython_clipboard"],
    license="MIT",
    author="Carlos G. Trejo",
    author_email="carlos.guadarrama.trejo@gmail.com",
    url="https://github.com/CarlosGTrejo/ipython_extensions/tree/master/ipython_clipboard",
    description="An IPython extension to copy and/or pickle input/output lines or variables.",
    long_description=README,
    long_description_content_type="text/x-rst",
    keywords="ipython clipboard clip utility utilities tools copy paste",
    install_requires=['ipython', 'pyperclip'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
)
