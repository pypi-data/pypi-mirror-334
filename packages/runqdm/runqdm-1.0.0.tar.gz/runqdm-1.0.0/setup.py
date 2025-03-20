from setuptools import setup, find_packages

setup(
    name="runqdm",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        'runqdm': ['running_man_frame/*.txt'],
    },
    include_package_data=True,
    install_requires=[
        "setuptools",  # pkg_resources를 위해
        "colorama",    # Windows ANSI 지원
    ],
    author="hangilzzang",
    author_email="gkrwhddlwjqrl@gmail.com",
    description="A running progress bar package with animation",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hangilzzang/runqdm.git",  # 깃허브 URL 추가 필요
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 라이선스에 맞게 수정 필요
        "Operating System :: OS Independent",
    ],
) 