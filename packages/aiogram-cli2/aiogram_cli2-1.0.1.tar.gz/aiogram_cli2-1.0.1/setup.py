from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-16") as file:
    content = file.read()

with open("README.md", "w", encoding="utf-8") as file:
    file.write(content)

setup(
    name="aiogram_cli2",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "watchdog"
    ],
    url="https://github.com/sinofarmonovzfkrvjl/aiogram-cli",
    author="https://t.me/python_dev323",
    description="bu aiogram kutubxonasi uchun aiogram cli (command line tool)",
    entry_points={
        'console_scripts': [
            'aiogram-cli = aiogram_cli.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=content,
    long_description_content_type="text/markdown",
)
