import ffmpeg
import os
import numpy as np

from randomFunctions import getRandomHashName


import data as dataModule


# Status instance
# 0. Riff chunk
# 1. Wav chunk 
# 2. Data chunk

class audio:

    def __init__(self,
                 quiet : bool = True):
        self.bitRate = 1411
        self.quiet = quiet
        self.status = [0, 0, 0]
        self.dataDir = "test-data/"
        self.workingDir = "C:/Users/Kris/AppData/Local/Temp/"
        self.getAudioFilesReady()
        self.numberOfFileNames = len(self.existingFileNames)
        


    # Convert all audio file to .wav format. Create new names for files 
    # and put them into listened directory. Create file named .indexes and
    # write all existing file names into.
    def getAudioFilesReady(self):

        try:

            fileNames = []

            # Creating lists for files names.
            outputRecords = []

            # Setting up counter value.
            counter = 0

            # Fill list with exists files in given directory.
            filesList = os.listdir(self.dataDir)

            # Files list length.
            listLength = len(filesList)

            # Exists.
            if listLength == 0:
                return 1

            # While listLength != counter all files will be converted from any to .wav .
            while listLength != counter:
                fileNames.append(self.dataDir + filesList[counter])
                outputRecords.append(getRandomHashName() + ".wav")
                counter += 1

            # Get file handler to /.indexes file with +append mode.
            hFile = open(self.workingDir + ".indexes", '+a')

            counter = 0

            # While i != len(inputRecords) length -> do.
            while listLength != counter:
                stream = ffmpeg.input(fileNames[counter])
                stream = ffmpeg.output(stream, (self.workingDir +  outputRecords[counter]), audio_bitrate=self.bitRate, format="wav")
                ffmpeg.run(stream, quiet=self.quiet) # quiet flag is true by default to prevent surplus console output.
                hFile.write(outputRecords[counter] + "\n")
                counter += 1

            # Closing file handler.
            hFile.close()

            self.existingFileNames = outputRecords

        except:
            return 1


    # TODO: Describe this function manually.
    def getInfoFromAudioFile(self,
                             existingFileName : str):
        
        try:

            # First data index in file.
            firstDataIndex = 0

            # Some local consts.
            riffChunk = 295
            wavChunk = 307
            dataChunk = 410

            print(self.workingDir + existingFileName)

            # Open file -> read everything to the buffer -> close file.
            hFile = open(self.workingDir + existingFileName, "rb")
            data = hFile.read()
            hFile.close()

            # Counter for file parsing.
            counter = 0

            # Parsing loop.
            while counter < 300:
                # Riff chunk block.
                if self.status[0] == 0:
                    if sum(data[counter:counter + 4]) == riffChunk:
                        print("Riff chunk founded at addr:" + str(counter))
                        self.status[0] = 1 + counter


                # Main info chunk block. As is - wav, af, nc, sr, br, ba
                if self.status[1] == 0:
                    if sum(data[counter:counter + 4]) == wavChunk:
                        # Wav chunk block.
                        print("Wav chunk founded at addr:" + str(counter))
                        self.status[1] = 1 + counter

                        counter += 12

                        # Audio format chunk block.
                        print("Audio format chunk founded at addr:" + str(counter))
                        print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                        self.audioFormat = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))
                        
                        counter += 2

                        # Number of channels block.
                        print("Number of channels founded at addr:" + str(counter))
                        print((dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))))
                        self.numberOfChannels = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))

                        counter += 2

                        # Sample rate block.
                        print("Sample rate founded at addr:" + str(counter))
                        print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4])))
                        self.sampleRate = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4]))

                        counter += 4

                        # Byte rate block.
                        print("Byte rate founded at addr:" + str(counter))
                        print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4])))
                        self.byteRate = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4]))

                        counter += 2

                        # Block align block.
                        print("Block align founded at addr:" + str(counter))
                        print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                        self.blockAlign = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))

                        counter += 2

                        # Bits per sample.
                        print("Bits per sample founded at addr:" + str(counter))
                        print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                        self.bitsPerSample = dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))


                # Data chunk block. 
                if self.status[2] == 0:
                    if sum(data[counter:counter + 4]) == dataChunk:
                        # Data & its size.
                        print("Data chunk founded at addr:" + str(counter))
                        print("Size chunk was found at addr:" + str(counter+4) + "\nFile size is now:" + str(dataModule.getNormalizedDataFromWAV(list(data[counter+4:counter+8]))))
                        firstDataIndex = counter + 8
                        self.audioDataLength = dataModule.getNormalizedDataFromWAV(list(data[counter+4:counter+8]))


                        # FristData block.
                        print("First data was founded at addr:", firstDataIndex)
                        print("First data:", hex(data[counter+8]))
                        self.status[2] = 1 + counter

                counter += 1

            self.firstDataIndex = firstDataIndex
            self.data = data
            self.dataLength = len(data)

        except:
            return 1


    # Convert data to amplitude values by
    # bitsPerSample rate.
    def normalizeDataFromAudio(self):

        try:

            length = len(self.data)

            counter = 0
            
            output = []

            match self.bitsPerSample:
                case 4:
                    while counter != length:
                        temp = list(bin(self.data[counter])[2:])

                        if len(temp) < 8:
                            tempCounter = len(temp)
                            while tempCounter != 8:
                                temp.reverse()
                                temp.append(0)
                                temp.reverse()
                                tempCounter += 1
                        if len(temp) % 8 != 0:
                            temp.reverse()
                            temp.append(0)
                            temp.reverse()

                        output.append(int(str(temp[:4]).replace(']', '').replace('[', '').replace('\'', '').replace(',', '').replace(' ', ''), 2))

                        output.append(int(str(temp[4:9]).replace(']', '').replace('[', '').replace('\'', '').replace(',', '').replace(' ', ''), 2) \
                                - int(str(temp[4:9]).replace(']', '').replace('[', '').replace('\'', '').replace(',', '').replace(' ', ''), 2) * 2)

                        counter += 1
                case 8:
                    while counter != length:
                        output.append(int(self.data[counter]))
                        counter += 1
            
            self.data = output
            self.dataLength = len(output)

        except:
            return 1


    def getAudioAsMonoFromData(self,
                               channel : int = 0):
        # data : list
        # channel : int = 0
        # 0 - stand for left channel
        # 1 - stand for right channel
        
        try:
            
            length = len(self.data)

            output = []

            if channel == 0:

                counter = 0

                while counter != length:
                    output.append(self.data[counter])
                    counter += 2
            elif channel == 1:

                counter = 1

                while counter != length:
                    output.append(self.data[counter])
                    counter += 2
            else:
                raise ValueError
            
            self.mono = output
        except:
            return 1
    

    def getAudioAsStereoFromData(self):

        try:
            
            length = len(self.data)

            left = []
            right = []

            counter = 0

            while counter != length:
                left.append(self.data[counter])
                right.append(self.data[counter+1])
                counter += 2
            
            self.left = left
            self.right = right
        except:
            return 1
    

    def left(self):
        return self.left
    
    
    def right(self):
        return self.right
    
    
    def mono(self):
        return self.mono
    

    def clearStatus(self):
        try:
            self.status[0] = 0
            self.status[1] = 0
            self.status[2] = 0
        except:
            return 1


    def statusCkeck(self):
        try:
            if self.status[0] == 0:
                print("Riff chunk was not founded")
            if self.status[1] == 0:
                print("Wav chunk was not founded")
            if self.status[2] == 0:
                print("Data chunk was not founded")
            elif self.status[0] != 0 and self.status[1] != 0 and self.status[2] != 0:
                print("Correction phase:Done\n")
        except:
            return 1


    def size(self):
        return self.numberOfFileNames
    

    def length(self):
        return self.dataLength