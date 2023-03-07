import subprocess
import sys
import os
import glob


def __loop(app_path: str, ui: bool):
    app_dir = os.path.dirname(app_path)
    if ui:
        f_path = os.path.join(app_dir, "*.ui")
    else:
        f_path = os.path.join(app_dir, "*.qrc")
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


def mk_desktop(app_path: str):
    app_dir = os.path.dirname(app_path)
    icon_path = os.path.join(app_dir, "Resources", "Icons", "WinLogo.png")
    home_dir = os.path.expanduser('~')
    desk_path = os.path.join(home_dir, "Desktop")
    share_path = os.path.join(home_dir, ".local", "share", "applications")

    if os.path.isdir(share_path):
        desk_path = os.path.join(share_path, "AucPeakFitter.desktop")
    elif os.path.isdir(desk_path):
        desk_path = os.path.join(desk_path, "AucPeakFitter.desktop")
    else:
        desk_path = os.path.join(home_dir, "AucPeakFitter.desktop")
    with open(desk_path, "w") as fid:
        fid.write("[Desktop Entry]\nVersion=1.0\nType=Application\nName=AUC Peak Decomposition\n")
        fid.write(f"Icon={icon_path}\n")
        fid.write(f'Exec={sys.executable} {app_path}\n')
        fid.write("Categories=Development\nTerminal=false\nStartupWMClass=Qt\nStartupNotify=true\n")
        print("\n---\nDesktop entry is written in:")
        print(desk_path)


def ui2py(f_path: str):
    __loop(f_path, ui=True)


def qrc2py(f_path: str):
    __loop(f_path, ui=False)


if __name__ == "__main__":
    curr_path = os.path.relpath(sys.argv[0])
    ui2py(curr_path)
    qrc2py(curr_path)
