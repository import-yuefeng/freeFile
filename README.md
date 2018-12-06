# freeFile

freeFile is still in the early development, if there is any doubt, please mention Issue.

freeFile 还在早期开发中, 如果使用有疑问, 请提起Issue.

*************
freeFile
*************
![Python3.6.4](https://img.shields.io/badge/Python-3.6.4-green.svg)

![gitlab-ci](https://img.shields.io/badge/Gitlab-ci-red.svg)

![MIT](https://img.shields.io/badge/MIT-red.svg)

![freeFile](https://img.shields.io/badge/freeFile-0.1.0-red.svg)

freeFile is a terminal program designed to help quickly share a (s) file/directory across multiple computers.

Based on Python3 development, *it only runs on Unix-like operating systems for the time being.*



freeFile是一个旨在帮助在多台计算机中快速共享某个(s)文件/目录的terminal程序.

基于Python3开发, 暂时只运行于类Unix操作系统上.

未来将支持Windows系统, 并将兼容Python2.7.

建立在高效的对象存储[Object storage service] (minio)之上.

Quickstart
===========

Add freeFile to your computer. The following example uses the default.

in OSS implementation for storage.



.. code-block:: bash

```bash
$ pip install pip -U 

$ sudo pip install --no-cache-dir freeFile

$ touch test.txt

$ ls
test.txt

$ ff push -i test.txt -n config

$ rm test.txt

$ ls

$ ff pull -n nickName/config

$ ls
test.txt


```


