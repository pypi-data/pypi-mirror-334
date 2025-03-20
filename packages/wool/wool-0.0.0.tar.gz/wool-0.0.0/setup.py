import setuptools


entrypoint = "workerpool._cli:cli"


setuptools.setup(
    author="Conrad Bzura",
    author_email="conradbzura@gmail.com",
    entry_points={
        "console_scripts": [
            f"workerpool={entrypoint}",
            f"wp={entrypoint}",
        ]
    },
    include_package_data=True,
    install_requires=["pydantic~=2.0", "click", "debugpy", "psutil"],
    name="wool",
    package_dir={"": "src"},
    packages=setuptools.find_packages(include=["src"]),
    version="0.0.0",
)
