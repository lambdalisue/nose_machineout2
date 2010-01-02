
"""
Formats nose output into format easily parsable by machine.

It is intended to be use to integrate nose with your IDE such as Vim.

@author: Max Ischenko <ischenko@gmail.com>
"""

import re
import os.path
import traceback
from nose.plugins import Plugin

__all__ = ['NoseMachineReadableOutput']

try:
    import doctest
    doctest_fname = re.sub('\.py.?$', '.py', doctest.__file__)
    del doctest
except ImportError:
    doctest_fname = None

class dummystream:
    def write(self, *arg):
        pass
    def writeln(self, *arg):
        pass
    def flush(self):
        pass

def is_doctest_traceback(fname):
    return fname == doctest_fname

class PluginError(Exception):
    def __repr__(self):
        s = super(PluginError, self).__repr__()
        return s + "\nReport bugs to ischenko@gmail.com."

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
        fname, lineno, funname, msg = fulltb[-1]
        # explicit support for doctests is needed
        if is_doctest_traceback(fname):
            # doctest traceback includes pre-formatted error message
            # which we parse (in a very crude way).
            n = value.args[0].rindex('-'*20)
            formatted_msg = value.args[0][n+20+1:]
            m = self.doctest_failure_re.match(formatted_msg)
            if not m:
                raise RuntimeError("Can't parse doctest output: %r" % value.args[0])
            fname, lineno, funname, msg = m.groups()
            if '.' in funname: # strip module package name, if any
                funname = funname.split('.')[-1]
            lineno = int(lineno)
            lines = msg.split('\n')
            msg0 = lines[0]
        else:
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
        "Strips common path segments if any."
        if fname.startswith(self.basepath):
            return fname[len(self.basepath)+1:]
        return fname

    def addFailure(self, test, err):
        self.addFormatted('fail', err)

    def setOutputStream(self, stream):
        # grab for own use
        self.stream = stream
        # return dummy stream to supress normal output
        return dummystream()
