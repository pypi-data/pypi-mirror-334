import setuptools

with open("splinaltap/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="splinaltap",
    version="0.7.0",
    author="chris",
    author_email="chrisdreid@gmail.com",
    description="Keyframe interpolation and expression evaluation that goes to eleven!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisdreid/splinaltap",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "numpy": ["numpy>=1.20.0"],
        "visualize": ["matplotlib>=3.5.0", "numpy>=1.20.0"],
        "gpu": ["jax>=0.3.0", "jaxlib>=0.3.0", "cupy>=10.0.0"],
        "numba": ["numba>=0.55.0", "numpy>=1.20.0"],
        "all": ["numpy>=1.20.0", "matplotlib>=3.5.0", "jax>=0.3.0", "jaxlib>=0.3.0", 
                "cupy>=10.0.0", "numba>=0.55.0"],
    },
    entry_points={
        "console_scripts": [
            "splinaltap=splinaltap.cli:main",
        ],
    },
)