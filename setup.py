import setuptools

setuptools.setup(
    name="songs",
    version="0.1.0",
    url="https://github.com/",
    author="Mikel Tobar del Barrio",
    author_email="mtobar@uoc.edu",
    description="Creation of a songs dataset and analysis",
    #long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    package_data={'': ['data/data.zip']},
)
