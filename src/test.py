import sys
import argparse


parser = argparse.ArgumentParser(description='Usage under args.')  

parser.add_argument("-f", dest = "filePath", help = "FilePath" )
parser.add_argument("--name", dest = "name", help = "Update/Download use FIN.tar.bz2 or name.tar.bz2")

args = parser.parse_args(list(sys.argv[2:]))
print(args.name, args.filePath)
print(sys.argv[1])