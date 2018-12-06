# PT Grey Image Acquisition
PT Grey Image Acquisition is a command line-based python script developed for the Conformable Decoders group at the MIT Media Lab that acquires and saves images from a photogrammetry setup of multiple Point Grey Blackfly GigE cameras. The script utilizes FLIR’s [Spinnaker](https://www.ptgrey.com/spinnaker-sdk) SDK and PySpin Python library to interface with the cameras. The user can choose from three different modes of image acquisition: manual, timed and continuous. After image acquisition is completed, all images are rotated 270 degrees for easier viewing and saved under the PNG file format. All images are taken in grayscale, and image naming follows the requirements specified for use with [MultiDIC](https://github.com/MultiDIC/MultiDIC). 
## Installation
This script was developed and tested on 64-bit Windows 10, and has not been tested on other platforms. PT Grey Image Acquisition was written in Python 3.6, and uses the PySpin, datetime, time, os, and PIL Python libraries. It has not been tested on any earlier or later versions of python. The download and documentation for the PySpin library can be found on [FLIR’s website](https://www.ptgrey.com/support/downloads) under “Spinnaker for Python”.  The script can be run from the command line or from a Python IDE; the script was developed and tested using [Anaconda’s Spyder](https://www.anaconda.com/download/).  It is also recommended to use FLIR’s [FlyCapture2 Viewer](https://www.ptgrey.com/support/downloads) to show live streams of individual cameras while manually focusing them. 
## Setup
The cameras used in this setup must be focused by hand. It is recommended to use FLIR’s FlyCapture2 Viewer to view the camera livestream while adjusting. The user can select a camera by serial number to view the livestream, as shown in figure 2. Cameras are focused by turning the focus ring to infinity and then adjusting the iris ring until the desired brightness and focus is achieved. A diagram of the lens used in the setup can be found on the [Computar](https://computar.com/resources/files_v2/1636/A4Z2812CS-MPIR_12-14.pdf) website. Minor adjustments to the iris will need to be made when switching between subjects of different skin tones. The FlyCapture2 Viewer should be closed completely before running the script.
# Usage
## User Input
The user will be taken through several prompts to apply settings for the camera run. If the user provides an invalid input, the script terminates and must be re-run. Only manual mode requires user interaction during image acquisition. There are several print statements throughout the program to signify when major actions have been performed, such as acquiring a round of images or saving the images.
## Image Acquisition
User interaction differs between the different acquisition modes. The use cases and typical interactions with each mode are listed below.  
### Manual Mode
Manual mode should be used for runs in which the user wishes to trigger the cameras manually. After the cameras are initialized, the user can specify when to take an image by pressing the ‘enter’ button. Once the images for that round are acquired, the user can press ‘enter’ once again to take the next round of images. The user signifies that the camera run is complete by entering ‘e’ in the prompt, at which point the images are saved and the script terminates. 
### Timed Mode
Timed mode should be used for runs in which the user wishes to automatically take pictures but with a delay of at least one second in between each image round. The user specifies the desired number of images as well as the time delay between each image. Once the cameras are initialized, there is a 5 second delay before the script begins taking images. After acquiring a round of images, the script will “sleep” for the specified time delay. Once the desired number of images are taken, all images are saved and the script terminates. The current image round number will be printed to the screen as the program progresses. 
### Continuous Mode
Continuous mode should be used for runs in which the user wishes to automatically take pictures with no time delay between each image round. The user specifies the desired number of images. Once the cameras are initialized, there is a 5 second delay before image acquisition begins. The current image round will be printed to the screen as the script progresses. Once the desired number of images are taken, all images are saved and the script terminates. 
## Saved Images
The images will be saved in the path specified during the script and camera setup. The default location path is "…\ Documents\Camera Runs", which was used for the specified equipment setup. If a new path location is entered for this setting, the validity of the specified path is checked during the input phase of the script. The entire run will exist in a folder with the naming format “Camera Run Year-Month-Day Hour Minute Second”. Within this folder there will be several folders in the format “Camera Number”. Within each camera folder are the images acquired from this image for the run, with the naming format “camNumberImage_x.png”. All images are saved in grayscale and rotated 270 degrees. Image naming is compatible with MultiDIC. 
# Documentation and Full User Manual
Further explanation on the script can be found [here](https://github.com/rachelmci/PT-Grey-Image-Acquisition/blob/master/Software%20Documentation%20and%20User%20Guide.pdf).
# Contributing
If you wish to contribute, please send an email to rmcintos@mit.edu
# License
[MIT](https://choosealicense.com/licenses/mit/)
