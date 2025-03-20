from setuptools import setup, find_packages


setup(
    name='my_package_testo098',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # a python package used in the code like numpy or others is possible to include here
    author='Dany',
    author_email="dany19@gmail.com",  # your email
    description='A simple example private package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Y2nn/my_package_testo098',  # your GitHub URL of the package
    # The classifiers are not functional, they are for documentation, and will be listed on the PYPI page, once uploaded
    # It is conventional to include the Python versions supported in this release.
    # A complete list of classifiers is available at: PyPI classifiers list
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.8'
)
