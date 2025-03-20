from setuptools import setup, find_packages

setup(
    name="apache-airflow-dragdrop-plugin",
    version="0.1.1",
    author="Akshay Thakare",
    author_email="akshay.thakare031@gmail.com",
    description="A drag-and-drop DAG designer plugin for Apache Airflow",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/datainteg/apache-airflow-dragdrop-plugin",
    packages=find_packages(include=["airflow_dragdrop_plugin", "airflow_dragdrop_plugin.*"]),
    include_package_data=True,
    install_requires=["apache-airflow>=2.5"],
    classifiers=[
        "Framework :: Apache Airflow",
        "Programming Language :: Python :: 3",
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
)