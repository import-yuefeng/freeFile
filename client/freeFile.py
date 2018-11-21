#!/usr/bin/env python3
# @File:freeFile.py
# @Date:2018/10/22
# Author:Cat.1

import os
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
    基于Python3开发, 暂时只运行于类Unix操作系统terminal上.

    未来将支持Windows.
    
    感谢@yifan Gao 学长提供的灵感.

    建立在高效的对象存储[Object storage service]之上.

    """
    OSINFOCMD = "uname -a"



    def __init__(self):
        """init Function
        
        初始化必要数据.
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
            # 用户传入了流文件到freeFile中
            writeStreamFile.writelines(streamLine)
            self.StreamFileFlag = 1
        writeStreamFile.close()


    def initArgument(self):
        self.name, self.FIN, self.nameSpace, self.hostName = [None for i in range(0, 4)]

    def initConfig(self):
        """init Function
        
        初始化/检查freeFile配置文件
        """

        if os.path.exists("/etc/freeFile/ff.conf"):
            try:
                print("\033[1;32m[SUCCESS]\033[0m Find the configFile Success!")
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
            # 生成新的配置文件后再次递归调用来读取配置文件
            self.initConfig()

    def initCommand(self):
        """init Function
        
        初始化argoarse读入的参数.
        """        

        parser = argparse.ArgumentParser(description='Usage under args.')  
        parser.add_argument("-i", "--source",  dest = "filePath", help = "FilePath")
        parser.add_argument("-n", "--name", dest = "name", help = "Update/Download use FIN or nameSpace")
        parser.add_argument("-t", "--time", dest = "time", help = "File/directory expired time")
        parser.add_argument("-e", "--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")
        parser.add_argument('push', action='store_true', help='push file to oss service')
        parser.add_argument('pull', action='store_true', help='pull file from oss service')
        parser.add_argument('-q', "--quiet", action='store_true', help='quiet run freeFile')

        try:
            # 首个指令必须为 push/pull
            sys.argv[1]
        except IndexError:
            print("\033[1;31;40m[ERROR]\033[0m Not understand your command\n\033[1;35m[WARNING]\033[0m Please input: ff push/pull [Arguments]")
            exit(1)
        except:
            pass
        else:
            self.action = sys.argv[1]
            args = parser.parse_args(list(sys.argv[2:]))
            self.filePath = args.filePath
            if sys.argv[1] == 'pull':
                if "/" in args.name:
                    self.nameSpace = args.name
                else:
                    self.name = args.name
            else:
                self.name = args.name
            # 在pull到本地时，FIN和name都应该是args.name的参数
            self.expiredTime = args.time
            self.encrypt = args.encrypt


    def initOSS(self):
        """init Function
        
        初始化OSS配置.
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
        else:
            return 3
            # print("\033[1;31;40m[ERROR]\033[0m Not understand your command\nPlease input: ff push/pull ...")
            # exit(1)

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
        print(shareUrl)
        try:
            subprocess.check_output(shareUrl + self.archiveFileName, shell=True)
        except:
            print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")
        else:
            print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+self.archiveFileName)
            subprocess.check_output("rm -f " + self.archiveFileName, shell=True)

    def CreateArchive(self) -> str:
        """创建上传文件的归档文件格式函数
        
        创建需要上传文件的归档文件
        """
        Path = self.filePath

        if self.CheckPathVaildIsError(Path):
            # 检查要上传的文件的位置是否正确
            if self.CheckNameIsNone():
                # 如果文件名不存在, 则自动生成新的文件名hash
                # 自动解包生成的FIN和name
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
        
        创建一个文件的FIN值.
        用户没有指定FIN, 则利用文件内容和当前时间以及本机数据生成一个随机hash值为文件的FIN.
        利用该FIN值来实现
        '''
        Path = self.filePath

        print("\033[1;35m[WARNING]\033[0m No FIN is specified, it will be generated automatically!")
        # 输出告警, 标志没有自定义FIN则自动生成一个.
        # 先只考虑同时只传一个文件的情况
        try:
            # 尝试读取文件，生成fileHash
            fileHash = self.CreateFileHash()

        except FileNotFoundError:
            print("\033[1;31;40m[ERROR]\033[0m No such file or directory")
            exit(1)

        else:
            self.FIN = self.CreateFIN()
            if self.name == None:
                self.name = self.hostName + "/" +self.FIN[:6]
                # 如果用户不指定nameSpace，则认为nameSpace就是FIN
            print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+self.FIN)
            print("\033[1;32m[INFO]\033[0m Use FIN pull file: "+self.FIN)
            print("\033[1;32m[INFO]\033[0m Use nameSPace pull file: "+self.name)


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
            #  用户发起了push 请求
            self.CreateArchive()
            self.PushArchive()
        elif self.CheckCommand() == 2:
            # 用户发起了pull 请求
            self.PullArchive()
        else:
            print("\033[1;35m[WARNING]\033[0m Not know Args!")


class ConfigRead(object):

    # 获取config配置文件
    # 类方法，第一参数默认传入cls，可被类/实例调用
    @classmethod
    def getConfig(cls, section, key):
        config = configparser.ConfigParser()
        path = '/etc/freeFile/ff.conf'
        config.read(path)
        return config.get(section, key)


if __name__ == '__main__':
    test = freeFile()
    test.main()

