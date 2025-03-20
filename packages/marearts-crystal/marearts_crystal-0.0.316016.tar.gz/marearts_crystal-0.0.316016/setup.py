from setuptools import setup, Extension
from Cython.Build import cythonize
from wheel.bdist_wheel import bdist_wheel

class BdistWheelCommand(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        self.root_is_pure = False
        self.plat_name_supplied = True

# Define the extension
ext_modules = [
    Extension(
        "marearts_crystal.ma_crystal", 
        ["marearts_crystal/ma_crystal.pyx"]
    )
]

# Compile the extension
compiled_ext_modules = cythonize(
    ext_modules, 
    compiler_directives={'language_level': "3"}
)

if __name__ == '__main__':
    setup(
        ext_modules=compiled_ext_modules,
        cmdclass={'bdist_wheel': BdistWheelCommand},
        include_package_data=True,
    )