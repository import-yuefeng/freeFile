import time
import requests

def GetOriginFileName(filePath):
    Path = filePath
    if '/' in Path:
        OriginFileName = Path.split("/")[-1]
        return OriginFileName
    else:
        OriginFileName = Path
        return OriginFileName


def ApplyApi(target, expiredTime, FIN, name, OSSSERVERURL, nameSpace, filePath):


    if target == 'push':

        headers = {
                    "AccessToken":"ThisIsATest"
                }
        timestamp = str(int(time.time()))
        if expiredTime == None:
            expiredTime = '72h'

        response = requests.get(url=OSSSERVERURL+'/applyupload?&FIN=%s&time=%s&expired=%s&nameSpace=%s&fileName=%s'%(
            FIN+"tar.gz", timestamp, expiredTime, nameSpace, GetOriginFileName(filePath)), headers=headers)

        responseJson = response.json()

        if responseJson["statusCode"] != 200:
            print("\033[1;31;40m[ERROR]\033[0m %s"%responseJson["message"])
            print("\033[1;31;40m[statusCode]\033[0m %s"%responseJson["statusCode"])
            exit(1)
        else:
            return responseJson["shareUrl"]

    elif target == 'pull':

        if expiredTime == None:
            expiredTime = '24h'
        timestamp = str(int(time.time()))

        if "/" in nameSpace:
            response = requests.get(url=OSSSERVERURL+'/applydownload?&FIN=%s&time=%s&expired=%s&nameSpace=%s'%(
                "tar.gz", timestamp, expiredTime, nameSpace))

        else:

            response = requests.get(url=OSSSERVERURL+'/applydownload?&FIN=%s&time=%s&expired=%s&nameSpace=None'%(
                FIN+"tar.gz", timestamp, expiredTime))

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
