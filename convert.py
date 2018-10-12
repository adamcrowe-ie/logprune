# This program will convert logrotate style logs into compressed logs

import sys, main, os, gzip, TestSuite

from config import *


def run():
    if "--test" in sys.argv:
        testUnit = TestSuite.TestUnit("convert")
        for directory in testUnit.directoriesToTest:
            try:
                print "Testing Directory " + directory
                convert(directory)
            except:
                testUnit.testFailure(directory)
        testUnit.checkOutcomes()
    else:
        convert()



def convert(directory = PATH):
    for logLevel in LOGLEVELS:

        indexes = main.listLogIndexes(logLevel, directory)
        if len(indexes) > 0:
            lowestIndex, highestIndex = indexes[0], indexes[-1]

        for fileName, filePath in main.listLogArchives(logLevel, directory):
            if ".gz" not in fileName:

                # open the original file
                with open(filePath, "rb+") as unzippedFile:

                    newIndex = highestIndex + lowestIndex - main.index(filePath)
                    zippedFileName = "{0}.log.{1}.gz".format(logLevel, newIndex)
                    zippedFilePath = os.path.join(directory, zippedFileName)

                    with gzip.open(zippedFilePath, "wb") as zippedFile:
                        unzippedRaw = unzippedFile.read()
                        zippedFile.write(unzippedRaw)

                # delete the original file
                os.remove(filePath)


if __name__ == "__main__":
    run()