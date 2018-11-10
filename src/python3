[baseConfig]
# baseConfigure
name=None
OSS_Choice=default
encrypt=no

import sys
import argparse

streamFile = None

parser = argparse.ArgumentParser(description='Usage under args.')  

parser.add_argument("-f", dest = "filePath", help = "FilePath" )
parser.add_argument("--name", dest = "name", help = "Update/Download use FIN.tar.bz2 or name.tar.bz2")

args = parser.parse_args(list(sys.argv[2:]))
print(args.name, args.filePath)
print(sys.argv[1])

streamFile = sys.stdin.read()

if streamFile != None:
    print("有流形式传入数据")
    print("内容是%s" %text)
else:
    print("没有流形式传入数据")


# import subprocess
# import re

# FIN = "ASHJKDkagkjs"
# ip = subprocess.check_output("curl ip.sb", shell=True)
# print(str(ip).split(r"\n")[0][2:])
# # result = subprocess.check_output("mc share upload minio/test/"+FIN, shell=True)
# # # print(result)
# # print(re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)<FILE>", str(result))[0])

