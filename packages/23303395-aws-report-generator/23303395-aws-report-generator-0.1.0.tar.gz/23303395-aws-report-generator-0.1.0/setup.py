from setuptools import setup, find_packages

setup(
    name="23303395-aws-report-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "openpyxl"
    ],
    author="23303395 National College of Ireland",
    author_email="rohit.korlahalli21@gmail.com",
    description="A library to fetch AWS data, generate Excel reports, and upload them to S3.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourgithub/aws-report-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)