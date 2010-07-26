"""
Formats nose output into format easily parsable by machine.
It is intended to be use to integrate nose with your IDE such as Vim.
"""

import re
import traceback
from nose.plugins import Plugin


__all__ = ['NoseMachineReadableOutput']


class dummystream:

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

    doctest_failure_re = re.compile('File "([^"]+)", line (\d+), in ([^\n]+)\n(.+)',
            re.DOTALL)

    def __init__(self):
        super(NoseMachineReadableOutput, self).__init__()
        self.basepath = os.getcwd()

    def add_options(self, parser, env):
        super(NoseMachineReadableOutput, self).add_options(parser, env)
        parser.add_option("--machine-output", action="store_true",
                          dest="machine_output",
                          default=False,
                          help="Reports test results in easily parsable format.")

    def configure(self, options, conf):
        super(NoseMachineReadableOutput, self).configure(options, conf)
        self.enabled = options.machine_output

    def addSkip(self, test):
        pass

    def addDeprecated(self, test):
        pass

    def addError(self, test, err):
        self.addFormatted('error', err)

    def addFormatted(self, etype, err):
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
        msg0 = lines[0]

        fname = self.format_testfname(fname)
        prefix = "%s:%d" % (fname, lineno)
        self.stream.writeln("%s: In %s" % (fname, funname))
        self.stream.writeln("%s: %s: %s" % (prefix, etype, msg0))

        if len(lines) > 1:
            pad = ' '*(len(etype)+1)
            for line in lines[1:]:
                self.stream.writeln("%s: %s %s" % (prefix, pad, line))

    def format_testfname(self, fname):
        if fname.startswith(self.basepath):
            return fname[len(self.basepath)+1:]

        return fname

    def addFailure(self, test, err):
        self.addFormatted('fail', err)

    def setOutputStream(self, stream):
        self.stream = stream
        return dummystream()
