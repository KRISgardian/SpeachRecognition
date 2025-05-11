import audio as audioModule
import pyqtgraph as pg
import numpy as np


# init script explanation step by step
# 1. Create first instance of audio module
# which lately will provide all required
# functions & methods.
# 2. 


if __name__ == "__main__":

    # There's just some global vars.
    global pythonCuda
    pythonCuda = True

    # Create audioModule class instance.
    audio = audioModule.audio()

    # Counter for main working loop.
    counter = 0

    while counter != audio.size():

        # This will get data from files name by name.
        audio.getInfoFromAudioFile(audio.existingFileNames[counter])

        # Status check.
        audio.statusCkeck()

        # Audio normalization.
        audio.normalizeDataFromAudio()

        # Create quick app.
        app = pg.mkQApp()

        # Create main window object.
        window = pg.PlotWidget(useOpenGL=True)

        # Using gpu to process data.
        pg.setConfigOption("useCupy", pythonCuda)

        # Set plot data.
        window.plot(np.linspace(0, 10, audio.length()), audio.data, pen='b')

        # Set title to graph by file name.
        window.setTitle(str(audio.existingFileNames[counter]), color='w', size="16pt")

        # Show window.
        window.show()

        # Execute QT app.
        app.exec()

        counter += 1