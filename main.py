# This program is designed to act as a replacement to the Logrotate
# program (https://linux.die.net/man/8/logrotate). Like Logrotate, is used for maintaining logs
# of the

# The behaviour of this program is as follows:
# -- Iterate through each logLevel
# ------ If the current log of the logLevel exceeds 1MB
# ---------- Compress the file and save it with the next available index
# ---------- While the total size of the compressed files > 300MB
# -------------- Delete the compressed file with the lowest index


import os, gzip, time, sys, TestSuite, convert, LogLevel

from config import *
from TestSuiteConfig import *


def main():
    if "--convert" in sys.argv:
        convert.run()
    if "--test" in sys.argv:
        testUnit = TestSuite.TestUnit("main")
        for directory in testUnit.directoriesToTest:
            try:
                print "Testing Directory " + directory
                processLogs(directory, TESTING_UNZIPPED_SIZE_LIMIT, TESTING_ZIPPED_SIZE_LIMIT)
            except:
                testUnit.testFailure(directory)
        testUnit.checkOutcomes()
    else:
        while True:
            processLogs()
            time.sleep(INTERVAL)


def processLogs(directory=PATH,
                unzippedSizeLimit=UNZIPPED_SIZE_LIMIT,
                zippedSizeLimit=ZIPPED_SIZE_LIMIT):

    # create list of LogLevel objects
    # this is re-calibrated on each run in case files were modified externally, in which case the
    # information in the objects would be incorrect
    logLevelObjects = [LogLevel.LogLevel(levelName, directory) for levelName in LOGLEVELS]

    for logLevel in logLevelObjects:  # iterate through the list
        if size(logLevel.unzippedFilePath) > unzippedSizeLimit:
            with open(logLevel.unzippedFilePath, "rb") as unzippedFile:

                # get the index by taking the last index of the sorted list and adding one
                index = 1 if logLevel.zippedFiles == [] else logLevel.zippedFiles[-1]["index"] + 1
                zippedFilePath = logLevel.unzippedFilePath + "." + str(index) + ".gz"

                # create the zipped file and write to it
                with gzip.open(zippedFilePath, "wb+") as zippedFile:
                    zippedFile.write(unzippedFile.read())

                logLevel.addZippedFile(zippedFilePath)

            with open(logLevel.unzippedFilePath, "wb") as unzippedFile:
                unzippedFile.write("")  # delete the contents of the unzipped file

            while totalSize(logLevelObjects) > zippedSizeLimit:

                # find the largest log level by sorting the list by the 'totalzippedsize'
                # attribute and taking the last element
                largestLogLevel = sorted(logLevelObjects, key=lambda x: x.totalZippedSize)[-1]
                fileToDelete = largestLogLevel.zippedFiles[0]  # find the lowest indexed file

                # recalculate the size of logLevel
                largestLogLevel.totalZippedSize -= size(fileToDelete["path"])
                os.remove(fileToDelete["path"])  # delete the file
                largestLogLevel.zippedFiles.pop(0)  # remove it from the list of files


def size(filePath):
    return int(os.stat(filePath).st_size)  # finds the size of a file


def totalSize(logLevelObjects):
    # sums the 'totalZippedSize' attribute of each logLevel
    return sum([logLevel.totalZippedSize for logLevel in logLevelObjects])


def index(filePath):
    for substr in filePath.split("."):
        if substr.isdigit(): return int(substr)
    return 0


def listLogIndexes(logLevel, directory):
    indexes = []
    for fileName, filePath in listLogArchives(logLevel, directory):
        if index(filePath) != 0:
            indexes.append(index(filePath))
    return sorted(indexes)


def listLogArchives(logLevel, directory):
    for fileName in os.listdir(directory):
        if logLevel in fileName and any(ch.isdigit() for ch in fileName):
            yield (fileName, os.path.join(directory, fileName))


if __name__ == "__main__":
    main()