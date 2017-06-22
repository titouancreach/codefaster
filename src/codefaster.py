import argparse
import asyncio
import config
import glob
import itertools
import logging
import os.path
import random
import signal
import sys
import re

try:
    from termcolor import colored
except ImportError:
    pass


logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s -- %(message)s')


class TimeoutException(Exception):
    """
    Exception that will be raised when the SIGALRM will be triggered.
    """
    pass


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
        :return a random line
    """
    selectedfile = random.choice(files_path)

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
    line = ''  # not valid line at start
    while not lineisvalid(line):
        line = randomline(files_path)
        line = cleanline(line)

    return line


def cleanline(line):
    """
    Clean the line, replace tabs by space, remove trailings spaces
        :param line the line to clean
    """
    return line.replace('\t', ' ' * 4).strip(' \n')


def startdactylo(files_path):

    correct_line = 0
    incorrect_line = 0

    try:
        while True:
            rl = randomlinevalid(files_path)
            print(rl)
            v = input()
            if v == rl:
                correct_line += 1
                if 'termcolor' in sys.modules:
                    logging.info(colored('correct', 'green'))
                else:
                    logging.info('correct')
            else:
                incorrect_line += 1
                if 'termcolor' in sys.modules:
                    logging.info(colored('incorrect', 'red'))
                else:
                    logging.info('incorrect')

    except TimeoutException:
        return correct_line, incorrect_line


def lineisvalid(line):
    """
    Tell if the line is valid.
        :param line the line to test
        :return True if the line is valid false otherwise
    """

    matches = [re.match(x, line) for x in config.LINE_IGNORE_PATTERNS]

    return line and not any(matches)


def handle_sig_alarm(signum, frame):
    """
    handle SIGALRM signal
    """
    raise TimeoutException()


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

    signal.signal(signal.SIGALRM, handle_sig_alarm)

    signal.alarm(config.TIMEOUT)

    correct_line, incorrect_line = startdactylo(filenames)

    if 'termcolor' in sys.modules:
        logging.info('\n\n' + colored(('You typed {} correct lines and {}'
                                       ' incorrect lines')
                     .format(correct_line, incorrect_line), 'green'))
    else:
        logging.info('\n\nYou typed {} correct lines and {} incorrect lines'
                     .format(correct_line, incorrect_line))

    logging.info('bye !')
