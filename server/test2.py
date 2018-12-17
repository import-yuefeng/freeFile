# [baseConfig]
# # baseConfigure
# name=None
# OSS_Choice=default
# encrypt=no
# import sh


# https://u.nu/api.php?action=shorturl&format=simple&url=http://118.126.93.123:9000/test/?&keyword=example
# http://118.126.93.123:9000/test/c2434fa32eb140cc5e55a2192b496e1922e9a9ab779d3d4bd9f6cbccc2f7748etar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7%2F20181204%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181204T101019Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=f9f0b3024fb4b293fd60c7ffef8f6bd59e50e0630cd208acc9c966e4ad729933
import sys
# import argparse    
import time

# parser = argparse.ArgumentParser(description='Very welcome to use freeFile! Please check the options currently supported by freeFile\n')  
total_length = 20
dl = 0
for dl in range(1, 19):
    # print(i)
    # print("\r当前下载到第".format(i)+str(i)+"页, 即将下载第".format(i+1)+str(i+1)+"页, 下载到".format(i/20*100)+str(i/20*100)+"%%", end="")
    done = int(20 * dl / total_length)
    sys.stdout.write("\r[%s%s]" % ('█' * done, ' ' * (total_length - done)))
    sys.stdout.flush()

    time.sleep(1)
    # print("\r".format(app)+str(app), end="")


# parser.add_argument('-qr', "--qrcode", dest = "qrcode", action='store_true', help='Need to output download QRcode')
# args = parser.parse_args()
# print(args.qrcode)

# streamFile = None

# parser = argparse.ArgumentParser(description='Usage under args.')  

# parser.add_argument("-f", dest = "filePath", help = "FilePath" )
# parser.add_argument("--name", dest = "name", help = "Update/Download use FIN.tar.bz2 or name.tar.bz2")

# args = parser.parse_args(list(sys.argv[2:]))
# print(args.name, args.filePath)
# print(sys.argv[1])

# streamFile = sys.stdin.read()

# if streamFile != None:
#     print("有流形式传入数据")
#     print("内容是%s" %text)
# else:
#     print("没有流形式传入数据")


# import subprocess
# import re

# FIN = "ASHJKDkagkjs"
# import subprocess

# # command -v brew >/dev/null 2>&1 || { echo >&2 "I require foo but it's not installed.  Aborting."; }
# print("\033[1;37m[INFO]\033[0m Check dependency program")
# for app in ['brew', 'pv', 'qrencode']:
#     try:
#         subprocess.check_output("command -v %s >/dev/null 2>&1 || { echo >&2 \" \033[1;35m[WARNING]\033[0m I require %s but it's not installed.\"; exit 1;}"%(app, app), shell=True)
#     except subprocess.CalledProcessError:
#         exit(1)


# print(ip)
# print(str(ip).split(r"\n")[0][2:])
# # result = subprocess.check_output("mc share upload minio/test/"+FIN, shell=True)
# # # print(result)
# # print(re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)<FILE>", str(result))[0])

