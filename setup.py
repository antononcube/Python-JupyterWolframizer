import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JupyterWolframizer",
    version="0.0.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Custom Jupyter magics for interacting with Wolfram Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-JupyterWolframizer",
    packages=setuptools.find_packages(),
    install_requires=["wolframclient>=1.1.7",
                      "IPython>=8.15.0",
                      "pyperclip>=1.8.2"
                      ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["wolfram", "wolfram language", "wolfram client", "mathematica",
              "symbolic", "symbolic computation",
              "magics", "jupyter", "notebook"],
    package_data={},
    python_requires='>=3.7',
)
