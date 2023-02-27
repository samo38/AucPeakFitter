from PySide6 import QtWidgets
from main_widget import MainWindow
import qt_to_py
import sys
import argparse

if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument('--ui2py', dest='ui2py', help='Convert all UI files', action='store_true', default=False)
    args = options.parse_args()
    if args.ui2py:
        qt_to_py.qt_uic()
        qt_to_py.qt_rcc()

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
