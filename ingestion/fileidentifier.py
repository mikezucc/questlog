imageFileTypes = ["jpeg", "jpg", "png"]
soundFileTypes = ["mp3", "wav", "flac", "raw", "m4a", "aac", "iso"]
textFileTypes = ["json","txt", "ascii", "text"]

def determineSimpleType(filepathURI):
    # should find a safer solution to reading, buffer may be overflow
    with open(filepathURI, 'r') as openFile:
        fileTypeMagic = magic.from_buffer(openFile.read(1024))

        splitFileType = fileTypeMagic.split(',')
        print splitFileType
        slugFileType = splitFileType[0].split(' ')[0].lower()
        print slugFileType

        try:
            print "checking " + slugFileType + " against "
            print imageFileTypes
            if imageFileTypes.index(slugFileType) != None:
                print "ISSA IMAGE BITCH HA HA"
                return "image"
        except:
            print "not an image"

        try:
            if soundFileTypes.index(slugFileType):
                print "ISSA SOUND BITCH HA HA"
                return "sound"
        except:
            print "not an soundfile"

        openFile.close()
    return "generic"

def determineSimpleFormat(filepathURI):
    # should find a safer solution to reading, buffer may be overflow
    with open(filepathURI, 'r') as openFile:
        fileTypeMagic = magic.from_buffer(openFile.read(1024))

        splitFileType = fileTypeMagic.split(',')
        print splitFileType
        slugFileType = splitFileType[0].split(' ')[0].lower()
        print slugFileType

        try:
            print "checking " + slugFileType + " against "
            print imageFileTypes
            if imageFileTypes.index(slugFileType) != None:
                print "ISSA IMAGE BITCH HA HA"
                return slugFileType
        except:
            print "not an image"

        try:
            if soundFileTypes.index(slugFileType):
                print "ISSA SOUND BITCH HA HA"
                return slugFileType
        except:
            print "not an soundfile"

        openFile.close()
    return "generic"
