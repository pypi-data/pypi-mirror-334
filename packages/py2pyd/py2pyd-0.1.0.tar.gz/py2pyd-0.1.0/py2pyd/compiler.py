import os
import sys
import shutil
import sysconfig

def get_pyd_filename(module_name):
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")  # Get platform-specific suffix
    if ext_suffix is None:
        raise RuntimeError("Could not determine .pyd extension")
    return f"{module_name}{ext_suffix}"

def testAndCut(py_file):
    genPyd = get_pyd_filename(py_file.split(".")[0])
    finPyd = genPyd.split(".")[0] + ".pyd" if os.path.exists(genPyd) else None
    if finPyd:
        rem_files([finPyd])
        os.rename(genPyd, finPyd)
    return finPyd

def create_pyx(py_file):
    pyx_file = py_file.replace(".py", ".pyx")
    shutil.copy(py_file, pyx_file)
    return pyx_file

def create_setup(pyx_file):
    module_name = os.path.splitext(os.path.basename(pyx_file))[0]
    setup_code = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{pyx_file}", language_level='3')
)
"""
    return setup_code

def compile_pyd(py_file):
    try:
        pyx_file = create_pyx(py_file)
        setup_code = create_setup(pyx_file)

        setup_path = "setup.py"
        with open(setup_path, "w") as f:
            f.write(setup_code)

        os.system(f"python {setup_path} build_ext --inplace")

        compiled_pyd = pyx_file.replace(".pyx", ".pyd")
        return compiled_pyd
    except Exception as e:
        print(f"Compilation error: {e} - for module: {py_file.split('.')[0]}")

def rem_files(arr_files):
    for fi in arr_files:
        if os.path.exists(fi):
            os.remove(fi)
        else:
            print(f"The file: {fi} does not exist")

def convert(py_file=None):
    if py_file is None:
        if len(sys.argv) < 2:
            print("Usage: py2pyd <your_script.py>")
            sys.exit(1)
        py_file = sys.argv[1]  # Get the first argument from the command line

    if not os.path.exists(py_file):
        print(f"Error: File '{py_file}' not found.")
        return None

    try:
        compiled_pyd = compile_pyd(py_file)
        compiled_pyd = testAndCut(py_file)

        if compiled_pyd is not None:
            print(f"Successfully created {compiled_pyd}")
            arr_files = [py_file.replace(".py", ".pyx"), py_file.replace(".py", ".c"), "setup.py"]
            rem_files(arr_files)
            shutil.rmtree("./build")
        return compiled_pyd
    except Exception as e:
        print(f"Compilation error: {e} - for module: {py_file.split('.')[0]}")
        return None

if __name__ == "__main__":
    convert()  # This ensur