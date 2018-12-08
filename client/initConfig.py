import os
try:import configparser
except:from six.moves import configparser 
import socket
import subprocess




class ConfigRead(object):

    # Get config configuration file
    # Class method, the first parameter is passed to cls by default, which can be called by class/instance
    @classmethod
    def getConfig(cls, section, key):
        config = configparser.ConfigParser()
        path = '/etc/freeFile/ff.conf'
        config.read(path)
        return config.get(section, key)



def ReturnConfig():

    hostName = socket.gethostname()
    nameSpace = ConfigRead().getConfig("baseConfig", "name")
    OSS_Choice = ConfigRead().getConfig("baseConfig", "OSS_Choice")
    encryptBool = ConfigRead().getConfig("baseConfig", "encrypt")
    OSSSERVERURL = ConfigRead().getConfig("baseConfig", "OSSSERVERURL")

    return {
            "hostName":hostName, 
            "nameSpace":nameSpace, 
            "OSS_Choice":OSS_Choice, 
            "encryptBool":encryptBool, 
            "OSSSERVERURL":OSSSERVERURL
            }


def initConfig():
    """init Function
    
    Initialize/check the freeFile configuration file.
    """
    

    OSSSERVERURLDEFULT = "http://115.238.228.39:32771/v1"

    try:
        if os.path.exists("/etc/freeFile/ff.conf"):
            try:
                print("\033[1;32m[SUCCESS]\033[0m Find the configFile Success!")
                print("\033[1;37m[INFO]\033[0m configFile in /etc/freeFile/ff.conf")
            except IndexError:
                print("\033[1;31;40m[ERROR]\033[0m Read config Error!")
                subprocess.check_output("rm /etc/freeFile/ff.conf", shell=True)
                exit(1)
        else:
            print("\033[1;35m[WARNING]\033[0m Not find configFile!")
            print("\033[1;32m[CONFIGURE]\033[0m Please configure your configFile!")
            name = input("\033[1;32m[INPUT]\033[0m yourName[default HostName]: ")
            OSS_Choice = input("\033[1;32m[CHOOSE]\033[0m Input your Choose\n[1]. Minio(default) [2]. AliYun\n[3]. Amazon S3 [4]. Google Cloud\nYour Choose: ")
            OSSSERVERURL = input("\033[1;32m[INPUT]\033[0m Your OSS SERVER URL:[default Official]: ")

            if name == "\n" or name == "":
                name = socket.gethostname()
            elif OSS_Choice == '\n' or OSS_Choice == '':
                OSS_Choice = "Minio"
            elif OSSSERVERURL == '\n' or OSSSERVERURL == '':
                OSSSERVERURL = OSSSERVERURLDEFULT
            try:
                subprocess.check_output("sudo mkdir /etc/freeFile", shell=True)
            except subprocess.CalledProcessError:
                print("\033[1;35m[WARNING]\033[0m /etc/freeFile exists!")
            subprocess.check_output("sudo touch /etc/freeFile/ff.conf", shell=True)     
            subprocess.check_output("sudo chmod -R 777 /etc/freeFile/", shell=True)

            writeConfiger = open("/etc/freeFile/ff.conf", "w")
            writeConfiger.write("[baseConfig]\nname=%s\nOSS_Choice=%s\nencrypt=no\nOSSSERVERURL=%s" %(name, OSS_Choice, OSSSERVERURL))
            writeConfiger.close()
            print("\033[1;32m[SUCCESS]\033[0m Configure Success!")
            # Recursive call to read the configuration file after generating a new \
            # configuration file
            initConfig()
    except KeyboardInterrupt:
        print("\n")
        print("\033[1;31;40m[ERROR]\033[0m User active exit!")
        exit(1)




