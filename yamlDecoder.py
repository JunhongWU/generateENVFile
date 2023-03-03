import base64
import yaml
import shutil
import os

"""
Download the "secret-esvsecrets.yaml" from https://console-openshift-console.apps.aro-delta.euw-hub02.azure.volvo.net/k8s/ns/esv-qa/secrets
Save it under your default downloads path, this script will searche for the downloaded file with the name 'secret-esvsecrets.yaml'
By default, the .env file will be generated in the current working directory where the script is executed
Run this script and go check your .ENV 
"""

# Define the current file path and the destination folder path
#generated_ENV_file_location_ = 'C:/ESV_Jun/gwdp-backend/.env'
generated_ENV_file_location_ = '.env'
home_dir = os.path.expanduser("~")
download_path = os.path.join(home_dir, "Downloads")
yamlFile_Name = 'secret-esvsecrets.yaml'
yamlFileOnTxtFormat_Name = 'secret-esvsecrets.txt'

def main():
    # Indicate the original download yaml file from secret
    dataYaml = readYamlFile(download_path + yamlFile_Name)
    #Transform the downloaded yaml file to txt format
    writeYamlFileToTxtFile(dataYaml, download_path + yamlFileOnTxtFormat_Name)
    #Retrive the lanes that will be used
    filteredLines = filterLinesBetweenTwoLines(readTextFile(download_path + yamlFileOnTxtFormat_Name))
    #Restructure and descrypt the data
    generateFileDot_ENV(filteredLines, generated_ENV_file_location_)   
    os.remove(download_path + yamlFileOnTxtFormat_Name)


def generateFileDot_ENV(data, outputFileName):
    #This function restructure the filtered data and decrypt it, output a file with predefined name
    #@data: filtered data before decrypting
    #@outputFileName: target file as output
    decodedLines = ''
    for line in data.split('\n'):
        words = line.split()
        if line != '':
            variableName = words[0].replace(':','')
            encryptedInfo = words[1]
            decryptedInfo = decodeBase64String(encryptedInfo)
            decodedLines += variableName + ' = ' + decryptedInfo + '\n'
    writeTextFile(decodedLines, outputFileName)   
    return     

def filterLinesBetweenTwoLines(document):
    start = "data:"
    end = "metadata:"
    filter_on = False
    filteredLines = ''

    for line in document.split('\n'):
        if line.split()[0] == start:
            filter_on = True
            continue
        elif line.split()[0] == end:
            filter_on = False
            break
        if filter_on:
            filteredLines += line +'\n'
    
    return filteredLines

def readTextFile(documentName):
    with open(documentName) as f:
        document_content = f.read()
        f.close()
    return document_content

def writeTextFile(data, file):
    f = open(file, 'w')
    f.write(data)
    f.close()

def readYamlFile(documentName):
    with open(documentName, 'r') as file:
        document_content = yaml.safe_load(file)
        #reformatedData = pprint.pprint(data)
    return document_content

def writeYamlFileToTxtFile(data, documentName):
    with open(documentName, 'w') as file:
        yaml.dump(data, file)
    return 

def decodeBase64String(base64_string):
    # Define a Base64-encoded string
    # Decode the Base64-encoded string
    decoded_string = base64.b64decode(base64_string).decode("utf-8")
    # Print the decoded string
    return decoded_string

if __name__ == "__main__":
    main()
