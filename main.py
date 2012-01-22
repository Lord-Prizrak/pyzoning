#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.game import *
from os import popen

def main():

    ## TODO: В дальнейшем убрать
    fd = popen("hg tip")
    for line in fd:
        if line.startswith("changeset"):
            revision = line[len("changeset:"):].strip()
            print "Revision:",revision
    fd.close()

    g=Game()
    g.start()
    print "Quit."
    return 0


if __name__ == '__main__':
    main()
