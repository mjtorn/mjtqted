# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
    from PySide import QtCore
except:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
    from PyQt5 import QtGui
    from PyQt5 import uic

import importlib
import os
import shutil
import sys


# XXX: Would be configurable in anything real
EDITOR_PATH = os.path.join(os.path.expanduser('~'), '.mjtqted/')
PLUGINS_PATH = os.path.join(EDITOR_PATH, 'plugins')
sys.path.insert(0, PLUGINS_PATH)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Create a plugins dir for convenience
        if not os.path.exists(EDITOR_PATH):
            # Disregard beginning and trailing slashes
            split_path = EDITOR_PATH.split(os.path.sep)[1:-1]
            p = '/'
            for elem in split_path:
                p = os.path.join(p, elem)
                if not os.path.exists(p):
                    os.mkdir(p)

            # XXX: This would also be safer in anything real
            shutil.copytree('plugins', PLUGINS_PATH)

        # Using QtGui.QStandardItemModel makes sense, it's well suited
        # to contain our plugins. Can be inherited if needed, of course.
        self.registry = QtGui.QStandardItemModel()

    def _get_plugins(self):
        """Get individual plugins
        """

        files = os.listdir(PLUGINS_PATH)
        for f in files:
            if not f.startswith('_') and f.endswith('.py'):
                plugin_module_name = f.split('.', 1)[0]
                plugin_module = importlib.import_module(plugin_module_name)

                for obj_name in dir(plugin_module):
                    obj = getattr(plugin_module, obj_name)

                    # XXX: This could and/or should be stricter!
                    if type(obj) == QtCore.pyqtWrapperType:
                        self.registry.appendRow(obj())

    def set_initial_state(self):
        """Helper for things we init after ui is inited
        """

        # XXX: textEdit could be custom-inherited from QTextEdit
        self.textEdit.saved = False

        # Save in home directory by default
        self.lineEdit.setText(os.path.join(os.path.expanduser('~'), ''))

        # Get plugins
        self._get_plugins()

        # Have the listView react on the registry
        self.listView_Outputs.setModel(self.registry)

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

    @QtCore.pyqtSlot('QModelIndex', name='on_listView_Outputs_doubleClicked')
    def save_output(self, index):
        plugin = self.registry.item(index.row())
        fname = self.lineEdit.text()
        content = '{}\n'.format(self.textEdit.document().toPlainText().strip())
        plugin.save(self, fname, content)

if __name__ == '__main__':
    shutil.rmtree(EDITOR_PATH, ignore_errors=True)

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    ui = uic.loadUi('mainwindow.ui', baseinstance=main_window)

    ui.action_Quit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    # Do the init we can do after ui is set up
    main_window.set_initial_state()

    main_window.show()

    sys.exit(app.exec_())

