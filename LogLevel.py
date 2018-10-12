
from main import *

class LogLevel:
    def __init__(self, levelName, directory):
        self.levelName = levelName
        self.unzippedFilePath = os.path.join(directory, levelName + ".log")
        self.zippedFiles = []
        self.totalZippedSize = 0

        # add each zipped file of the logLevel to the list 'zippedFiles'
        for fileName, filePath in listLogArchives(levelName, directory):
            if ".gz" in fileName:
                self.addZippedFile(filePath)

    def addZippedFile(self, filePath):
        self.zippedFiles.append({
            "path": filePath,
            "size": size(filePath),
            "index": index(filePath)
        })
        self.totalZippedSize += size(filePath)  # add the size to the total size of zipped logs
        self.zippedFiles.sort(key=lambda x: x["index"])  # sort list by index
