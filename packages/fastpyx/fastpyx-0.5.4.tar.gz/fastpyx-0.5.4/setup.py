from setuptools import setup, Extension

setup(
    name="fastpyx",
    version="0.5.4",
    author="Mohammad Hasan Khoddami",
    author_email="mohammadh.khoddami@gmail.com",
    description="A fast memory optimization extension for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    ext_modules=[Extension("fastpyx", ["fastpyx/fastpyx.c"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
