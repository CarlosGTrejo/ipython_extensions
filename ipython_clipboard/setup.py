from setuptools import setup

setup(
    name="IPythonClipboard",
    version="1.0b1",
    packages=["ipython_clipboard"],
    license="MIT",
    author="Carlos G. Trejo",
    author_email="carlos.guadarrama.trejo@gmail.com",
    url="https://github.com/CarlosGTrejo/ipython_extensions",
    description="An IPython extension to copy and/or pickle line outputs or variables.",
    long_description=open("README.rst").read(),
    keywords="ipython clipboard clip utility utilities tools copy paste",
    install_requires=['ipython', 'pyperclip'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
)
