from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="monitorpeek",
    version="2.1.0",
    author="John",
    author_email="zorat@abv.bg",
    description="A lightweight secondary monitor viewer with cursor tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zorat111/MonitorPeek",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Desktop Environment :: Window Managers",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyQt6>=6.4.0",
        "opencv-python>=4.7.0",
        "numpy>=1.24.0",
        "mss>=9.0.1",
        "pywin32>=305"
    ],
    package_data={
        "monitorpeek": ["final_icon.ico"],
    },
    entry_points={
        "console_scripts": [
            "monitorpeek=monitorpeek.main:main",
        ],
    },
) 