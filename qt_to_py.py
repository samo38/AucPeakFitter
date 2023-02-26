import subprocess
import sys
import os
import glob


def __loop(ui: bool):
    if ui:
        f_path = os.path.join(os.path.curdir, "*.ui")
    else:
        f_path = os.path.join(os.path.curdir, "*.qrc")
    f_list = glob.glob(f_path)
    for f_name in f_list:
        in_file = os.path.abspath(f_name)
        fsp = os.path.split(in_file)
        if ui:
            out_nm = fsp[1].replace(".ui", ".py")
        else:
            out_nm = fsp[1].replace(".qrc", "_rc.py")
        py_file = os.path.join(fsp[0], out_nm)
        py_path = os.path.split(sys.executable)[0]
        if ui:
            cmd = os.path.join(py_path, "pyside6-uic")
        else:
            cmd = os.path.join(py_path, "pyside6-rcc")
        subprocess.check_output([cmd, '-o', py_file, in_file])
        if ui:
            print(f"UI converted: {in_file}")
        else:
            print(f"RCC converted: {in_file}")


def qt_uic():
    __loop(ui=True)


def qt_rcc():
    __loop(ui=False)


if __name__ == "__main__":
    qt_uic()
    qt_rcc()