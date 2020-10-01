import setuptools


with open("README.md") as fp:
    long_description = fp.read()

cdk_version = "1.65.0"

setuptools.setup(
    name="sadevs_apps",
    version="0.0.1",
    description="cdk app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "sadevs_apps"},
    packages=setuptools.find_packages(where="sadevs_apps"),
    install_requires=[
        "boto3",
        f"aws-cdk.core=={cdk_version}",
        f"aws-cdk.aws-apigateway=={cdk_version}",
        f"aws_cdk.aws_route53_targets=={cdk_version}",
        f"aws_cdk.aws_cloudfront=={cdk_version}",
        f"aws_cdk.aws_s3=={cdk_version}",
        f"aws_cdk.aws_s3_deployment=={cdk_version}",
        f"aws_cdk.aws_dynamodb=={cdk_version}",
        f"aws_cdk.aws_secretsmanager=={cdk_version}",
        f"aws_cdk.aws_ecs=={cdk_version}",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
