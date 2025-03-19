from setuptools import setup, find_packages

setup(
    name="TestHub",
    version="0.1.9",
    author="Dearygt.",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
    include_package_data=True,
)
