# Primitive i/o functions referenced elsewhere, useful for test patching (a
# sort of dependency injection

import sys

import readchar

from wizlib.parser import WizArgumentError


ISATTY = all(s.isatty() for s in (sys.stdin, sys.stdout, sys.stderr))


def isatty():
    return ISATTY


def stream():
    return '' if ISATTY else sys.stdin.read()


def ttyin():
    if ISATTY:
        return readchar.readkey()
    else:
        raise WizArgumentError(
            'Command designed for interactive use')
