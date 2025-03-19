import setuptools

LONG_DESC = open("README.md").read()
VERSION = "0.1.0"
DOWNLOAD = "https://github.com/UAV4Res/uav4res-visualizer/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="uav4res-visualizer",
    version=VERSION,
    author="UAV4Res",
    author_email="nhphuong.code@gmail.com",
    description="uav4res-visualizer",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="uav4res-visualizer",
    license="MIT",
    url="https://github.com/UAV4Res/uav4res-visualizer",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["uav4res_visualizer=uav4res_visualizer.__main__:main"]
    },
    python_requires=">=3.5",
    install_requires=[
        "pygame>=2.4.0",
        "numpy",
        "opencv-python",
        "Pillow",
    ],
    package_data={"uav4res-visualizer": ["engine/*"]},
    include_package_data=True,
    zip_safe=False,
)
