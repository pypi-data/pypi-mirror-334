from setuptools import setup, find_packages

setup(
    name="basicApiModel",
    version="1.0.3",
    author="Clayton Melo",
    author_email="claytonsnt@hotmail.com",
    description="A simple API template to speed up development",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "basicApiModel-init=basicApiModel.app:app",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
