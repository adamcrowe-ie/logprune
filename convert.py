# This program will convert logrotate style logs into compressed logs

from main import *


def run():
    if "--test" in sys.argv:
        testUnit = TestSuite.TestUnit("convert")
        for directory in testUnit.directoriesToTest:
            try:
                print "Testing Directory " + directory
                convert(directory)
            except:
                testUnit.testFailure(directory)

    else:
        convert()



def convert(directory = PATH):
    for logLevel in LOGLEVELS:

        indexes = listLogIndexes(logLevel, directory)
        lowestIndex, highestIndex = indexes[0], indexes[-1]

        for fileName, filePath in listLogArchives(logLevel, directory):
            if ".gz" not in fileName:
                # open the original file
                with open(filePath, "rb+") as unzippedFile:

                    newIndex = highestIndex + lowestIndex - index(filePath)

                    zippedFilePath = os.path.join(PATH, "{0}.log.{1}.gz").format(logLevel, newIndex)

                    with gzip.open(zippedFilePath, "wb") as zippedFile:
                        unzippedRaw = unzippedFile.read()
                        zippedFile.write(unzippedRaw)

                    # delete the original file
                    os.remove(filePath)


if __name__ == "__main__":
    run()