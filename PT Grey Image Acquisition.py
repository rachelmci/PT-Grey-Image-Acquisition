# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 22:05:00 2018

@author: Rachel McIntosh
@version: 1.0
MIT Media Lab - Conformable Decoders

Command line-based script used to acquire images from a photogrammetry setup of multiple PT Grey GigE Blackfly cameras
using Flir's Spinnaker package. Acquisition can be performed through a 'manual' mode (the user clicks to take an image),
a 'timed' mode (the user indicates how many pictures to take and the time between shots), or a 'continuous'
mode (the user enters the number of images to take and the program gathers the images as quickly as possible).
Images are rotated 90 degrees to account for the camera positioning in the physical setup and saved in folders
corresponding to the run's timestamp and the camera number. File naming is compatible for MultiDIC runs. 

Future versions will increase the number of images taken per second in continuous acquisition mode and
implement a GUI.

"""

# import statements
import PySpin
import datetime
import time
import os
from PIL import Image

# dictionary mapping serial numbers to camera numbers for easy file saving
# this is specific to the conformable decoders lab setup
serial_to_number = {'18407214': 1, '18407121': 2, '18408213': 3, '18407110': 4, '18407120': 5, '18407122': 6}   

# camera acquisition modes
MANUAL_MODE = 1
TIMED_MODE = 2
CONTINUOUS_MODE = 3    

# image format modes - MultiDIC uses grayscale so we can use mono
MONO8 = 0
MONO12 = 11
MONO16 = 1 
        

def initialize(camera_mode, save_path, save_nickname=True):
    """
    Creates an instance of the PySpin System and initializes all detected cameras based on user input. It also
    creates all the folders necessary for a camera run - the general date/time folder containing the entire run
    and the folder for each camera detected.
    
    Arguments: 
        camera_mode: the image format mode to set the camera to - constants defined in global space
        save_path: string representing the path to save the images to
        save_nickname: boolean value to denote whether to use the nicknames in serial_to_number; if this is false, 
        all naming will be based on the camera's serial number instead (default value true)
        
    Returns:
        A tuple containing the pointer to the camera system instance, a list of camera pointers, and the full saving path
        of the current run
    """

    # get the system and cameras using library
    system = PySpin.System.GetInstance()
    cameras = system.GetCameras()
    num_cams = cameras.GetSize()
    print("Cameras detected:" + str(num_cams))
    
    serial_numbers = []
    # initialize the cameras and get their serial numbers
    for i, cam in enumerate(cameras):
        cam.Init()
        serial_numbers.append(cam.TLDevice.DeviceSerialNumber.GetValue())
    print("Initialized cameras.")
    del cam
          
    # set acquisition and format mode    
    # currently, all runs are set to singleframe due to issues with the continuous mode revolving around 1) a bottle neck
    # sending image data over the ethernet connector and 2) problems with querying multiple cameras for images when in continous mode 
    for i, cam in enumerate(cameras):
        cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)
        cam.PixelFormat.SetValue(camera_mode)
    del cam
       
    # create the folders required for saving
    # create a new folder for the date/time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %Hhr %Mmin %Ss')
    time_path = save_path + "\\Camera Run " + timestamp
    os.mkdir(time_path)
    file_path = time_path
    # create the camera folders
    # save nicknames is enabled - use the camera numbers
    if save_nickname:
        camera_numbers = range(1, num_cams+1)
    # use the camera serial numbers for naming instead
    else:
        camera_numbers = serial_numbers
    for number in camera_numbers:
        cam_path = time_path + "\\Camera " + str(number)
        os.mkdir(cam_path)

    return (system, cameras, file_path)
  
    
def acquire_images(cameras, file_path, counter, camera_mode, nickname, num_images=1):
    """
    Begins acquisition for the cameras passed in, queries each camera for the passed in number of images,
    and ends acquisition for all of the cameras. Returns a dictionary with the keys being the names for the
    imagse and the values being the appropriate image pointers. 
    
    Arguments:
        cameras: list containing pointers to all cameras in the system
        file_path: the path of the directory to save images to for this run
        counter: an int representing the current image count for this call of the function
        camera_mode: the image format mode for this run
        nickname: boolean value to denote whether to use the nicknames in serial_to_number; if this is false, 
        all naming will be based on the camera's serial number instead
        num_images: the number of images to take for this run of the function (default 1) 
    
    Returns:
        A dictionary of all of the images taken.
    """

    # Begin Camera Acquisition for this round
    for i, cam in enumerate(cameras):
        cam.BeginAcquisition()
    del cam
    print("Began Acquisition")
          
    # acquire the specified number of images from the cameras, saving them into a dictionary
    images = {}
    for count in range(num_images):
        for i, cam in enumerate(cameras):
            cam_serial = cam.TLDevice.DeviceSerialNumber.GetValue()
            image_result = cam.GetNextImage()
            # a conversion or deep copy must be performed so that we can release the image_result pointer
            converted = image_result.Convert(camera_mode, PySpin.HQ_LINEAR)
            # determine the format to name the image
            if nickname:
                cam_number = serial_to_number[cam_serial]
                name = "cam" + str(cam_number) + "image_" + str(count + counter)
            else:
                name = "cam" + str(cam_serial) + "image_" + str(count + counter)
            images[name] = converted
            # prevent buffer overflow
            image_result.Release()
    print("Images acquired")
    del cam

    #end camera acquisition for this round
    for i, cam in enumerate(cameras):
        cam.EndAcquisition()
    del cam
    print("Acquisition ended")
    
    return images
    


def save_images(images, file_path, nickname):
    """
    Saves all of the images passed in to the specified file path and rotates them 270 degrees.
    
    Arguments: 
        images: a dictionary with the values being image pointers and the keys being a string representing
        the appropriate name for the image
        file_path: a string representing the path to save the images to
        nickname: boolean value to denote whether to use the nicknames in serial_to_number; if this is false, 
        all naming will be based on the camera's serial number instead
    """
    for image_name in images.keys():
        # determine where to save the images
        if nickname:
            # pull the camera number from the image name - assumes less than 10 cameras in a setup
            cam_number = image_name[3]
            path = file_path + "\\Camera " + str(cam_number) + "\\" + image_name +  ".png"
        else:
            # pull the serial number from the image name
            cam_serial = image_name[3:image_name.index("i")]
            path = file_path + "\\Camera " + str(cam_serial) + "\\" + image_name +  ".png"
        images[image_name].Save(path)
        # rotate the image for better viewing
        im = Image.open(path)
        im = im.transpose(Image.ROTATE_270)
        im.save(path)
        
    print("Images saved")
    
      
def main():
    
    # determine the camera mode
    camera_mode = input("Image Acquisition Mode? Type 1 for manual, 2 for timed, or 3 for continuous ")
    camera_mode = int(camera_mode)
    if camera_mode not in (MANUAL_MODE, TIMED_MODE, CONTINUOUS_MODE):
        print("Invalid input! Aborting...")
        return
    if camera_mode == TIMED_MODE or camera_mode == CONTINUOUS_MODE:
        # determine the number of images
        num_images = input("Enter the number of images: ")
        num_images = int(num_images)
    if camera_mode == TIMED_MODE:
        # determine the time delay
        time_delay = input("Enter the time delay in seconds: ")
        time_delay = float(time_delay)
        print("Time delay: " + str(time_delay))
    if camera_mode == MANUAL_MODE:
        # for manual mode images will be taken one at a time
        num_images = 1
        
    # determine the image mode
    # it is recommended to use mono8 mode for continuous acquisition and mono8 or mono12 for other modes
    # mono16 often results in damaged images due to the large amount of data in the picture
    image_mode = input("Image color mode? Type 1 for mono8, 2 for mono12 and 3 for mono16 ")
    if image_mode == '1':
        image_mode = MONO8
    elif image_mode == '2':
        image_mode = MONO12
    elif image_mode == '3':
        image_mode = MONO16
    else:
        print("Invalid input! Aborting...")
        return
        
    # default file path based on conformable decoders lab setup
    file_path = "\\Users\\danig\\Documents\\Camera Runs"
    # determine where to save the runs
    default_path = input("The default file path is '" + file_path + "'. Would you like to save here? ('y' for yes, 'n' for no) ")
    # user wants to save to a new path
    if default_path == "n":
        file_path = input("Please enter a valid path you would like to save to: ")
        # check that this is a valid input
        if not os.path.exists(file_path):
            print("File path does not exist. Aborting...")
            return
    elif default_path == "y":
        pass
    else:
        print("Invalid input! Aborting...")
        return
    
    # determine if the user wants to use the camera nicknames during image saving
    nickname = input("Do you want to use camera nicknames? ('y' for yes, 'n' for no) ")
    if nickname == 'y':
        save_nickname = True
    elif nickname == 'n':
        save_nickname = False
    else:
        print("Invalid input! Aborting....")
        return
    
    # initialize the cameras
    system, cameras, file_path = initialize(image_mode, file_path, save_nickname)

    
    # begin image acquisition
    images = {}
    # manual mode - have the user signify when to take an image
    if camera_mode == MANUAL_MODE:
        count = 1
        while True:
            inp = input("Type enter to take a picture or 'e' to exit ")
            if inp == '':
                # acquire images on the user's input
                img_round = acquire_images(cameras, file_path, count, image_mode, save_nickname)
                images.update(img_round)
                del img_round
                # increase the image 'count' so that we know which round we are on
                count += 1
            elif inp == 'e':
                break
            else:
                print("Invalid input! Try again.")
    # timed mode - have the program sleep in between image round (recommended time delay is at least 1 second)
    elif camera_mode == TIMED_MODE:
        print("Time delay: " + str(time_delay))
        print("Beginning timed image acquisition...")
        time.sleep(5)
        for i in range(1, num_images+1):
            # acquire all images for the entire round first to decrease the time required between rounds
            img_round = acquire_images(cameras, file_path, i, image_mode, save_nickname)
            images.update(img_round)
            print("Image round " + str(i) + " complete")
            del img_round
            time.sleep(time_delay)
    # continuous mode - have the program take images as fast as possible
    elif camera_mode == CONTINUOUS_MODE: 
        print("Beginning continuous image acquisition...")
        time.sleep(5)
        print("Number of images: " + str(num_images))
        for i in range(1, num_images+1):
            # acquire all images for the entire round first to decrease the time required between rounds
            img_round = acquire_images(cameras, file_path, i, image_mode, save_nickname)
            images.update(img_round)
            print("Image round " + str(i) + " complete")
            del img_round
            
    # save the images that we've collected
    save_images(images, file_path, save_nickname)
    print("Image acquisition complete.")
    
    # deinitialize cameras
    for i, cam in enumerate(cameras):
        cam.DeInit()
    # remove all camera pointers
    del cam
    
    # clear camera lists before releasing
    cameras.Clear()
    system.ReleaseInstance()
    print("Done")
      
if __name__ == '__main__':
    main()
