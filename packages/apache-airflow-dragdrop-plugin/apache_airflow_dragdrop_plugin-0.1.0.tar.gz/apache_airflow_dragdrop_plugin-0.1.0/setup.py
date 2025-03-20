from setuptools import setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    name="apache-airflow-dragdrop-plugin",
    version="0.1.0",
    description="A drag-and-drop DAG designer plugin for Apache Airflow",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/datainteg/apache-airflow-dragdrop-plugin",
    author="Akshay Thakare",
    author_email="thakarea686@gmail.com",
    license="MIT",
    classifiers=[
        "Framework :: Apache Airflow",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    entry_points={
        "apache_airflow_plugin": [
            "dragdrop_plugin = airflow_dragdrop_plugin.plugin:MyReactPlugin"
        ]
    },
    packages=["package"],
    include_package_data=True,
)