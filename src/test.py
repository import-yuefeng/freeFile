import sys
import argparse


# parser = argparse.ArgumentParser(description='Usage under args.')  

# parser.add_argument("-f", dest = "filePath", help = "FilePath" )
# parser.add_argument("--name", dest = "name", help = "Update/Download use FIN.tar.bz2 or name.tar.bz2")

# args = parser.parse_args(list(sys.argv[2:]))
# print(args.name, args.filePath)
# print(sys.argv[1])
# 
# 
import subprocess
import re

FIN = "ASHJKDkagkjs"
result = subprocess.check_output("mc share upload minio/test/"+FIN, shell=True)
# print(result)
print(re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)<FILE>", str(result))[0])

