"""
Formats nose output into format easily parsable by machine.
It is intended to be use to integrate nose with your IDE such as Vim.
"""

import os
import traceback
from nose.plugins import Plugin


class DummyStream:

    def write(self, *arg):
        pass

    def writeln(self, *arg):
        pass

    def flush(self):
        pass


class NoseMachineReadableOutput(Plugin):
    """
    Output errors and failures in a machine-readable way.
    """

    name = 'machineout'

    def __init__(self):
        super(NoseMachineReadableOutput, self).__init__()
        self.basepath = os.getcwd()

    def addError(self, test, err):
        self.add_formatted('error', err)

    def addFailure(self, test, err):
        self.add_formatted('fail', err)

    def setOutputStream(self, stream):
        self.stream = stream
        return DummyStream()

    def add_formatted(self, etype, err):
        exctype, value, tb = err
        fulltb = traceback.extract_tb(tb)

        fallback = fulltb[-1]
        try:
            while True:
                fname, lineno, funname, msg = fulltb.pop()

                # The check for the `assert' prefix allows the user to extend
                # unittest.TestCase with custom assert-methods, while
                # machineout still returns the most useful error line number.
                if fname.startswith(self.basepath) \
                        and not funname.startswith('assert'):
                    break
        except IndexError:
            fname, lineno, funname, msg = fallback

        lines = traceback.format_exception_only(exctype, value)
        lines = [line.strip('\n') for line in lines]
        msg = lines[0]

        fname = self._format_testfname(fname)
        prefix = "%s:%d" % (fname, lineno)
        self.stream.writeln("%s: %s: %s" % (prefix, etype, msg))

        if len(lines) > 1:
            pad = ' ' * (len(etype) + 1)
            for line in lines[1:]:
                self.stream.writeln("%s: %s %s" % (prefix, pad, line))

    def _format_testfname(self, fname):
        if fname.startswith(self.basepath):
            return fname[len(self.basepath) + 1:]

        return fname
