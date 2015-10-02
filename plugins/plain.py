# vim: fileencoding=utf-8

from plugins import Plugin


class Plain(Plugin):
    """Plugins inherit list items to be displayable
    """

    name = 'plain'

    def save(self, main_win, path, content):
        """The default plugin ignores the window, saves content to path
        """

        with open(path, 'wb') as f:
            f.write(bytes(content, 'utf-8'))

