from setuptools import find_packages, setup

setup(
    name='anvil-uplink-windows',
    version='0.0.1',
    author='Owen Campbell',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    license='The MIT License (MIT)',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ],
    python_requires='>=3.6'
)
