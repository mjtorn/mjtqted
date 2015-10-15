# vim: fileencoding=utf-8

from plugins import Plugin


class Reverse(Plugin):
    """Plugin for reversing text
    """

    name = 'reverse'

    def save(self, main_win, path, content):
        """Reverse the lines in content, save in path
        """

        with open(path, 'wb') as f:
            # Thanks, Python, for .writelines() not taking a newline keyword argument
            f.writelines((bytes('{}\n'.format(l[::-1]), 'utf-8') for l in content.splitlines()))

