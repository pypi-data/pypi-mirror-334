from setuptools import setup, find_packages

setup(
    name="scripts_lot",  # Replace with your library's name
    version="0.9.0",  # Update version as needed
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package has
    ],
    author="tran_nigga",
    author_email="your-email@example.com",
    description="A brief description of your library",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/HamzaAhmad6292/lib",  # GitHub URL or project URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust if you're using a different license
        "Operating System :: OS Independent",
    ],
)
