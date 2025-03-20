"""
Created on:     7/2/2021
Created by:     Marcos E. Mercado
Description:    This module contains the FileMgmt class that encapsulates methods to find a file and move a file between directories.
Sources:        https://docs.python.org/3/library/fnmatch.html
                https://docs.python.org/3/library/os.path.html
"""

import fnmatch
import pathlib
import csv
from PC_Utils.Runtime import Runtime

class FileMgmt:
    """This class will encapsulate actions on the filesystem like finding a file within a directory and moving a file."""

    def __init__(self):
        self.workingDir = pathlib.Path.cwd()

    def getInputFileName(self, argv: list, no_file_msg: str = "Please include the path and name of the input file.") -> pathlib.Path:
        """Method that receives the array of sys arguments and determines whether an argument was provided (assuming it's the path to and name of the file) and if not, displays a message.
        If an argument is provided, it is returned assuming it's the path and name of the input file."""
        if len(argv) == 1:
            print(no_file_msg)
            exit()
        else:
            return argv[1]

    def findFiles(self, pattern: str, path: pathlib.Path = None) -> list:
        """Method that receives a file search pattern and the path to a folder.
        Returns the list of names of those files (and folders) in that path that match the pattern.
        If no path is specified, the current working directory will be used."""
        if not path:
            path = self.workingDir

        fileNames = []

        for file in path.iterdir():
            if fnmatch.fnmatch(file.name, pattern) and file.is_file():
                fileNames.append(file.name)
        
        return fileNames

    def moveFile(self, pathToFile: pathlib.Path, destinationfolder: pathlib.Path, newFileName: str = None) -> None:
        """Method that receives a file (including its full path) and a destination folder.
        It moves the file to the destination folder."""

        if not newFileName: #if no newFileName is specified, we use the original file name
            fileNm = self.getFileNameFromPath(pathToFile)
        else:   #if a newFileName is specified, use it.
            fileNm = newFileName

        pathToFile.replace(destinationfolder / fileNm)   # Move the file to the destinationfolder. Use rename instead of replace to avoid overwriting an existing file.

    def getFileNameFromPath(self, pathToFile: pathlib.Path) -> str:
        """Method that receives a file path and returns the file name without the path.
        If the path does not include a file, an error is thrown."""
        try:
            if pathToFile.is_file():    # If the path provided ends in an actual file name
                return pathToFile.name  # return the name of the file (last element of Path object)
            else:
                raise FileNotFoundError("Need to provide a valid path including a file name.")
        except:
            print("Error in method getFileNameFromPath(). Make sure you provided a valid file path including the file name.")

    def addSuffix(self, fileName: str, suffix: str) -> str:
        """Method that receives a file name with or without an extension and a suffix. It returns the file name with the suffx preserving the extension (if any).
        For example: if the file name is "archivo.txt" and the suffix is "20210708", this method returns: "archivo_20210708.txt"."""
        if fileName.count(".") == 0:    # If the fileName contains no dots
            return fileName + "_" + suffix
        #elif fileName.count(".") == 1:  # elif not needed anymore
        #    return fileName.replace(".", "_" + suffix + ".", 1)
        else:
            lastDotIn = fileName.rfind(".") # Finds the index of the last dot in the fileName string
            return fileName[:lastDotIn] + "_" + suffix + "." + fileName[lastDotIn+1:]
 
    def saveCSVfileFromListOfDictionaries(self, pathToFile: pathlib.Path, list_of_dicts: list, sort_headers: bool = False) -> None:
        """Method that receives a list of dictionaries and creates a CSV file with each element of the list as a row.
        NOTE: This method does not un-nest nested dictionaries."""

        # Getting list of headers - based on answer posted here: https://stackoverflow.com/questions/11399384/extract-all-keys-from-a-list-of-dictionaries
        csv_headers = set().union(*(d.keys() for d in list_of_dicts)) # We get the headers from the set of keys of all dictionaries in the list
        
        if sort_headers:
            csv_headers = sorted(csv_headers)   # We sort the headers alphabetically - may want to change method to specify sort?

        with open(pathToFile, 'w', encoding="utf-8", newline = '') as f:
            dict_writer = csv.DictWriter(f, csv_headers)
            dict_writer.writeheader()
            dict_writer.writerows(list_of_dicts)

    def readCSVfileIntoListOfDictionaries(self, pathToFile: pathlib.Path, encoding: str = "utf-8", exit_if_empty: bool = True) -> list:
        """Method that receives a path to a .csv file, enconding (optional), and loads the contents of the file into a list of dictionaries.
        If file has no data, this method will inform the user and by default will exit the program."""
        print(f"Loading input file '{pathToFile}'... ", end='')
        try:
            with open(pathToFile, encoding=encoding) as input_file:
                reader = csv.DictReader(input_file)
                file_contents = list(reader)
        except OSError as err:
            print(f"\n\nError {err=}, {type(err)=} occurred when attempting to read the file.")
            raise

        num_rows = len(file_contents)

        if num_rows > 0:
            print(f"done. File has {num_rows} rows of data.")
            return file_contents
        else:
            print(f"Input file has no data.")
            if exit_if_empty: exit()
            else: return None

    def validateCSVfileHeaders(self, file_headers: list, required_file_headers: list) -> None:
        """Method that ensures all elements in the list of required file headers are in the list of headers"""
        print("Validating input file headers... ", end='')

        for required_header in required_file_headers:   # Loop through the file headers to make sure we have the headers we need.
            if required_header not in file_headers:
                print(f"\n> Required file header '{required_header}' not found in the file. Please check the input file and try again.")
                exit()

        print("done.")

    def createOutputCSVfileFromListOfDictionaries(self, list_of_dictionaries: list, output_file_nm: pathlib.Path, sort_headers: bool = False, start_msg: str = "> Creating output file... ", no_file_created_msg: str = "> No output file was created.") -> None:
        """Method that receives a list of dictionaries that resulted from processing an input file and creates a .csv file with the same name as the input file but with a provided suffix."""
        if len(list_of_dictionaries) > 0:
            print(start_msg, end ='')   # message that indicates that the program is going to create the output file

            self.saveCSVfileFromListOfDictionaries(output_file_nm, list_of_dictionaries, sort_headers)
            print(" done")
        else:
            print(no_file_created_msg)

    def fileIntake(self, argv: list, no_file_msg: str = "", required_file_headers: list = []) -> None:
        """Method that encapsulates the intake of an input file. It leverages methods already defined in this class to do the following:
        1. Check the number of arguments and get input file name (which may include the full path)
        2. Reads the contents of the input file
        3. (Optional) Validates if the required headers are present in the input file
        """
        
        # check number of arguments and get input file name (including path, if provided)
        if no_file_msg:
            self.input_file_nm = self.getInputFileName(argv, no_file_msg)
        else:
            self.input_file_nm = self.getInputFileName(argv)
        
        # read input file
        self.file_contents = self.readCSVfileIntoListOfDictionaries(self.input_file_nm)
        self.file_headers = self.file_contents[0].keys()
        
        # validate file headers if provided - If provided and required headers are not found in the file, program will exit.
        if required_file_headers:
            self.validateCSVfileHeaders(self.file_headers, required_file_headers)
            
    def createOutputFile(self, file_data: list, file_suffix: str = "", sort_headers: bool = False, start_msg: str = "", no_file_created_msg: str = "") -> None:
        """Method that encapsulates the creation of output files with data in the form of a list of dictionaries. It leverages the methods already defined in this class to do the following:
        1. Define output file name with timestamp
        2. Adds suffix to file name
        3. Creates CSV output file
        """
        runtime = Runtime()
        
        fileNameTimeStamp = runtime.strTimeStamp()        
        base_file_nm = self.input_file_nm  # The output file name will be called the same as the input file name (includes the path, so it'll be saved in the same directory), with the addition of a suffix.
        file_nm_suffix   =   file_suffix + '_' + fileNameTimeStamp  # suffix for the output file
        output_file_nm = self.addSuffix(base_file_nm, file_nm_suffix)
        
        if start_msg and no_file_created_msg:   # If both messages are provided
            self.createOutputCSVfileFromListOfDictionaries(file_data, output_file_nm, sort_headers, start_msg, no_file_created_msg)
        elif start_msg:
            self.createOutputCSVfileFromListOfDictionaries(file_data, output_file_nm, sort_headers, start_msg=start_msg)
        elif no_file_created_msg:
            self.createOutputCSVfileFromListOfDictionaries(file_data, output_file_nm, sort_headers, no_file_created_msg=no_file_created_msg)
        else:   # if neither the start nor the no_file_created message are provided
            self.createOutputCSVfileFromListOfDictionaries(file_data, output_file_nm, sort_headers)