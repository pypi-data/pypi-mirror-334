from setuptools import setup, find_packages
def load_readme() -> str:
    with open("README.md",encoding="utf-8_sig") as fin:
        return fin.read()
setup(
    name='Pix-Chan',
    version='1.0.1',
    keywords = "pixai",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    author='taka4602',
    author_email='taka4602@gmail.com',
    url='https://github.com/taka-4602/Pix-Chan',
    description='An API wrapper for the PixAI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "requests",
    ],
    python_requires='>=3.6',
)