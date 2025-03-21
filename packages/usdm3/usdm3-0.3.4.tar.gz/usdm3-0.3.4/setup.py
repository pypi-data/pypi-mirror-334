import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_info = {}
with open("src/usdm3/__version__.py") as fp:
    exec(fp.read(), package_info)

setuptools.setup(
    name="usdm3",
    version=package_info["__package_version__"],
    author="D Iberson-Hurst",
    author_email="",
    description="A python package for using the CDISC TransCelerate USDM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pydantic",
        "beautifulsoup4",
        "pyyaml",
        "simple-error-log",
        "jsonschema",
        "beautifulsoup4",
        "simple-error-log",
        "jsonschema",
        "python-dotenv",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "usdm3": [
            "ct/cdisc/missing/missing_ct.yaml",
            "ct/cdisc/library_cache/library_cache.yaml",
            "ct/cdisc/config/ct_config.yaml",
            "rules/library/schema/usdm_v3.json",
        ]
    },
    tests_require=["pytest", "pytest-cov", "pytest-mock", "python-dotenv"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
