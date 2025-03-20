from setuptools import setup, find_packages

setup(
    name="shell-style",  
    version="0.1.8",
    description="A terminal formatting library with 24-bit color support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TheOmniOnic",  
    packages=find_packages(where="."),
    package_dir={"": "."},
    include_package_data=True,
    install_requires=[],
    url="https://github.com/TheOmniOnic/shell-style",
    python_requires=">=3.12.0",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Terminals",
    ],
    entry_points={
        'console_scripts': [
            'shell-style = shell_style.__main__:main',  
        ],
    },
)