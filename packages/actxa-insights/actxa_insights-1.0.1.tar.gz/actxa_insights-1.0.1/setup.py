from setuptools import setup, find_packages

setup(
    name="actxa_insights",
    version="1.0.1",
    packages=find_packages(),
    description="SDK Python package for Actxa Insights",
    author="Actxa Insights",
    author_email="hadriang.gunawan@inphosoft.com",
    # url="https://github.com/yourusername/my-package",
    python_requires=">=3.9",
    install_requires=["requests"],
)
