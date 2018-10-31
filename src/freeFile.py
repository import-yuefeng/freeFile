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
# from minio import Minio
try:import configparser
except:from six.moves import configparser 
# from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
#                          BucketAlreadyExists)


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
        self.initArgument()
        self.initConfig()
        self.initOSS()


    def initConfig(self):
        """init Function
        
        初始化/检查freeFile配置文件
        """
        if os.path.exists("/etc/freeFile/ff.conf"):
            print("\033[1;32m[SUCCESS]\033[0m Find the configFile Success!")
            self.hostName = ConfigRead().getConfig("[baseConfig]", "name")
            self.OSS_Choice = ConfigRead().getConfig("[baseConfig]", "OSS_Choice")
            self.encryptBool = ConfigRead().getConfig("[baseConfig]", "encrypt")


        else:
            print("\033[1;35m[WARNING]\033[0m Not find configFile!")
            print("\033[1;32m[CONFIGURE]\033[0m Please configure your configFile!")
            name = input("\033[1;32m[INPUT]\033[0m yourName[default HostName]: ")
            OSS_Choice = input("\033[1;32m[CHOOSE]\033[0m [1]. Minio(default)\n [2]. AliYun\n[3]. Amazon S3\n[4]. Google Cloud")
            if name == "\n":
                name = socket.gethostname()
            elif OSS_Choice == '\n':
                OSS_Choice = "Minio"

            writeConfiger = open("/etc/freeFile/ff.conf")
            writeConfiger.write("""[baseConfig]\n
                                    # baseConfigure\n
                                    name=%s\n
                                    OSS_Choice=%s\n
                                    encrypt=no\n
                                    """ %(name, OSS_Choice))
            writeConfiger.close()
            # 生成新的配置文件后再次递归调用来读取配置文件
            self.initConfig()


    def initArgument(self):
        """init Function
        
        初始化argoarse读入的参数.
        """        

        parser = argparse.ArgumentParser(description='Usage under args.')  
        parser.add_argument("-i", "--source",  dest = "filePath", help = "FilePath")
        parser.add_argument("-n", "--name", dest = "name", help = "Update/Download use FIN or name")
        parser.add_argument("-t", "--time", dest = "time", help = "File/directory expired time")
        parser.add_argument("-e", "--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")
        parser.add_argument('push', action='store_true', help='push file to oss service')
        parser.add_argument('pull', action='store_true', help='pull file from oss service')
        parser.add_argument('-q', "--quiet", action='store_true', help='quiet run freeFile')
        self.action = sys.argv[1]

        args = parser.parse_args(list(sys.argv[2:]))
        self.filePath = args.filePath
        self.name = args.name
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
            return 2
        else:
            print("\033[1;31;40m[ERROR]\033[0m Not understand your command\nPlease input: ff push/pull ...")
            exit(1)

    def CheckNameIsNone(self) -> bool:
        return (self.name == None)
    
    def CheckPathVaildIsError(self, path) -> bool:
        try:
            os.access(path, os.F_OK)
        except:
            return False
        else:
            return os.access(path, os.F_OK)


    def CreateArchive(self) -> str:
        """创建上传文件的归档文件格式函数
        
        创建需要上传文件的归档文件
        """
        Path = self.filePath

        if self.CheckPathVaild(Path):
            # 检查要上传的文件的位置是否正确
            if not self.CheckName():
                # 如果文件名不存在, 则自动生成新的文件名hash
                self.CreateFileIdentificationName()
            # subprocess.check_output("tar -jcvf " + self.name + ".tar.bz2 -C" + Path, shell=True)
            sysstr = platform.system()
            # 有问题！！！！！！
            # 有问题！！！！！！
            # 有问题！！！！！！
            if(sysstr =="Windows"):
                print("\033[1;31;40m[ERROR]\033[0m freeFile not work on Windows.")
                exit(1)
            elif(sysstr == "Linux"):
                subprocess.check_output("tar -cf - %s | pv -s $(du -sb %s | awk '{print $1}') | gzip > %s.tar.gz"%(self.name, self.name, self.name), shell=True)
            else:
                subprocess.check_output("tar -cf - %s | pv -s $(($(du -sk %s | awk '{print $1}') * 1024)) | gzip > %s.tar.gz"%(self.name, self.name, self.name), shell=True)

        self.archiveFileName = self.name + ".tar.bz2"


    def PullArchive(self):
        try:
            subprocess.check_output("wget -q " + self.baseUrl+(self.name), shell=True)
        except:
            print("\033[1;31;40m[ERROR]\033[0m Not found file from OSS Service")
        else:
            subprocess.check_output("pv %s.tar.gz | tar -zxf -",%(self.name) shell=True)
            subprocess.check_output("rm -f " + self.name, shell=True)



    def PushArchive(self) -> bool:
        headers = {
                    "AccessToken":"ThisIsATest"
                }
        timestamp = str(int(time.time()))
        expired = '7d'
        response = requests.get(url='115.238.228.39:9090/applyupload&FIN=%s&time=%s&expired=%s&nameSpace=%s&fileName=%s'%(
            self.FIN, timestamp, expired, self.hostName, ), 
            headers=headers)
        responseJson = response.json()
        if responseJson["statusCode"] != 200:
            print("\033[1;31;40m[ERROR]\033[0m %s"%responseJson["message"])
            print("\033[1;31;40m[statusCode]\033[0m %s"%responseJson["statusCode"])
            exit(1)
        else:
            try:
                subprocess.check_output(responseJson["shareUrl"] + self.archiveFileName, shell=True)
            except:
                print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")
            else:
                print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+self.archiveFileName)
                subprocess.check_output("rm -f " + self.archiveFileName, shell=True)

    def CreateFIN(self):

        timestamp = str(int(time.time()))
        osInfoHash = self.CreateFileHash()
        FIN = hashlib.sha256((self.fileHash + timestamp + osInfoHash).encode("utf-8")).hexdigest()
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
            # self.fileHash = hashlib.sha256(open(Path,'rb').read()).hexdigest()
            # 尝试读取文件，生成fileHash
            fileHash = self.CreateFileHash()

        except FileNotFoundError:
            print("\033[1;31;40m[ERROR]\033[0m No such file or directory")
            exit(1)

        else:
            FIN = self.CreateFIN()

            print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+self.FIN)
            if self.name == None:
                name = self.hostName + "/" + FIN[]
            else:
                name = self.name

            return (FIN, name)

    def GetOriginFileName(self):
        Path = self.filePath
        if '/' in Path:
            self.OriginFileName = Path.split("/")[-1]
        else:
            self.OriginFileName = Path


    def main(self):
        if self.pushBool:
            self.CreateArchive()

            self.PushArchive()
        elif self.pullBool:
            self.PullArchive()




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

