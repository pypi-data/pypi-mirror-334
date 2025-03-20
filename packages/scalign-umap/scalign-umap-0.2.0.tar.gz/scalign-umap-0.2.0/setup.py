
import platform
from setuptools import setup

configuration = {
    "name": "scalign-umap",
    "version": "0.2.0",
    "description": 
        "fork from package umap-learn 0.5.8 for usage from scalign package. "
        "contains additional bug fixes",
    "license": "BSD",
    "packages": ["scalign_umap"],
    "python_requires": ">=3.6",
    "install_requires": [
        "numpy >= 1.23",
        "scipy >= 1.3.1",
        "scikit-learn >= 1.6",
        "numba >= 0.51.2",
        "pynndescent >= 0.5",
        "tqdm",
    ],
    "extras_require": {
        "parametric": [
            "tensorflow >= 2.1",
            "keras >= 3.0"
        ]
    },
    "ext_modules": [],
    "cmdclass": {},
    "data_files": (),
    "zip_safe": False,
}

setup(**configuration)
