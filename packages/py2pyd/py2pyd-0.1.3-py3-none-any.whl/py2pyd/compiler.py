import os
import sys
import shutil
import sysconfig
import platform
from setuptools import setup
from Cython.Build import cythonize

def get_shared_lib_filename(module_name):
    """Get the correct compiled extension based on OS"""
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX") or (".pyd" if platform.system() == "Windows" else ".so")
    return f"{module_name}{ext_suffix}"

def create_pyx(py_file):
    """Convert .py file to .pyx for Cython compilation"""
    pyx_file = py_file.replace(".py", ".pyx")
    shutil.copy(py_file, pyx_file)
    return pyx_file

def create_setup(pyx_file):
    """Generate setup.py script dynamically"""
    module_name = os.path.splitext(os.path.basename(pyx_file))[0]
    setup_code = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{pyx_file}", language_level='3')
)
"""
    return setup_code
def compile_shared_lib(py_file):
    """Compile Python file into a shared library (.pyd/.so)"""
    try:
        pyx_file = create_pyx(py_file)
        setup_code = create_setup(pyx_file)

        setup_path = "setup.py"
        with open(setup_path, "w") as f:
            f.write(setup_code)

        os.system(f"python {setup_path} build_ext --inplace")

        compiled_lib = get_shared_lib_filename(pyx_file.replace(".pyx", ""))
        return compiled_lib if os.path.exists(compiled_lib) else None
    except Exception as e:
        print(f"Compilation error: {e} - for module: {py_file}")
        return None

def clean_up(py_file):
    """Remove temporary build files"""
    temp_files = [py_file.replace(".py", ext) for ext in [".pyx", ".c", ".so", ".pyd", "setup.py"]]
    for fi in temp_files:
        if os.path.exists(fi):
            os.remove(fi)
    if os.path.exists('setup.py'):
        os.remove('setup.py')
    shutil.rmtree("./build", ignore_errors=True)

def convert(py_file=None):
    """Main function to compile .py to .pyd/.so"""
    if py_file is None:
        if len(sys.argv) < 2:
            print("Usage: py2pyd <your_script.py>")
            sys.exit(1)
        py_file = sys.argv[1]

    if not os.path.exists(py_file):
        print(f"Error: File '{py_file}' not found.")
        return None

    try:
        compiled_lib = compile_shared_lib(py_file)

        if compiled_lib:
            clean_up(py_file)
            output_file = compiled_lib.split(".")[0]+"."+compiled_lib.split(".")[-1]
            os.rename(compiled_lib, output_file)
            print(f"Successfully created {output_file}")
        return output_file
    except Exception as e:
        print(f"Compilation error: {e}")
        return None

def main():
    """Entry point for CLI usage"""
    convert()

if __name__ == "__main__":
    main()
