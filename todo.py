#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime   # для преобразования даты в приемлемый формат

IGNORE_DIRS = [".hg", ".svn", "data"]
FILE_EXT = (".py")
COMMENT = ("#", "##")
TODO = ("TODO:", "BUG:", "INFO:", "FIXME")

TODO_STR = []
proc_files = []

def getfiles(dir = "."):
    for root, dirs, files in os.walk(dir):
        for dir in set(dirs).intersection(IGNORE_DIRS):
            dirs.remove(dir)

        for file in files:
            if file.endswith(FILE_EXT):
                proc_files.append(os.path.join(root,file))


def processfile(file):
    ADD = False
    line_num = 0
    for line in open(file):
        line_num += 1
        line = line.strip()
        
        if not line.startswith(COMMENT):
            if ADD:
                ADD = False
                TODO_STR[-1] += "\n\n"
            continue

        line = line.strip("#")
        line = line.strip()
        
        if line.startswith(TODO):
            ADD = True
            TODO_STR.append(file + ":" + str(line_num) + "\n" + line)
            continue
            
        if ADD:
            TODO_STR[-1] += "\n" + line


        #print root, ' ', dirs, ' ', files

        ## count = count + files.count
        ## for name in files:
            ## fullname = os.path.join(root, name)	# получаем полное имя файла
            ## size = os.path.getsize(fullname)    # размер файла в байтах
            ## ksize = size//1024              # размер в килобайтах
            ## atime = os.path.getatime(fullname)  # дата последнего доступа в секундах с начала эпохи
            ## mtime = os.path.getmtime(fullname)  # дата последней модификации в секундах с начала эпохи

            ## print 'Size: ', ksize, ' KB'
            ## print 'Last access date: ', datetime.fromtimestamp(atime)
            ## print 'Last modification date: ', datetime.fromtimestamp(mtime)

            ## print 'name: '#, fullname, '\n'# root: ", root, " dirs: ", files, "\n"	# делаем что-нибудь с ним

def main():
    getfiles()
    for file in proc_files:
        processfile(file)
    todofile = open("TODO.txt", "w")
    for line in TODO_STR:
        todofile.write(line)

if __name__ == '__main__':
    main()
