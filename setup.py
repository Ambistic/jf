import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jf",
    version="0.0.1",
    author="Nathan Vinçon",
    author_email="nathan_v@hotmail.fr",
    description="A python toolbox for scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ambistic/jf/issues",
    project_urls={
        "Bug Tracker": "https://github.com/Ambistic/jf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['pandas', 'networkx', 'streamlit'],
    scripts=['bin/jf_watch']
)
