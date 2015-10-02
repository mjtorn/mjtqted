# vim: fileencoding=utf-8

from PyQt5 import QtGui


class Plugin(QtGui.QStandardItem):
    """Base class for plugins
    """

    def __init__(self, *args, **kwargs):
        """Instantiate if sane
        """

        super().__init__(*args, **kwargs)

        if self.__class__.__name__ != 'Plugin':
            if not hasattr(self, 'name'):
                raise AttributeError('Set the `name` attribute')

            self.setText(self.name)
            self.setEditable(False)

    def save(self, main_win, path, content):
        """qt main window, str path to file, str content
        """

        pass

