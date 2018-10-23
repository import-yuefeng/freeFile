#!/usr/bin/env python3
# @File:freeFile.py
# @Date:2018/10/22
# Author:Cat.1

import os
import oss2
import json
import time
import hashlib
import argparse
import subprocess
import config


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
        
        初始化argoarse读入的参数.
        """

        parser = argparse.ArgumentParser()        
        parser.add_argument("-f", dest = "filePath", help = "FilePath" )
        parser.add_argument("-d", dest = "directoryPath", help = "directoryPath")
        parser.add_argument("--name", dest = "name", help = "Update/Download FIN(File identification name)")
        parser.add_argument("-t", dest = "time", help = "File/directory expired time")
        parser.add_argument("--encrypt", dest = "encrypt", help = "If you need a private access file/directory, please give your gpg public key location")

        args = parser.parse_args()
        self.filePath = args.filePath
        self.directoryPath = args.directoryPath
        self.name = args.name
        self.expiredTime = args.time
        self.encrypt = args.encrypt

        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        self.auth = oss2.Auth('LTAI8pObJoHkFDYW', 'wiI200gyXQ3PnUl85TV64EYd3T1MtH')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(self.auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'catone')


    def encodeToBin(self, s):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

    def decodeFromBin(self, s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

    def CheckName(self) -> bool:
        return (self.name != None)
    
    def CheckPathVaild(self, path) -> bool:
        try:
            os.path.exists(path)
        except TypeError:
            return False
        else:
            return True

    def CreateArchive(self) -> str:
        Path = self.filePath

        if self.CheckPathVaild(Path):
            if not self.CheckName():
                self.CreateFileIdentificationName()

            subprocess.check_output("tar -jcvf " + self.name + ".tar.bz2 " + Path, shell=True)

        self.archiveFileName = self.name + ".tar.bz2"


    def PullArchive(self):
        url = "https://catone.oss-cn-hangzhou.aliyuncs.com/"


    def PushArchive(self) -> bool:

        # 必须以二进制的方式打开文件，因为需要知道文件包含的字节数
        try:
            with open(self.archiveFileName, 'rb') as fileobj:
                fileobj.seek(0, os.SEEK_SET)
                current = fileobj.tell()
                self.bucket.put_object(self.archiveFileName, fileobj)
        except:
            print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")
        else:
            print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+self.archiveFileName)
            subprocess.check_output("rm -f "+ self.archiveFileName, shell=True)




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
            fileHash = hashlib.sha256(open(Path,'rb').read()).hexdigest()
        except FileNotFoundError:
            print("\033[1;31;40m[ERROR]\033[0m No such file or directory")
            exit(1)
        else:
            timestamp = str(int(time.time()))
            osInfoHash = hashlib.sha256(subprocess.check_output("uname -a", shell=True)).hexdigest()

            FIN = hashlib.sha256((fileHash + timestamp + osInfoHash).encode("utf-8")).hexdigest()
            print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+FIN)
            self.name = FIN

    def main(self):
        self.CreateArchive()
        self.PushArchive()


if __name__ == '__main__':
    test = freeFile()
    test.main()
















    