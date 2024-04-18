from setuptools import setup

setup(
    name="meni",
    version="0.1.0",
    description="Software to manage a library of 3d files (stl)",
    url="https://github.com/diesphink/meni",
    author="Diego Pereyra",
    author_email="diego@diegopereyra.com",
    license="BSD 3-clause",
    packages=["meni", "meni.ui", "meni.ui.docks", "meni.ui.menus", "meni.ui.toolbars", "meni.ui.windows", "meni.model"],
    install_requires=["pyside6", "qt-material", "jsonpickle", "numpy-stl", "matplotlib", "qtawesome", "vtkplotlib"],
    script_name="main.py",
    package_data={"meni": ["logo.svg"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
