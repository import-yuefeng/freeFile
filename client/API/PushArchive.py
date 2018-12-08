import subprocess



def PushArchive(uploadUrl, archiveFileName):


    try:
        subprocess.check_output(uploadUrl + archiveFileName, shell=True)
    except:
        print("\033[1;31;40m[ERROR]\033[0m OSS Service Error")

    else:
        print("\033[1;32m[SUCCESS]\033[0m Successfully push file is "+archiveFileName)

    finally:
        subprocess.check_output("rm -f " + archiveFileName, shell=True)
