import argparse
import curses
import glob
import itertools
import logging
import os.path

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
