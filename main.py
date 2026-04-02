import sys
from MainWindow import MainWidget
from PySide6 import QtWidgets


def main():
    app = QtWidgets.QApplication([])
    widget = MainWidget()
    widget.show()

    widget.setWindowTitle("PyRKG Editor")
    widget.setMinimumSize(300, 175)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
