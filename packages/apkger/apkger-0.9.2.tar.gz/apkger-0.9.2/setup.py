from setuptools import setup, find_packages
import os
import subprocess


# Handle git submodules: ECDICT
def initialize_submodules():
    if os.path.exists(".git"):
        try:
            subprocess.check_call([
                "git",
                "submodule",
                "update",
                "--init",
                "--recursive",
            ])
            print("Git submodules initialized successfully")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Warning: Failed to initialize git submodules: {e}")
            print("If using a source distribution, this is expected")


initialize_submodules()

setup(
    name="apkger",
    version="0.9.2",
    author="Yaoyao Hu",
    author_email="shady030314@gmail.com",
    description="自动化 Anki 英语单词牌组生成器",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yaoyhu/anki_packager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Text Processing :: Linguistic",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.9",
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "apkger=anki_packager.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "anki_packager": ["config/*", "dicts/*"],
    },
)
