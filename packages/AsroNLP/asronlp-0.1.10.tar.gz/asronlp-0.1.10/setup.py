from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='AsroNLP',  # Name of your package
    version='0.1.10',  # Version number
    author='Asro',  # Your name or your organization's name
    author_email='asro@raharja.info',  # Your contact email
    description='Alat NLP sederhana untuk memproses dan menganalisis teks dalam bahasa Indonesia.',  # Short description
    long_description=long_description,  # Long description read from the README file
    long_description_content_type='text/markdown',  # Type of the long description
    url='https://github.com/asroharun6/AsroNLP',  # Link to your project's repository or website
    packages=find_packages(),  # Automatically find all packages and sub-packages
    include_package_data=True,  # Include all data files specified in MANIFEST.in
    package_data={
        'asro_nlp': ['data/*.txt', 'data/*.xlsx'],  # Include specific types of files from your package
    },
    install_requires=[
        'pandas>=1.1.5',  # Specify the dependencies and their versions
        'openpyxl>=3.0.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development status of your package
        'Intended Audience :: Developers',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Minimum version requirement of Python
)
