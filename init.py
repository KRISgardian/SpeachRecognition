import audio as audioModule
import visualize as visualModule


if __name__ == "__main__":
    # Status variable for information from the loop.
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Data list contains required information from file.
    data = []

    # FileNames list contains all existing file names.
    fileNames = []

    # Converting all files to raw .wav format(PCM modulation codec).
    existingRecords = audioModule.getAudioFilesReady(1411, "test-data/wav/44100/", "test-data/miscellaneous/", False)

    # Length of all existing file names.
    length = len(existingRecords)

    # Counter for main working loop.
    counter = 0

    # Main working loop.

    # While counter != length of all existing file names -> do .
    while counter != length:

        #First data index.
        firstDataIndex = 0
        
        # Getting info from wav file.
        firstDataIndex = audioModule.getInfoFromAudioFile("test-data/wav/44100/" + str(existingRecords[counter]), data, status)

        # Getting more details and determine if everything is good.
        if status[0] == 0:
            print("Riff chunk was not founded")
        if status[1] == 0:
            print("Wav chunk was not founded")
        if status[2] == 0:
           print("Data chunk was not founded")
        elif status[0] != 0 and status[1] != 0 and status[2] != 0:
            print("Correction phase:Done\n")


        # Audio proccessing phase.



        # Second counter instance.
        secondCounter = 0

        # Status length
        statusLength = len(status)

        while statusLength != secondCounter:
            status[secondCounter] = 0
            secondCounter += 1

        counter += 1
    

else:
    pass