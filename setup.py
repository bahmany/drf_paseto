# setup.py

from setuptools import setup, find_packages

setup(
    name='drf-paseto-auth',
    version='0.1.0',
    description='PASETO Authentication for Django REST Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohammad Reza Bahmani',
    author_email='bahmanymb@gmail.com',
    url='https://github.com/bahmany/drf-paseto',  # Change this to your repository URL
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'djangorestframework>=3.11',
        'paseto>=1.5.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
