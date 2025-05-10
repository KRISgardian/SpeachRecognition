import ffmpeg
import os
import numpy as np

from randomFunctions import getRandomHashName


import data as dataModule


# Convert all audio file to .wav format. Create new names for files 
# and put them into listened directory. Create file named .indexes and
# write all existing file names into. Delete old files if needed.
def getAudioFilesReady(bitrate : int,
                       savePath : str,
                       basePath : str,
                       clearAfter : bool = True,
                       quiet : bool = True):

    try:

        fileNames = []

        # Creating lists for files names.
        outputRecords = []

        # Setting up counter value.
        counter = 0

        # Fill list with exists files in given directory.
        filesList = os.listdir(basePath)

        # Files list length.
        listLength = len(filesList)

        # Exists.
        if listLength == 0:
            return 1

        # While listLength != counter all files will be converted from any to .wav .
        while listLength != counter:
            fileNames.append(basePath + filesList[counter])
            outputRecords.append(getRandomHashName() + ".wav")
            counter += 1


        # Convert everything to wav(PCmodulation coding type).


        # Counter value.
        i = 0

        # Get file handler to /.indexes file with +append mode.
        hFile = open(savePath + ".indexes", '+a')

        # While i != len(inputRecords) length -> do.
        while listLength != i:
            stream = ffmpeg.input(fileNames[i])
            stream = ffmpeg.output(stream, (savePath +  outputRecords[i]), audio_bitrate=bitrate, format="wav")
            ffmpeg.run(stream, quiet=quiet) # quiet flag is true by default to prevent surplus console output.
            hFile.write(outputRecords[i] + "\n")
            i += 1

        # Closing file handler.
        hFile.close()

        # If clearAfter == True then delete all previous files.
        if clearAfter:
            i = 0
            while i != listLength:
                try:
                    os.remove(fileNames[i])
                except:
                    if Exception == FileNotFoundError: # Plug. Without this Windows causes errors.
                        pass
                i += 1

    except:
        return 1

    return outputRecords



# TODO: Describe this function manually.
def getInfoFromAudioFile(path : str,
                          status : list):
    try:

        # First data index in file.
        firstDataIndex = 0

        # Some local consts.
        riffChunk = 295
        wavChunk = 307
        dataChunk = 410

        # Open file -> read everything to the buffer -> close file.
        hFile = open(path, "rb")
        data = hFile.read()
        hFile.close()

        # Counter for file parsing.
        counter = 0

        # Containter variables.
        container = []

        # Parsing loop.
        while counter < 300:
            # Riff chunk block.
            if status[0] == 0:
                if sum(data[counter:counter + 4]) == riffChunk:
                    print("Riff chunk founded at addr:" + str(counter))
                    status[0] = 1 + counter


            # Main info chunk block. As is - wav, af, nc, sr, br, ba
            if status[1] == 0:
                if sum(data[counter:counter + 4]) == wavChunk:
                    # Wav chunk block.
                    print("Wav chunk founded at addr:" + str(counter))
                    status[1] = 1 + counter

                    counter += 12

                    # Audio format chunk block.
                    print("Audio format chunk founded at addr:" + str(counter))
                    print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                    status[3] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))
                    
                    counter += 2

                    # Number of channels block.
                    print("Number of channels founded at addr:" + str(counter))
                    print((dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))))
                    status[4] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))

                    counter += 2

                    # Sample rate block.
                    print("Sample rate founded at addr:" + str(counter))
                    print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4])))
                    status[5] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4]))

                    counter += 4

                    # Byte rate block.
                    print("Byte rate founded at addr:" + str(counter))
                    print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4])))
                    status[6] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+4]))

                    counter += 2

                    # Block align block.
                    print("Block align founded at addr:" + str(counter))
                    print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                    status[7] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))

                    counter += 2

                    # Bits per sample.
                    print("Bits per sample founded at addr:" + str(counter))
                    print(dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2])))
                    status[8] = 1 + dataModule.getNormalizedDataFromWAV(list(data[counter:counter+2]))
                    

            # Data chunk block. 
            if status[2] == 0:
                if sum(data[counter:counter + 4]) == dataChunk:
                    # Data & its size.
                    print("Data chunk founded at addr:" + str(counter))
                    print("Size chunk was found at addr:" + str(counter+4) + "\nFile size is now:" + str(dataModule.getNormalizedDataFromWAV(list(data[counter+4:counter+8]))))
                    firstDataIndex = counter + 8

                    # FristData block.
                    print("First data was founded at addr:", firstDataIndex)
                    print("First data:", hex(data[counter+8]))
                    status[2] = 1 + counter

            counter += 1

    except:
        return 1

    return firstDataIndex, data




# Get amplitude from data whether file has 2(stereo)
# or 1(mono) channels to AVT(amplitude versus time)
# form. This function will rewrite whole data to
# mono amplitude form.
#def getMonoAVTFromAudioData(data : list):
#    pass



#FFT (Fast Fourier Transform) is a basic algorithm in 
# signals and frequencies. This function ->
#1 - Remove all junk from the data except the data itself.
#2 - Get the FFT from the data and store it in the FVT 
# (frequency versus time) variable.
#def useFFTOnAudioData(data : list):
#    fvt = np.fft.fft(data, norm="ortho")
#   return fvt


# Both functions works only with 4 bits depth audio files.
def convertAudioFileToMono(data):
    length = len(data)

    counter = 0
    
    output = []

    while counter != length:
        temp = list(bin(data[counter])[2:])

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

        counter += 1

    return output


def convertAudioFileToStereo(data):
    length = len(data)

    counter = 0
    
    output = []

    while counter != length:
        temp = list(bin(data[counter])[2:])

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

    return output