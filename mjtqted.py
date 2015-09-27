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

    def set_initial_state(self):
        """Helper for things we init after ui is inited
        """

        # XXX: textEdit could be custom-inherited from QTextEdit
        self.textEdit.saved = False

    def ask_new_file(self):
        """Split new file confirmation into its own function
        """

        msg_title = 'Confirmation'
        msg_contents = 'Unsaved changes, are you sure you want a new file?'
        msg_buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        msg_default = QtWidgets.QMessageBox.No

        reply = QtWidgets.QMessageBox.question(self, msg_title, msg_contents, msg_buttons, msg_default)

        return reply

    @QtCore.pyqtSlot(name='on_pushButton_New_clicked')
    def new_file(self):
        """Open a new file; if the current one's not saved, complain
        """

        editor = self.textEdit

        # Toggled by listView_Outputs
        saved = editor.saved

        document = editor.document()
        contents = document.toPlainText().strip()

        if contents and not saved:
            reply = self.ask_new_file()

            if reply == QtWidgets.QMessageBox.Yes:
                document.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    ui = uic.loadUi('mainwindow.ui', baseinstance=main_window)

    ui.action_Quit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    # Do the init we can do after ui is set up
    main_window.set_initial_state()

    main_window.show()

    sys.exit(app.exec_())

