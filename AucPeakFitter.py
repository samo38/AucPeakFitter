from PySide6 import QtWidgets
from main_widget import MainWindow
import setup_tools as st
import sys
import os
import argparse

if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument('--ui2py', dest='ui2py', help='Convert all UI files', action='store_true', default=False)
    options.add_argument('--mk_desk', dest='mk_desk', help="Make the application's desktop entry",
                         action='store_true', default=False)
    args = options.parse_args()
    app_path = os.path.relpath(sys.argv[0])
    app_path = os.path.abspath(app_path)
    if args.ui2py:
        st.ui2py(app_path)
        st.qrc2py(app_path)
    if args.mk_desk:
        st.mk_desktop(app_path)

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
