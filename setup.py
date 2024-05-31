import versioneer
from setuptools import find_packages, setup

client_requires = open("requirements-client.txt").read().strip().split("\n")
# strip the first line since setup.py will not recognize '-r requirements-client.txt'
install_requires = (
    open("requirements.txt").read().strip().split("\n")[1:] + client_requires
)
dev_requires = open("requirements-dev.txt").read().strip().split("\n")

setup(
    # Package metadata
    name="prefect",
    description="Workflow orchestration and management.",
    author="Prefect Technologies, Inc.",
    author_email="help@prefect.io",
    url="https://www.prefect.io",
    project_urls={
        "Changelog": "https://github.com/PrefectHQ/prefect/blob/main/RELEASE-NOTES.md",
        "Documentation": "https://docs.prefect.io",
        "Source": "https://github.com/PrefectHQ/prefect",
        "Tracker": "https://github.com/PrefectHQ/prefect/issues",
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # Versioning
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    # Package setup
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    # CLI
    entry_points={
        "console_scripts": ["prefect=prefect.cli:app"],
    },
    # Requirements
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        # Infrastructure extras
        "aws": "prefect-aws",
        "azure": "prefect-azure",
        "gcp": "prefect-gcp",
        "docker": "prefect-docker",
        "kubernetes": "prefect-kubernetes",
        "shell": "prefect-shell",
        # Distributed task execution extras
        "dask": "prefect-dask",
        "ray": "prefect-ray",
        # Version control extras
        "bitbucket": "prefect-bitbucket",
        "github": "prefect-github",
        "gitlab": "prefect-gitlab",
        # Database extras
        "databricks": "prefect-databricks",
        "dbt": "prefect-dbt",
        "snowflake": "prefect-snowflake",
        "sqlalchemy": "prefect-sqlalchemy",
        # Monitoring extras
        "email": "prefect-email",
        "slack": "prefect-slack",
    },
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
)
