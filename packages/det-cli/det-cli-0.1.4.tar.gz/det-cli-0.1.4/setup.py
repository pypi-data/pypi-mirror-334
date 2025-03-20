from setuptools import setup, find_packages

setup(
    name="det-cli",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "det-register = det_cli.register:register_protocol",
            "det-update = det_cli.protocol_handler:handle_protocol",
        ]
    },
    author="shukangzhang",
    author_email="skzhang@nuaa.edu.cn",
    description="A package to register a custom protocol for Det ssh config.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myapp-ssh-config",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
)
