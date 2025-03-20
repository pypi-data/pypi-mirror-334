from setuptools import setup, find_packages

setup(
    name="lt_cvd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "scikit-survival"],
    entry_points={
        "console_scripts": [
            "rsf-predict=lt_cvd.run_model:main"
        ]
    },
)
