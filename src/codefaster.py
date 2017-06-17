import config
import curses
import argparse
import glob
import os.path
import itertools


def scan_basedir(basedir, fileext):
    """
    Recursively scan base directory and search for file with the extension
    described in filext.
        :param basedir Base directory
        :filext list of the extension
        :return a lazy collection containing the path
    """

    basedirpath = os.path.join(os.path.abspath(os.path.expanduser(basedir)),
                               '**/*')
    print(basedirpath)
    filenames = [glob.iglob('{}.{}'.format(basedirpath, filename),
                 recursive=True) for filename in fileext]

    return itertools.chain(*filenames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Code faster')
    parser.add_argument('basedir', metavar='basedir', type=str,
                        help='base directory for source code')
    args = parser.parse_args()
    basedir = args.basedir

    filepath = scan_basedir(basedir, config.FILE_EXT)
