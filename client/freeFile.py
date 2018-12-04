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
import time
import socket
import getopt
import hashlib
import requests
import argparse
import platform
import subprocess
try:import configparser
except:from six.moves import configparser 



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

    Built on the efficient object storage[Object storage service](minio).

    """
    OSINFOCMD = "uname -a"



    def __init__(self):
        """init Function
        
        Initialize the necessary data.
        Initialization parameters, configuration files, OSS configuration information, 
        Argument command line parameters        
        """

        # self.initStream()
        self.initArgument()
        self.initConfig()
        self.initOSS()
        self.initCommand()



    def initStream(self):

        self.StreamFileFlag = 0

        streamLine = None
        writeStreamFile = open("./tmpFile.txt", "w")

        while True:
            streamLine = sys.stdin.readline()
            if not streamLine:
                break
            # The user passed the stream file to freeFile
            writeStreamFile.writelines(streamLine)
            self.StreamFileFlag = 1
        writeStreamFile.close()



    def initArgument(self):
        self.name, self.FIN, self.nameSpace, self.hostName = [None for i in range(0, 4)]



    def initConfig(self):
        """init Function
        
        Initialize/check the freeFile configuration file.
        """

        if os.path.exists("/etc/freeFile/ff.conf"):
            try:
                print("\033[1;32m[SUCCESS]\033[0m Find the configFile Success!")
                print("\033[1;37m[INFO]\033[0m configFile in /etc/freeFile/ff.conf")
                self.hostName = ConfigRead().getConfig("baseConfig", "name")
                self.OSS_Choice = ConfigRead().getConfig("baseConfig", "OSS_Choice")
                self.encryptBool = ConfigRead().getConfig("baseConfig", "encrypt")
            except IndexError:
                print("\033[1;31;40m[ERROR]\033[0m Read config Error!")
                subprocess.check_output("rm /etc/freeFile/ff.conf", shell=True)
                exit(1)
        else:
            print("\033[1;35m[WARNING]\033[0m Not find configFile!")
            print("\033[1;32m[CONFIGURE]\033[0m Please configure your configFile!")
            name = input("\033[1;32m[INPUT]\033[0m yourName[default HostName]: ")
            OSS_Choice = input("\033[1;32m[CHOOSE]\033[0m Input your Choose\n[1]. Minio(default)\n[2]. AliYun\n[3]. Amazon S3\n[4]. Google Cloud\nYour Choose: ")
            if name == "\n":
                name = socket.gethostname()
            elif OSS_Choice == '\n' or OSS_Choice == '':
                OSS_Choice = "Minio"
            try:
                subprocess.check_output("sudo mkdir /etc/freeFile", shell=True)
            except subprocess.CalledProcessError:
                print("\033[1;35m[WARNING]\033[0m /etc/freeFile exists!")
            subprocess.check_output("sudo touch /etc/freeFile/ff.conf", shell=True)     
            subprocess.check_output("sudo chmod -R 777 /etc/freeFile/", shell=True)

            writeConfiger = open("/etc/freeFile/ff.conf", "w")
            writeConfiger.write("[baseConfig]\nname=%s\nOSS_Choice=%s\nencrypt=no\n" %(name, OSS_Choice))
            writeConfiger.close()
            print("\033[1;32m[SUCCESS]\033[0m Configure Success!")
            # Recursive call to read the configuration file after generating a new configuration file
            self.initConfig()



    def initCommand(self):
        """init Function
        
        Initialize the parameters read by argoarse.
        """        

        parser = argparse.ArgumentParser(description='Very welcome to use freeFile! Please check the options currently supported by freeFile\n')  
        parser.add_argument("-i", "--source",  dest = "filePath", help = "File location to upload")
        parser.add_argument("-n", "--name", dest = "name", help = "Use FIN/nameSpace to Upload/Download files")
        parser.add_argument("-t", "--time", dest = "time", help = "Set file expiration time")
        parser.add_argument("-e", "--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")
        parser.add_argument('push', action='store_true', help='Upload the file to the oss server')
        parser.add_argument('pull', action='store_true', help='Download files from oss server')
        parser.add_argument('-q', "--quiet", action='store_true', help='Run freeFile quietly')
        parser.add_argument('-qr', "--qrcode", dest = "qrcode", action='store_true', help='Need to output download QRcode')

        try:
            # The first command must be push/pull or it will return help information
            # Will report an error if no parameters are used
            sys.argv[1]
        except IndexError:
            print("\033[1;31;40m[ERROR]\033[0m Not understand your command\n\033[1;35m[WARNING]\033[0m Please input: ff push/pull or --help/-h [Arguments]")
            exit(1)
        except:
            pass
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
                else:
                    self.name = args.name

                # When pull to local, both FIN and name should be arguments to args.name
                self.expiredTime = args.time
                self.encrypt = args.encrypt
                self.qrcode = args.qrcode
            else:
                parser.parse_args(["-h"])

    def initOSS(self):
        """init Function
        
        Initialize the OSS configuration.
        """
        if self.OSS_Choice == "Minio":
            ip = subprocess.check_output("curl ip.sb", shell=True)
            self.ip = str(ip).split(r"\n")[0][2:]
        else:
            pass



    def CheckCommand(self):
        if self.action == "push":
            return 1
        elif self.action == "pull":
            self.FIN = self.name
            return 2



    def CheckNameIsNone(self) -> bool:
        return (self.name == None)
    


    def CheckPathVaildIsError(self, path) -> bool:
        try:
            fileBool = os.access(path, os.F_OK)
        except:
            return False
        else:
            return os.access(path, os.F_OK)



    def ApplyApi(self, target):

        if target == 'push':
            headers = {
                        "AccessToken":"ThisIsATest"
                    }
            timestamp = str(int(time.time()))
            if self.expiredTime == None:
                self.expiredTime = '24h'

            response = requests.get(url='http://115.238.228.39:9091/applyupload?&FIN=%s&time=%s&expired=%s&nameSpace=%s&fileName=%s'%(
                self.FIN+"tar.gz", timestamp, self.expiredTime, self.hostName, self.GetOriginFileName()), headers=headers)
            responseJson = response.json()
            if responseJson["statusCode"] != 200:
                print("\033[1;31;40m[ERROR]\033[0m %s"%responseJson["message"])
                print("\033[1;31;40m[statusCode]\033[0m %s"%responseJson["statusCode"])
                exit(1)
            else:
                return responseJson["shareUrl"]

        elif target == 'pull':

            if self.expiredTime == None:
                self.expiredTime = '24h'
            timestamp = str(int(time.time()))
            if self.nameSpace != None:

                response = requests.get(url='http://115.238.228.39:9091/applydownload?&FIN=%s&time=%s&expired=%s&nameSpace/fileName=%s'%(
                    self.FIN+"tar.gz", timestamp, self.expiredTime, self.nameSpace))
            else:
                response = requests.get(url='http://115.238.228.39:9091/applydownload?&FIN=%s&time=%s&expired=%s&nameSpace/fileName=None'%(
                    self.FIN+"tar.gz", timestamp, self.expiredTime))

            responseJson = response.json()
            if responseJson["statusCode"] != 200:
                print("\033[1;31;40m[ERROR]\033[0m %s"%responseJson["message"])
                print("\033[1;31;40m[statusCode]\033[0m %s"%responseJson["statusCode"])
                exit(1)
            else:
                return responseJson["shareUrl"]
        else:
            print("\033[1;31;40m[ERROR]\033[0m Request not valid.")
            exit(1)




    def PullArchive(self):
        downloadUrl = self.ApplyApi("pull")
        try:
            subprocess.check_output(["wget", downloadUrl, "-O", '{0}.tar.gz'.format(self.name)])
        except:
            print("\033[1;31;40m[ERROR]\033[0m Not found file from OSS Service")
        else:
            print("\033[1;32m[SUCCESS]\033[0m Successfully pull file is "+self.name)
            subprocess.check_output("pv %s.tar.gz | tar -zxf -"%(self.name), shell=True)
            subprocess.check_output("rm -f " + self.name + '.tar.gz', shell=True)




    def PushArchive(self) -> bool:

        shareUrl = self.ApplyApi("push")

        try:
            subprocess.check_output(shareUrl + self.archiveFileName, shell=True)
        except:
            print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")
        else:
            print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+self.archiveFileName)

        finally:
            subprocess.check_output("rm -f " + self.archiveFileName, shell=True)
            if self.qrcode == True:
                # Output when the user needs a QR code
                print("↓↓↓↓↓↓ Download QRcode ↓↓↓↓↓↓")
                print(sh.qrencode("-o", "-", "-t", "UTF8", "-s", "3", "%s"%(self.ApplyApi("pull"))))


    def CreateArchive(self) -> str:
        """Create an archive file format function for uploading files
        
        Create an archive that needs to upload files
        """
        Path = self.filePath

        if self.CheckPathVaildIsError(Path):
            # Check if the location of the file to be uploaded is correct
            if self.CheckNameIsNone():
                # If the download file identifier [name] is not specified, a new file hash, FIN, is automatically generated.
                # Automatic unpacking generated FIN and name
                self.FIN, self.name = self.CreateFileIdentificationName()


            # subprocess.check_output("tar -jcvf " + self.name + ".tar.bz2 -C" + Path, shell=True)
            sysstr = platform.system()

            if(sysstr =="Windows"):
                print("\033[1;31;40m[ERROR]\033[0m freeFile not work on Windows.")
                exit(1)

            elif(sysstr == "Linux"):
                subprocess.check_output("tar -cf - %s | pv -s $(du -sb %s | awk '{print $1}') | gzip > %s.tar.gz"%(self.filePath, self.filePath, self.FIN), shell=True)
            else:
                subprocess.check_output("tar -cf - %s | pv -s $(($(du -sk %s | awk '{print $1}') * 1024)) | gzip > %s.tar.gz"%(self.filePath, self.filePath, self.FIN), shell=True)
            
            self.archiveFileName = self.FIN + ".tar.gz"
        else:
            print("\033[1;31;40m[ERROR]\033[0m Not found file.")
            exit(1)



    def CreateFIN(self):

        timestamp = str(int(time.time()))
        osInfoHash = self.CreateFileHash()
        FIN = hashlib.sha256((osInfoHash + timestamp + osInfoHash).encode("utf-8")).hexdigest()
        return FIN


    def CreateOsInfoHash(self):

        osInfoHash = hashlib.sha256(subprocess.check_output("uname -a", shell=True)).hexdigest()
        return osInfoHash


    def CreateFileHash(self) -> str:
        Path = self.filePath
        fileHash = hashlib.sha256(open(Path,'rb').read()).hexdigest()
        return fileHash


    def CreateFileIdentificationName(self) -> str:
        '''CreateFileIdentificationName Function
        
        Create a FIN value for a file.
        If the user does not specify a FIN, the file content and the current time and the \
        local data are used to generate a random hash value for the FIN of the file.
        Use this FIN value to achieve        
        '''

        Path = self.filePath

        print("\033[1;35m[WARNING]\033[0m No FIN is specified, it will be generated automatically!")
        # Output alarm, the flag is automatically generated without a custom FIN.
        # First consider only the case where only one file is transmitted at the same time.        try:
            
        try:
            fileHash = self.CreateFileHash()
            # Try to read the file and generate fileHash
        except FileNotFoundError:
            print("\033[1;31;40m[ERROR]\033[0m No such file or directory")
            exit(1)
        else:
            self.FIN = self.CreateFIN()
            if self.name == None:
                self.name = self.hostName + "/" +self.FIN[:6]
                # If the user does not specify a nameSpace, the nameSpace is considered to be a FIN.
            print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+self.FIN)
            print("\n")
            print("\033[1;37m[INFO]\033[0m Use FIN pull file: "+"\033[1;32m"+self.FIN+"\033[0m")
            print("\033[1;37m[INFO]\033[0m Use nameSPace pull file: "+"\033[1;32m"+self.name+"\033[0m")
            print("\n")
            return (self.FIN, self.name)



    def GetOriginFileName(self):
        Path = self.filePath
        if '/' in Path:
            OriginFileName = Path.split("/")[-1]
            return OriginFileName
        else:
            OriginFileName = Path
            return OriginFileName


    def main(self):
        if self.CheckCommand() == 1:
            #  User initiated a push request
            self.CreateArchive()
            self.PushArchive()
        elif self.CheckCommand() == 2:
            # User initiated pull request
            self.PullArchive()
        else:
            # The first instruction is not push/pull to return help information
            print("\033[1;35m[WARNING]\033[0m Not know Args!")



class ConfigRead(object):

    # Get config configuration file
    # Class method, the first parameter is passed to cls by default, which can be called by class/instance
    @classmethod
    def getConfig(cls, section, key):
        config = configparser.ConfigParser()
        path = '/etc/freeFile/ff.conf'
        config.read(path)
        return config.get(section, key)



if __name__ == '__main__':
    test = freeFile()
    test.main()

