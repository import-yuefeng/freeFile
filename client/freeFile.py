#!/usr/bin/env python3
# @File:freeFile.py
# @Date:2018/10/22
# @Update:2018/12/04
# Author:Cat.1

import os
import sh
import sys
import copy
import json
import getopt
import requests
import argparse
import subprocess
sys.path.append('..')
from client import initConfig
from client.API.ApplyApi import ApplyApi
from client.API.PullArchive import PullArchive
from client.API.PushArchive import PushArchive
from client.API.CreateArchive import CreateArchive



class freeFile(object):
    """介绍

    freeFile是一个旨在帮助在多台计算机中快速共享某个(s)文件/目录的terminal程序
    基于Python3开发, 暂时只运行于类Unix操作系统上.

    未来将支持Windows系统.
    
    感谢@yifan Gao 学长提供的灵感.

    建立在高效的对象存储[Object storage service](minio)之上.


    Introduction

    freeFile is a terminal program designed to help quickly share a (s) file/directory across multiple computers.
    Based on Python3 development, it only runs on Unix-like operating systems for the time being.

    The future will support Windows systems.
    
    Thanks to @yifan Gao for the inspiration provided by the senior.

    Built on the Object storage service(minio).

    """
    OSINFOCMD = "uname -a"
    OSSSERVERURLDEFULT = "http://115.238.228.39:32771"



    def __init__(self):
        """init Function
        
        Initialize the necessary data.
        Initialization parameters, configuration files, OSS configuration information, 
        Argument command line parameters        
        """
        initConfig.initConfig()
        self.initArgument()
        self.initCommand()
        initConfig.CheckDependency(self.notcheck)


    def initArgument(self):
        configDict = initConfig.ReturnConfig()

        self.nameSpace = configDict["nameSpace"]
        self.hostName = configDict["hostName"]
        self.OSSSERVERURL = configDict["OSSSERVERURL"]

        self.name, self.FIN = [None for i in range(0, 2)]



    def initCommand(self):
        """init Function
        
        Initialize the parameters read by argoarse.
        """        

        parser = argparse.ArgumentParser(description='Welcome to use freeFile! Please check the options currently supported by freeFile\n')  
        parser.add_argument("-i", "--source",  dest = "filePath", help = "File location to upload")
        parser.add_argument("-n", "--name", dest = "name", help = "Use FIN/nameSpace to Upload/Download files")
        parser.add_argument("-t", "--time", dest = "time", help = "Set file expiration time")
        parser.add_argument("-e", "--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")
        parser.add_argument('push', action='store_true', help='Upload the file to the oss server')
        parser.add_argument('pull', action='store_true', help='Download files from oss server')
        parser.add_argument('-q', "--quiet", dest = "quiet", action='store_true', help='Run freeFile quietly')
        parser.add_argument('-qr', "--qrcode", dest = "qrcode", action='store_true', help='Need to output download QRcode')
        parser.add_argument('-nc', "--notcheck", dest = "notcheck", action='store_true', help='Do not check dependencies')

        try:
            # The first command must be push/pull or it will return help information
            # Will report an error if no parameters are used
            sys.argv[1]
        except IndexError:
            parser.parse_args(["-h"])
            exit(1)
        except:
            print("\033[1;31;40m[ERROR]\033[0m Not Know Error\n\033[1;35m[WARNING]\033[0m Please input: ff push/pull or --help/-h [Arguments]")
        else:
            self.action = sys.argv[1]

            if self.action != '-h':
                args = parser.parse_args(list(sys.argv[2:]))
                self.filePath = args.filePath
                if self.action == 'pull':
                    if "/" in args.name:
                        self.nameSpace = args.name
                    else:
                        self.name = args.name
                        self.FIN = args.name
                else:
                    self.name = args.name
                # When pull to local, both FIN and name should be arguments to args.name
                self.expiredTime = args.time
                self.encrypt = args.encrypt
                self.qrcode = args.qrcode
                self.quiet = args.quiet

                self.notcheck = args.notcheck
            else:
                parser.parse_args(["-h"])
                exit(1)



    def CheckCommand(self):
        if self.action == "push":

            return "push"
        elif self.action == "pull":
            self.FIN = self.name
            return "pull"



    def CreateOsInfoHash(self):

        osInfoHash = hashlib.sha256(subprocess.check_output("uname -a", shell=True)).hexdigest()
        return osInfoHash






    def main(self):
        if self.CheckCommand() == "push":
            self.FIN, archiveFileName = CreateArchive(self.hostName, self.filePath, self.name)
            if self.name != None:
                self.nameSpace = self.nameSpace+"/"+self.name
            else:
                self.nameSpace = self.nameSpace+"/"+self.FIN[:6]

            shareUrl = ApplyApi("push", self.expiredTime, self.FIN, self.name, self.OSSSERVERURL, self.nameSpace, self.filePath)
            PushArchive(shareUrl, archiveFileName, self.quiet)

            if self.qrcode == True:

                print("↓↓↓↓↓↓ Download QRcode ↓↓↓↓↓↓")
                print(sh.qrencode("-o", "-", "-t", "UTF8", "-s", "3", "%s"%(ApplyApi("pull", self.expiredTime, self.FIN, self.name, self.OSSSERVERURL, self.nameSpace, self.filePath))))

        elif self.CheckCommand() == "pull":

            downloadUrl = ApplyApi("pull", self.expiredTime, self.FIN, self.name, self.OSSSERVERURL, self.nameSpace, self.filePath)

            PullArchive(downloadUrl, self.name, self.quiet)

        else:

            print("\033[1;35m[WARNING]\033[0m Not know Args!")





if __name__ == '__main__':
    test = freeFile()
    test.main()



