"""
Created on:     7/2/2021
Created by:     Marcos E. Mercado
Description:    This module contains the FileMgmt class that encapsulates methods to find a file and move a file between directories.
Sources:        https://docs.python.org/3/library/fnmatch.html
                https://docs.python.org/3/library/os.path.html
"""

import fnmatch
import pathlib

from azure.storage.blob import ContainerClient, BlobServiceClient

class FileMgmt:
    """This class will encapsulate actions on the filesystem like finding a file within a directory and moving a file."""

    def __init__(self):
        self.workingDir = pathlib.Path.cwd()

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
            
class AzureStorage(FileMgmt) :
    """Class that inherits functionality from FileMgmt but establishes functionality to work with azure.storage.blob files."""

    def __init__(self):
        FileMgmt.__init__(self)

    def findBlobs(self, pattern: str, container: ContainerClient = None) -> list:
        """Method based on superclass's findFiles() method.
        It receives a blob name search pattern and an Azure Blob Storage Blob Container Client.
        Returns the list of names of those blobs in that container that match the pattern.
        If no container is specified, the current working directory will be used but interpreter will most likely throw an error."""
        if not container:
            container = self.workingDir

        blobNames = []

        for blob in container.list_blobs():
            if fnmatch.fnmatch(blob.name, pattern):
                blobNames.append(blob.name)
        
        return blobNames

    def copyBlob(self, blob_service_client: BlobServiceClient, source_blob_url: str, destination_container: ContainerClient, destination_blob_name: str, destination_subdirectory: str = None) -> None:
        """Method that receives a BlobServiceClient, a source blob (which is the full URL path to the blob), destination container, a new blob name, and (optional) a destination subdirectory path.
        It copies the blob from the URL provided to the destination container with the new name. If a destination subdirectory path is provided, it assumes the container is the root level.
        Copying of the blob methods was based on information found here: https://stackoverflow.com/questions/32500935/python-how-to-move-or-copy-azure-blob-from-one-container-to-another"""

        if destination_subdirectory :   # if user provides a subdirectory...
            destination_container_name = destination_container.container_name + "/" + destination_subdirectory
        else :
            destination_container_name = destination_container.container_name

        copied_blob = blob_service_client.get_blob_client(destination_container_name, destination_blob_name)
        copied_blob.start_copy_from_url(source_blob_url)

    def deleteBlob(self, blob_service_client: BlobServiceClient, container: ContainerClient, blob_name: str) -> None:
        """Method that deletes a blob."""

        del_blob = blob_service_client.get_blob_client(container.container_name, blob_name)
        del_blob.delete_blob()

    def moveBlob(self, blob_service_client: BlobServiceClient, source_container: ContainerClient, destination_container: ContainerClient, source_blob_name: str, destination_blob_name: str, destination_subdirectory: str = None) -> None:
        """Method that creates the source_blob_URL and combines copyBlob and deleteBlob methods."""

        source_blob_url = f"{source_container.url}/{source_blob_name}"

        self.copyBlob(blob_service_client, source_blob_url, destination_container, destination_blob_name, destination_subdirectory)
        self.deleteBlob(blob_service_client, source_container, source_blob_name)