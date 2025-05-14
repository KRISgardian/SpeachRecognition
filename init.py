import audio as audioModule
import pyqtgraph as pg
import numpy as np

# TODO: Done with this step by step shit
# init script explanation step by step
# 1. Create first instance of audio module
# which lately will provide all required
# functions & methods.
# 2. Start loop. Loop will work 'till it 
# through all file names and get data from.
# 3. Using data wich audio class will 
# provide, get amplitude values from them.
# 4. Create required instances of UI interface
# 5. Modify data. Try to compress it for show
# purposes.


if __name__ == "__main__":

    # There's just some global vars.
    global pythonCuda
    pythonCuda = True

    # Create audioModule class instance.
    audio = audioModule.audio()

    # Counter for main working loop.
    counter = 0

    while counter != audio.size():

        # This will get data from files name by name and contain it inside audio class.
        # It will automatically delete previous instance of data.
        audio.getInfoFromAudioFile(audio.existingFileNames[counter])

        # Status check. Just a little pritn function to see if things get right or not.
        audio.statusCkeck()

        # Audio normalization function will return data itself without any meta from file
        # and also will cut all data using bits per sample value from file meta.
        audio.normalizeDataFromAudio()

        # Create quick app.
        app = pg.mkQApp()

        # Create main window object.
        window = pg.PlotWidget(useOpenGL=True)

        # Using gpu to process data. I my own doubt it tbh.
        pg.setConfigOption("useCupy", pythonCuda)

        # Set plot data. As is create first graph using amplitude from data.
        window.plot(np.linspace(0, 10, audio.length()), audio.data, pen='b')

        # Set title to graph by file name.
        window.setTitle(str(audio.existingFileNames[counter]), color='w', size="16pt")

        # Show window.
        window.show()

        # Execute QT app.
        app.exec()

        counter += 1