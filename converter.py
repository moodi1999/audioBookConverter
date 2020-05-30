import sys
import getopt
import os
import eyed3
import glob
import argparse


class ConvertFiles:
    def __init__(self):
        self.artistName = ''
        self._files = []

    def initOptions(self):
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], "hs:a:", ["singleFile=", "artist="])
        except getopt.GetoptError as err:
            print(err)
            print('converter.py [-s singlefile.mp3] [-a artistName] ')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('converter.py [-s singlefile.mp3] [-a artistName] ')
                sys.exit()
            elif opt in ("-s", "--singleFile"):
                print('converting only ', arg)
                self._files.append(arg)
            elif opt in ("-a", "--artist"):
                print('with artist name ', arg)
                self.artistName = arg

        if (len(self._files) == 0):
            self._files.extend(glob.glob('**/*', recursive=True))

    def convertToMp3(self, fileName):
        if ('.mp3' in fileName):
            return fileName
        return self.renameFile(fileName, fileName)

    def renameFile(self, filePath, newTitle):
        new_filename = "{0}.mp3".format(newTitle)
        os.rename(filePath, new_filename)
        return new_filename

    def startConverting(self):
        for f in self._files:
            fName = os.path.basename(f)
            if ('.py' in fName):
                continue
            mp3File = self.convertToMp3(f)

            audiofile = eyed3.load(mp3File)

            title = audiofile.tag.title

            finalName = f.replace(fName, title)

            try:
                comment = audiofile.tag.comments[0].text
                if (title == comment):
                    print('editing -> {0}'.format(title))
                    continue

                audiofile.tag.title = comment

                if (self.artistName != ''):
                    audiofile.tag.artist = self.artistName
            except:
                print('errre in {0}'.format(fName))
            
            audiofile.tag.save()

            mp3File = self.renameFile(mp3File, finalName)

if __name__ == "__main__":
    print('init...')
    cf = ConvertFiles()
    print('setting options ...')
    cf.initOptions()
    print('starting...')
    cf.startConverting()
    print('Done!')
