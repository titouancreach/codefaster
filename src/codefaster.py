import argparse
import curses
import glob
import itertools
import logging
import os.path
import random

import config

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s -- %(message)s')


def scan_basedir(basedir, fileext):
    """
    Recursively scan base directory and search for file with the extension
    described in filext.
        :param basedir Base directory
        :param filext list of the extension
        :param return a lazy collection containing the path
    """

    basedirpath = os.path.join(os.path.abspath(os.path.expanduser(basedir)),
                               '**/*')
    filenames = [glob.iglob('{}.{}'.format(basedirpath, filename),
                 recursive=True) for filename in fileext]

    return itertools.chain(*filenames)


def randomline(files_path):
    """
    Retrieve a random line from a file contained in files_path
        :param files_path list of paths
        :return a random lien
    """
    selectedfile = random.choice(files_path)

    logging.debug(selectedfile)

    selectedline = ''

    # (Waterman's "Reservoir Algorithm")
    with open(selectedfile) as f:
        line = next(f)
        for num, line in enumerate(f):
            if random.randrange(num + 2):
                continue
            selectedline = line
        return selectedline


def randomlinevalid(files_path):
    """
    Get a random line from the file that fit our requierements
        :param files_path list of paths
        :return a random line
    """
    line = ''  # not valid line for start
    while not lineisvalid(line):
        line = randomline(files_path)
        line = cleanline(line)

    return line


def configui(stdscr):
    """
    Configure the UI.
        :param stdscr curse screen handle
    """
    curses.noecho()
    curses.nocbreak()
    stdscr.keypad(True)


def mainloop(stdscr, win):
    try:
        while True:
            stdscr.getch()
    except KeyboardInterrupt:
        pass


def cleanline(line):
    """
    Clean the line, replace tabs by space, remove trailings spaces
        :param line the line to clean
    """
    return line.replace('\t', ' ' * 4).strip(' \n')


def lineisvalid(line):
    """
    Tell if the line is valid.
        :param line the line to test
        :return True if the line is valid false otherwise
    """
    return line != ''


def startui(stdscr):
    """
    Start the UI mode.
    The screen handle is created by the wrapper and is
    automatically bound to this function.
        :param stdscr curse screen handle
    """
    configui(stdscr)

    win = curses.newwin(curses.LINES - 1, curses.COLS - 1, 0, 0)
    win.box()
    stdscr.refresh()
    win.refresh()

    mainloop(stdscr, win)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Code faster')
    parser.add_argument('basedir', metavar='basedir', type=str,
                        help='base directory for source code')
    args = parser.parse_args()
    basedir = args.basedir

    filespath = scan_basedir(basedir, config.FILE_EXT)

    logging.info('Scanning...')
    filenames = list(filespath)
    logging.info('Finished, {} files where found...'.format(len(filenames)))
    logging.info('Starting UI')

    curses.wrapper(startui)

    logging.info('bye !')

    logging.debug(randomlinevalid(filenames))
