#!/usr/bin/env python3
import os

from argparse import ArgumentParser


def main():
    usage = """usage: %(prog)s [options] /path/to/appendonlydir
Example : %(prog)s --dump -f json "user.*" /path/to/appendonlydir"""

    parser = ArgumentParser(prog='aof', usage=usage)
    parser.add_argument("-d", "--dump", action='store_true', required=True,
                        help="dump AOF file to printable lines")
    parser.add_argument("-f", "--format", required=False, default="json",
                        help="lines formate, Valid format are json, raw")
    parser.add_argument("-o", "--output", required=False,
                        help="outout destination, default is stdout")
    parser.add_argument("-n", "--db", dest="dbs", default=0, type=int,
                        help="database Number.")
    parser.add_argument("--offset", dest="offset", default=0, type=int,
                        help="AOF offset, index smaller are discarded")
    parser.add_argument("directories", metavar='DIR', nargs=1,
                        help="AOF dir to process")

    options = parser.parse_args()

    """
    Here we start to process appendonlydir, it will contain three files:

    1. `appendonly.aof.manifest` descripe which base file(RDB) and append file
       (AOF) we should use.
    2. `appendonly.aof.2.base.rdb`, RDB file, which should process first.
    3. `appendonly.aof.2.incr.aof`, AOF file, which showld process after RDB.
    """
    try:
        manifest = manifest_file(options.directories[0])
        rdb_file = get_rdb_file(options.directories[0], manifest)
        aof_file = get_aof_file(options.directories[0], manifest)
        print(rdb_file)
        print(aof_file)

        # aof_callback = AOFCallback()
        # parser = RdbParser(aof_callback, filters=None)
        # parser.parse(rdb_file)
    finally:
        pass


def manifest_file(dir: str):
    file = dir + "/appendonly.aof.manifest"

    if not os.path.exists(file):
        raise FileNotFoundError

    return file


def get_rdb_file(dir: str, manifest_file: str):
    with open(manifest_file, 'r') as file:
        for line in file:
            if "type b" not in line:
                continue
            file_name = line.split(" ")[1]
            break

    rdb_file = dir + "/" + file_name
    if not os.path.exists(rdb_file):
        raise FileNotFoundError

    return rdb_file


def get_aof_file(dir: str, manifest_file: str):
    with open(manifest_file, 'r') as file:
        for line in file:
            if "type i" not in line:
                continue
            file_name = line.split(" ")[1]
            break

    aof_file = dir + "/" + file_name
    if not os.path.exists(aof_file):
        raise FileNotFoundError

    return aof_file


if __name__ == '__main__':
    main()
