# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
    from PySide import QtCore
except:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
    from PyQt5 import uic

import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    ui = uic.loadUi('mainwindow.ui', baseinstance=main_window)

    ui.action_Quit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    main_window.show()

    sys.exit(app.exec_())

