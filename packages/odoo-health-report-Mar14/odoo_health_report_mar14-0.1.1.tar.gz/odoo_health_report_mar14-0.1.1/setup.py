from setuptools import setup, find_packages

setup(
    name="odoo-health-report-Mar14",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2.0",
        # Add other dependencies from your requirements.txt
    ],
    entry_points={
        "console_scripts": [
            "odoo-health-report=health_report.cli:main",
        ],
    },
    python_requires=">=3.6",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Django application for monitoring Odoo server metrics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/odoo-health-report",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)
