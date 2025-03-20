from setuptools import setup, find_packages

setup(
    name="youtube_downloader2",
    version="0.0.2",
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
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
