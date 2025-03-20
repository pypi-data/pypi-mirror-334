from setuptools import setup

setup(
    name="rokugu",
    version="0.0.1",
    description="An opinionated PyQt/PySide6 component library.",
    long_description="An opinionated PyQt/PySide6 component library offering a collection of aesthetically pleasing and highly accessible UI components.",
    readme="./README.md",
    license="MIT",
    license_files=["./LICENSE"],
    author="Santos Vilanculos",
    author_email="santosvilanculos@yahoo.com",
    url="http://github.com/SantosVilanculos/rokugu",
    package_dir={"": "src"},
    python_requires=">=3.12",
    requires=["setuptools", "wheel"],
    install_requires=[
        "pendulum",
        "pillow",
        "psutil",
        "PySide6",
    ],
)
