# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
    from PySide import QtCore
except:
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4 import QtWidgets
    from PyQt4 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        pass
