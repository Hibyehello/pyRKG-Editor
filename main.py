def main():
    try:
        import sys
        from MainWindow import MainWidget
        from PySide6 import QtWidgets
        import fastcrc
        import pytest
        import requests
    except ModuleNotFoundError:
        print("You should have read the README!! Please run pip -r requirements.txt")
        exit(-1)

    app = QtWidgets.QApplication([])
    widget = MainWidget()
    widget.show()

    widget.setWindowTitle("PyRKG Editor")
    widget.setMinimumSize(300, 175)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
