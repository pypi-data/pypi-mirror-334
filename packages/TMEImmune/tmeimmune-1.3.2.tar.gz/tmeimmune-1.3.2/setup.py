from setuptools import setup, find_packages

VERSION = '1.3.2' 
DESCRIPTION = 'Python package for calculating TME scores'


# Setting up
setup(
        name="TMEImmune", 
        version=VERSION,
        author="Qilu Zhou",
        author_email="<qiluzhou@umass.edu>",
        url="https://github.com/ShahriyariLab/TMEImmune",
        description=DESCRIPTION,
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        include_package_data=True,
        package_data={
        "TMEImmune": ["data/*.csv", "data/*.json", "data/*.gmt", "data/nb_biomarker/*", "data/Gide/*"], 
        },
        install_requires=["pandas>=1.5.0", "numpy>=1.23.5", "rnanorm",
                          "inmoose", "lifelines", "scikit-learn", "matplotlib", "scipy", "statsmodels", "joblib"], 
        keywords=['python', 'TME score'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        python_requires=">=3.10"
)