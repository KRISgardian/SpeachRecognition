import audio as audioModule
import pyqtgraph as pg
import numpy as np

def clearStatus(status : list):
    status[0] = 0
    status[1] = 0
    status[2] = 0
    status[3] = 0
    status[4] = 0
    status[5] = 0
    status[6] = 0
    status[7] = 0
    status[8] = 0

if __name__ == "__main__":
    # Status variable for information from the loop.
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 0. Riff chunk
    # 1. Wav chunk 
    # 2. Data chunk
    # 3. Audio format
    # 4. Number of channels
    # 5. Sample rate
    # 6. Byte rate
    # 7. Block align
    # 8. Bits per sample

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
        firstDataIndex, data = audioModule.getInfoFromAudioFile("test-data/wav/44100/" + str(existingRecords[counter]), status)


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

        sample = 150 # status[6] - 1

        data = data[firstDataIndex:sample]
    
        data = audioModule.convertAudioFileToStereo(data)

        app = pg.mkQApp()

        window = pg.PlotWidget()

        pg.setConfigOption("useCupy", "True")

        window.useOpenGL(True)

        window.plot(np.linspace(0, 100000, len(data)), data, pen='b')

        window.setTitle(str(existingRecords[counter]), color='w', size="16pt")

        window.show()

        app.exec()

        clearStatus(status)

        counter += 1