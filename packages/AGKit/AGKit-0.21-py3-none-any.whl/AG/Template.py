import os

from AG.Singleton import Singleton
from AG.DirUtil import DirUtil


class Template(Singleton):
    templateDict = {}

    def __init__(self):
        pass

    def Init(self, root):
        if not DirUtil.Check(root, False):
            return
        for _, dirs, _ in os.walk(root):
            for dir in dirs:
                dir_path = "%s/%s" % (root, dir)
                for _, _, files in os.walk(dir_path):
                    for file in files:
                        file_path = "%s/%s" % (dir_path, file)
                        with open(file_path, 'r', encoding='utf8') as f:
                            content = f.read()
                            if dir not in self.templateDict.keys():
                                self.templateDict[dir] = {}
                            self.templateDict[dir][file] = content

    def Get(self, dir, file):
        return self.templateDict[dir][file]
