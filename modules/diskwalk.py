#!/usr/bin/python
# _*_ coding=utf-8 _*_
import os
#path = "./SecAudit"
class diskwalk(object):
    def __init__(self,path):
        self.path = path
###列出所有的文件路径
    def enumeratepaths(self):
        path_collection = []
        for dirpath,dirname,filenames in os.walk(self.path):
            for file in filenames:
                fullpath=os.path.join(dirpath,file)
                path_collection.append(fullpath)
        return path_collection

###列出所有的文件
    def enumeratefiles(self):
        file_collection = []
        for dirpath,dirnames,filenames in os.walk(self.path):
            for file in filenames:
                file_collection.append(file)
        return file_collection

###列出所有的目录
    def enumeratedir(self):
        dir_collection = []
        for dirpath,dirnames,filenames in os.walk(self.path):
            for dir in dirnames:
                dir_collection.append(dir)
        return dir_collection
'''
if __name__ == "__main__":
    path_collection=diskwalk.enumeratedir(path)
    file_collection=diskwalk.enumeratefiles(path)
    dir_collection=diskwalk.enumeratepaths(path)

    print(path_collection)
    print(file_collection)
   print(dir_collection) 
'''
