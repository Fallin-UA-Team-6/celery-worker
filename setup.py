from setuptools import setup, find_namespace_packages

setup(
    name='safety-ping',
    version='1',
    python_requires='>=3.8',
    author='Brian Donald, Tejash Desai',
    author_email='suuport@iamnotbrian.com',
    packages=find_namespace_packages(include=['backend']),
    long_description="implements safety-ping system for fall-in-ua hackathon",
    package_data={
    },
    install_requires=[
        "click",
        "Flask",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "Werkzeug",
        "pydantic",
        "kombu",
    ]
)