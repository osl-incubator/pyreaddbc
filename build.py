from distutils.command.build_ext import build_ext
from distutils.core import Extension
from distutils.errors import DistutilsExecError  # noqa E501
from distutils.errors import CCompilerError, DistutilsPlatformError
from pathlib import Path

BASE_DIR = Path().resolve()

ext_modules = [
    Extension(
        "_readdbc",
        sources=[
            "pyreaddbc/c-src/dbc2dbf.c",
            "pyreaddbc/c-src/blast.c",
        ],
        include_dirs=["pyreaddbc/c-src/"],
    ),
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed("File not found. Could not compile C extension.")

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (
            CCompilerError,
            DistutilsExecError,
            DistutilsPlatformError,
            ValueError,
        ):
            raise BuildFailed("Could not compile C extension.")


# raise Exception()
def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": ExtBuilder}}
    )
