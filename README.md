# ECGAssess Executable
![Screenshot](ECGAssessGUI.PNG)

### Prerequisites - Program
The executable program should work on all operating systems and does not require any installation or additional software.

### Prerequisites - Data

The data entered in program must have the same formatting as the data in the folder "set-a". Specifically this means:

* The document must be in .txt format.
* There is no heading or any other written words in the document.
* Each measurement is written on a new line. The recordings have a length of 10 seconds and have a frequency of 500 measurements per second.
* In the first column is the numeration of the measurements.
* The other columns are the measured values of the ECG machine in microvolts.
* The individual columns are separated from each other by a comma.

***Example (with 12 leads):***
>**0**,0,4,4,-2,4,-2,0,-4,-16,-16,-16,-12\
>**1**,2,4,2,-3,3,0,-2,-6,-16,-18,-16,-14\
>**2**,0,4,4,-2,4,-2,-2,-6,-15,-18,-16,-14\
>**3**,-2,6,8,-2,7,-5,-2,-6,-15,-18,-15,-11\
>**4**,-3,6,9,-1,8,-6,0,-4,-14,-16,-15,-11\
>...\
>**4997**,-4,-12,-8,8,-10,2,16,12,-6,-15,-12,-12\
>**4998**,-3,-12,-9,7,-10,3,16,12,-4,-14,-12,-12\
>**4999**,0,-12,-12,6,-12,6,16,12,-4,-12,-12,-12

### GUI

After starting the program, a window is opened, which is built up as shown in the image above. To use the program, simply follow the numbers:

1. The first thing to be done is to set how many leads the ECG to be evaluated has. The number can be set simply by clicking the arrow buttons. The default value is 12 and it can be selected from the range of 1 to 12 leads.
2. Next, the "Load Data" button must be pressed. A new window opens where a file must be selected. This file must contain the correct leads as set in step 1 and must meet the data requirements described above.
3. The last thing to do is to press the "Process" button. After that, the results of the analysis will be visible in the table at the bottom right.

After a file is loaded into the program, the plot is visible in the center of the window. The visible lead can be adjusted with the slider at the top of the window.
