import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="itxtools", ## 소문자 영단어
    version="0.0.1", ##
    author="WooSeok Park", ## ex) Sunkyeong Lee
    author_email="ws0601@naver.com", ##
    description="preProcess for hyosungitx", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pws0601/itxtools", ##
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
