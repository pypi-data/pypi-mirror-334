import setuptools
import codecs
import os.path


setuptools.setup(
    name="turby",
    version="0.0.1dev0",
    author="Zachary R. Claytor",
    author_email="zclaytor@stsci.edu",
    description="Optical Turbulence Profiling with Machine Learning",
    license="MIT",
    python_requires='>=3',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)
