import setuptools

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Filter out comments and blank lines
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

version = {}
with open("pygformula/version.py") as fp:
    exec(fp.read(), version)

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='pygformula',
    version=version['__version__'],
    maintainer='Jing Li',
    maintainer_email='jing_li@hsph.harvard.edu',
    description='A python implementation of the parametric g-formula',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    python_requires='>=3.11'
)