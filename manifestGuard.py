import struct
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='manifestGuard:对Androidmanifest文件进行简单加固和相关修复')
    parser.add_argument('-g','--guard', action='store_true',default=False, help='guard mode')
    parser.add_argument('-f','--fixed', action='store_true',default=False, help='fix mode')
    parser.add_argument('-s','--source', type=str,required=True, help='source file')
    parser.add_argument('-o','--out', type=str,required=True, help='target file')

    args = parser.parse_args()
    sourceFile = args.source
    outFile = args.out
    if args.guard == True:
        manifestGuard(sourceFile,outFile)
    elif args.fixed == True:
        fixManifest(sourceFile,outFile)
    else:
        print("One of the two parameters(-g and -f) must be set!")
    


def insert(oldBytes,offset,newBytes):
    rtnBytes = oldBytes[0:offset] + newBytes + oldBytes[offset:]
    return rtnBytes

def delete(oldBytes,offset,size):
    rtnBytes = oldBytes[0:offset] + oldBytes[offset + size:]
    return rtnBytes

def change(oldBytes,offset,newContent):
    newContentSize = len(newContent)
    rtnBytes = oldBytes[0:offset] + newContent + oldBytes[offset + newContentSize:]
    return rtnBytes

def getFileSize(fileContents):
    size = struct.unpack_from('<I',fileContents,4)
    return size[0]

def getStringChunkSize(fileContents):
    size = struct.unpack_from('<I',fileContents,12)
    return size[0]

def getStringPoolOffset(fileContents):
    offset = struct.unpack_from('<I',fileContents,28)
    return offset[0]


def writeFileSize(fileContents,newSize):
    newfileContents = change(fileContents,4,newSize)
    return newfileContents

def writeStringChunkSize(fileContents,newSize):
    newfileContents = change(fileContents,12,newSize)
    return newfileContents

def writeStringPoolOffset(fileContents,newOffset):
    newfileContents = change(fileContents,28,newOffset)
    return newfileContents


def manifestGuard(manifestFilePath,newfilePath):
    with open(manifestFilePath,'rb') as f:
        contents = f.read()
        fileSize = getFileSize(contents)
        stringChunkSize = getStringChunkSize(contents)
        newFileSize = struct.pack("<I",fileSize + 4)
        newStringChunkSize = struct.pack("<I",stringChunkSize + 4)
        contents = writeFileSize(contents,newFileSize)
        contents = writeStringChunkSize(contents,newStringChunkSize)
        fileSize = getFileSize(contents)
        stringChunkSize = getStringChunkSize(contents)
        stringPoolOffset = getStringPoolOffset(contents)
        newStringPoolOffset = struct.pack("<I",stringPoolOffset + 4)
        contents = writeStringPoolOffset(contents,newStringPoolOffset)
        dirtyData = struct.pack("<I",0)
        contents = insert(contents,stringPoolOffset + 8, dirtyData)
    
    with open(newfilePath,'wb') as f:
        f.write(contents)

def fixManifest(oriManifest,outManifest):
    with open(oriManifest,'rb') as f:
        contents = f.read()
        fileSize = getFileSize(contents)
        stringChunkSize = getStringChunkSize(contents)
        newFileSize = struct.pack("<I",fileSize - 4)
        newStringChunkSize = struct.pack("<I",stringChunkSize - 4)
        contents = writeFileSize(contents,newFileSize)
        contents = writeStringChunkSize(contents,newStringChunkSize)
        fileSize = getFileSize(contents)
        stringChunkSize = getStringChunkSize(contents)
        stringPoolOffset = getStringPoolOffset(contents)
        newStringPoolOffset = struct.pack("<I",stringPoolOffset - 4)
        contents = writeStringPoolOffset(contents,newStringPoolOffset)
        contents= delete(contents,stringPoolOffset + 4 ,4)

    with open(outManifest,'wb') as f:
        f.write(contents)


if __name__ == '__main__':
    parse_args()