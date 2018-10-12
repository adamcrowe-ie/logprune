
import main, os

class LogLevel:
    def __init__(self, levelName, directory):
        self.levelName = levelName
        self.unzippedFilePath = os.path.join(directory, levelName + ".log")
        self.zippedFiles = []
        self.totalZippedSize = 0

        # add each zipped file of the logLevel to the list 'zippedFiles'
        for fileName, filePath in main.listLogArchives(levelName, directory):
            if ".gz" in fileName:
                self.addZippedFile(filePath)

    def addZippedFile(self, filePath):
        self.zippedFiles.append({
            "path": filePath,
            "size": main.size(filePath),
            "index": main.index(filePath)
        })
        self.totalZippedSize += main.size(filePath)  # add the size to the total size of zipped logs
        self.zippedFiles.sort(key=lambda x: x["index"])  # sort list by index
