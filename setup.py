from setuptools import setup, find_packages

setup(
    name="manga-text-detection",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pywin32",
        "opencv-python",
        "torch<2.6.0",  # https://dev-discuss.pytorch.org/t/bc-breaking-change-torch-load-is-being-flipped-to-use-weights-only-true-by-default-in-the-nightlies-after-137602/2573
        "torchvision",
        "numpy",
        "pyclipper",
        "shapely",
    ],
)
