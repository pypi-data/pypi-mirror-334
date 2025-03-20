from setuptools import setup, find_packages

setup(
    name="autoroblox",
    version="1.1.0",
    author="AutoRoblox Project",
    author_email="contact.autoroblox@gmail.com",
    description="AutoRoblox is a library offering tools for automating Roblox gameplay.",
    long_description="AutoRoblox is a library offering tools for automating Roblox gameplay.",
    url="https://github.com/autoRobloxProject/AutoRoblox",
    packages=find_packages(),
    install_requires=[
        "pynput",
        "keyboard",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
