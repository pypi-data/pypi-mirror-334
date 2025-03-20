from setuptools import setup, find_packages

setup(
    name="api_2fa_fb",
    version="1.0.0",
    author="Nguyễn Minh Đức",
    author_email="dancntt7@gmail.com",
    description="A Python package for fetching Facebook 2FA OTP",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
