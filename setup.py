from setuptools import setup, find_packages

setup(
    name="manga-text-detection",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pywin32",
        "opencv-python",
        "torch",
        "torchvision",
        "numpy",
        "pyclipper",
        "shapely",
    ],
)
