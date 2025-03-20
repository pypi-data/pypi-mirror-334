from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-16") as file:
    content = file.read()

with open("README.md", "w", encoding="utf-8") as file:
    file.write(content)

setup(
    name="youtube_downloader2",
    version="0.0.3",
    description="A package to download youtube videos and audio from youtube",
    author="Sino Farmonov",
    url="https://github.com/sinofarmonovzfkrvjl/youtube-downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["requests"],
    long_description=content,
    long_description_content_type="text/markdown",
)
