#!/usr/bin/env python3
# @File:freeFile.py
# @Date:2018/10/22
# Author:Cat.1

import os
import sys
import oss2
import copy
import json
import time
import getopt
import hashlib
import argparse
import subprocess
try:import configparser
except:from six.moves import configparser 


class freeFile(object):
    """介绍

    freeFile是一个旨在帮助在多台计算机中快速共享某个(s)文件/目录的terminal程序
    基于Python3开发, 运行于类Unix操作系统terminal上.
    
    感谢@yifan Gao 学长提供的灵感.

    建立在高效的对象存储[Object storage service]之上.

    """
    OSINFOCMD = "uname -a"

    def __init__(self):
        """init Function
        
        初始化/检查配置文件
        """
        if os.path.exists("/etc/freeFile/ff.conf"):
            print("\033[1;32m[SUCCESS]\033[0m Find the configFile Success!")
            name = ConfigRead().getConfig("[baseConfig]", "name")
            OSS_Choice = ConfigRead().getConfig("[baseConfig]", "OSS_Choice")

        else:
            print("\033[1;35m[WARNING]\033[0m Not find configFile!")
            print("\033[1;32m[CONFIGURE]\033[0m Please configure your configFile!")
            name = input("\033[1;32m[INPUT]\033[0m yourName[default HostName]: ")
            OSS_Choice = input("\033[1;32m[CHOOSE]\033[0m [1]. AliYun(default)\n[2]. Amazon S3\n[3]. Google Cloud")

            writeConfiger = open("/etc/freeFile/ff.conf")
            writeConfiger.write("""[baseConfig]\n
                                    # baseConfigure\n
                                    name=%s\n
                                    OSS_Choice=%s\n
                                    encrypt=no\n
                                    """ %(name, OSS_Choice))
            writeConfiger.close()

    def checkCommand(self):
        if self.action == "push":

        elif self.action == "pull":

        else:
            print("\033[1;31;40m[ERROR]\033[0m Not understand your command\nPlease input: ff push/pull ...")
            return -1


    def initArgument(self):
        """init Function
        
        初始化argoarse读入的参数.
        """        

        parser = argparse.ArgumentParser(description='Usage under args.')  
        parser.add_argument("-f", dest = "filePath", help = "FilePath" )
        parser.add_argument("--name", dest = "name", help = "Update/Download use FIN.tar.bz2 or name.tar.bz2")
        parser.add_argument("-t", dest = "time", help = "File/directory expired time")
        parser.add_argument("--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")
        parser.add_argument('push', action='store_true', help='push file to oss service')
        parser.add_argument('pull', action='store_true', help='pull file from oss service')

        self.action = sys.argv[1]

        args = parser.parse_args(list(sys.argv[2:]))
        self.filePath = args.filePath
        self.name = args.name
        self.expiredTime = args.time
        self.encrypt = args.encrypt


    def initAliYun(self):
        """init Function
        
        初始化AliYun OSS配置.
        """

        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        self.auth = oss2.Auth("LTAI8pObJoHkFDYW", "wiI200gyXQ3PnUl85TV64EYd3T1MtH")
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(self.auth, "http://oss-cn-hangzhou.aliyuncs.com", "catone")
        self.baseUrl = "https://catone.oss-cn-hangzhou.aliyuncs.com/"


    def encodeToBin(self, s):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

    def decodeFromBin(self, s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

    def CheckName(self) -> bool:
        return (self.name != None)
    
    def CheckPathVaild(self, path) -> bool:
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
        jsonVersion = []
        if self.CheckPathVaild(Path):
            # 检查要上传的文件的位置是否正确
            if not self.CheckName():
                # 如果文件名不存在, 则自动生成新的文件名hash
                
                self.name = self.CreateFileIdentificationName()

            subprocess.check_output("tar -jcvf " + self.name + ".tar.bz2 " + Path, shell=True)

        self.archiveFileName = self.name + ".tar.bz2"


    def PullArchive(self):
        try:
            subprocess.check_output("wget -q " + self.baseUrl+(self.name), shell=True)
        except:
            print("\033[1;31;40m[ERROR]\033[0m Not found file from OSS Service")
        else:
            subprocess.check_output("pv " + self.name + " | tar xvf ./", shell=True)
            subprocess.check_output("rm -f " + self.name, shell=True)



    def PushArchive(self) -> bool:

        try:
            with open(self.archiveFileName, 'rb') as fileobj:
                fileobj.seek(0, os.SEEK_SET)
                current = fileobj.tell()
                self.bucket.put_object(self.archiveFileName, fileobj)

        except:
            print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")
        else:
            print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+self.archiveFileName)
            subprocess.check_output("rm -f " + self.archiveFileName, shell=True)


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
        # 先只考虑只传一个文件/目录的情况
        try:
            self.fileHash = hashlib.sha256(open(Path,'rb').read()).hexdigest()
            # 尝试读取文件，生成fileHash
        except FileNotFoundError:

            print("\033[1;31;40m[ERROR]\033[0m No such file or directory")

            exit(1)
        else:
            self.timestamp = str(int(time.time()))
            osInfoHash = hashlib.sha256(subprocess.check_output("uname -a", shell=True)).hexdigest()
            self.FIN = hashlib.sha256((self.fileHash + self.timestamp + osInfoHash).encode("utf-8")).hexdigest()

            print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+self.FIN)

            if self.name == None:
                self.name = self.FIN
            return self.FIN

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

