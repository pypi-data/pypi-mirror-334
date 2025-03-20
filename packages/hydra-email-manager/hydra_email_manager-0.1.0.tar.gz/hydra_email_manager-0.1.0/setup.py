from setuptools import setup, find_packages

setup(
    name='hydra_email_manager',
    version='0.1.0',
    author='Ronaldo Peregrina',
    author_email='ronaldo@example.com',
    description='A Python package for managing email sending and receiving using Microsoft Graph API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/hydra_email_manager',  # Replace with your actual repository URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
        'msal',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your actual license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)