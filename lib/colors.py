class Colors(object):

    COLOR_CODES = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
    }

    @staticmethod
    def colorize(code, string):
        return "\033[%sm%s\033[0m" % (code, string)

    def __getattr__(self, attr_name):
        if attr_name in self.COLOR_CODES.keys():
            return lambda x: self.colorize(self.COLOR_CODES[attr_name], x)

colors = Colors()
