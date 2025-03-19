from setuptools import setup, find_packages

setup(
    name="crawzy",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "trafilatura", "colorama", "tqdm"],
    entry_points={"console_scripts": ["crawzy = crawzy:main"]},
)
