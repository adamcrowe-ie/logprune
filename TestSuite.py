
import os, shutil, filecmp

from distutils.dir_util import copy_tree
from TestSuiteConfig import *

class TestUnit:
    def __init__(self, unitToTest):
        self.unitToTest = unitToTest
        self.failedDirectories = []

        self.originalFilesDirectory = ORIGINAL_FILES_PATH.format(unitToTest)
        self.testOutputFilesDirectory = TEST_OUTPUT_PATH.format(unitToTest)
        self.outcomeFilesDirectory = OUTCOME_FILES_PATH.format(unitToTest)

        shutil.rmtree(self.testOutputFilesDirectory)
        copy_tree(self.originalFilesDirectory, self.testOutputFilesDirectory)
        
        self.directoriesToTest = [os.path.join(self.testOutputFilesDirectory, directory) for directory
                                  in os.listdir(self.testOutputFilesDirectory)]

        print "\nRunning Tests on Module " + unitToTest


    def testFailure(self, failedDirectory):
        self.failedDirectories.append(failedDirectory)


    def checkOutcomes(self):
        for directory in os.listdir(self.testOutputFilesDirectory):

            testOutput = os.path.join(self.testOutputFilesDirectory, directory)
            expectedOutcome = os.path.join(self.outcomeFilesDirectory, directory)
            
            dircmp = filecmp.dircmp(testOutput, expectedOutcome)

            if dircmp.left_list != dircmp.right_list and testOutput not in self.failedDirectories:
                self.failedDirectories.append(testOutput)

        if len(self.failedDirectories) > 0:
            raise Exception("\nFailed Tests:{0}".format(self.failedDirectories))
        else:
            print "\nTESTS SUCCESSFUL!"
