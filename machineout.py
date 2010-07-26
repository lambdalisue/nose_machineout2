"""
Formats nose output into format easily parsable by machine.
It is intended to be use to integrate nose with your IDE such as Vim.
"""

import re
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

    doctest_failure_re = re.compile(
            'File "([^"]+)", line (\d+), in ([^\n]+)\n(.+)',
            re.DOTALL)

    def __init__(self):
        super(NoseMachineReadableOutput, self).__init__()
        self.basepath = os.getcwd()

    def add_options(self, parser, env=None):
        super(NoseMachineReadableOutput, self).add_options(parser, env)
        parser.add_option("--machine-output", action="store_true",
                          dest="machine_output", default=False,
                          help="Reports test results in parsable format.")

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
                if fname.startswith(self.basepath):
                    break
        except IndexError:
            fname, lineno, funname, msg = fallback

        lines = traceback.format_exception_only(exctype, value)
        lines = [line.strip('\n') for line in lines]
        msg = lines[0]

        fname = self.format_testfname(fname)
        prefix = "%s:%d" % (fname, lineno)
        self.stream.writeln("%s: In %s" % (fname, funname))
        self.stream.writeln("%s: %s: %s" % (prefix, etype, msg))

        if len(lines) > 1:
            pad = ' '*(len(etype)+1)
            for line in lines[1:]:
                self.stream.writeln("%s: %s %s" % (prefix, pad, line))

    def format_testfname(self, fname):
        if fname.startswith(self.basepath):
            return fname[len(self.basepath)+1:]

        return fname
