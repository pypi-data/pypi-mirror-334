from setuptools import setup, find_packages

setup(
    name="django-crudgen",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.0",
    ],
    author="Mohammad Hasan Khoddami",
    author_email="mohammadh.khoddami@gmail.com",
    description="A simple package to generate CRUD views for Django models.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohammadkhoddami/django-crudgen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
