import os
import sys
import subprocess
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.develop import develop
import sysconfig

class CMakeExtension(Extension):
    """Defines a CMake extension for compiling C++ code."""
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

def ensure_pybind11():
    try:
        import pybind11
        print(f"Pybind11 already installed: {pybind11.__version__}")
    except ImportError:
        print("Installing pybind11 before compilation...")
        print(sys.executable)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11"])

class CMakeBuild(build_ext):
    """Runs CMake and Make to build the shared library."""
    def build_extension(self, ext):
        ensure_pybind11()
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        python_include_dir = sysconfig.get_path("include")
        python_library_dir = sysconfig.get_config_var("LIBDIR")


        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPython3_EXECUTABLE={sys.executable}",
            f"-DPYTHON_INCLUDE_DIR={python_include_dir}",
            f"-DPYTHON_LIBRARY={python_library_dir}/libpython3.11.so",
            "-DCMAKE_BUILD_TYPE=Release",
        ]


        build_temp = os.path.join(self.build_temp, ext.name)
        os.makedirs(build_temp, exist_ok=True)

        # Run CMake configuration
        subprocess.run(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp, check=True)
        
        # Compile the C++ extension
        subprocess.run(["cmake", "--build", ".", "--config", "Release"], cwd=build_temp, check=True)

class CustomInstall(install):
    """Ensures the C++ extension is built during pip install."""
    def run(self):
        self.run_command("build_ext")
        install.run(self)

class CustomDevelop(develop):
    """Ensures the C++ extension is built during development install."""
    def run(self):
        self.run_command("build_ext")
        develop.run(self)

#Setup the installation
setup(
    name="uaibot",
    version="1.1.0",
    author="Vinicius Goncalves et al",
    author_email="vinicius.marianog@gmail.com",
    description="Uaibot, online robotic simulator",
    long_description="Uaibot, online robotic simulator",
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_repo",
    #packages=setuptools.find_packages(where=".",include=["uaibot", "uaibot.*"]),
    packages=["uaibot"] + setuptools.find_packages(include=["uaibot.*"]),
    package_dir={"uaibot": "uaibot"},  
    include_package_data=True,  
    ext_modules=[CMakeExtension("uaibot_cpp_bind", sourcedir="uaibot/c_implementation")],
    cmdclass={
        "build_ext": CMakeBuild,
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
    # package_data={
    #     "simulation": ["**/*.js"], 
    # },
    package_data={
        "uaibot.simulation": ["*.js"], 
    },    
     
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "pybind11>=2.10",
        "colour==0.1.5",
        "httplib2==0.20.4",
        "ipython==8.0.1",
        "numpy==1.24", 
        "scipy>=1.10",  
        "setuptools>=58.0.4",
        "quadprog>=0.1.13",
        "matplotlib >= 3.10.0",
        "requests"
    ],
    setup_requires=["pybind11>=2.10"],
)
