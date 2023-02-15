# 21M.370 Framework

Repo for MIT course 21M.370 Digital Instrument Design
Taught by Ian Hattwick
- created Spring 2020
- this branch for Spring 2023

## Getting started

This framework consists of three elements:
* Firmware for the ESP32, developed using the Arduino IDE
* Python scripts for processing sensor data
* Pure Data patches for sound synthesis

Information on how to install the necessary environment for each element is located on the respective elements subfolder in this repo.

## Installing this repo

1. Choose a directory to store the repo (probably on your desktop or in your documents folder) and navigate there in the Terminal.
2. Clone the NIME repo into the folder you just chose using either GitHub Desktop or the terminal. https://help.github.com/en/articles/cloning-a-repository
3. You may need to install git tools if necessary. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Once the repo is cloned you can update it when necessary by navigating to your NIME folder in the terminal and entering the command `git pull`

## FAQ

* **Can I put the repository in Dropbox?**
No, it can't be in a Dropbox or other shared folder, but anywhere else is fine.

* **How do I navigate in Terminal?**
https://computers.tutsplus.com/tutorials/navigating-the-terminal-a-gentle-introduction--mac-3855

  * Type `pwd` in the terminal to doublecheck which directory you are in.
  
  * **What is the difference between cloning and pulling?**
Cloning creates a fresh copy of the MLE library, whereas pulling just updates the library with any changes.

  * You really only want to clone once to install the library.

* **Gimme the commands to clone and pull repos again?**
  * To clone, navigate to the folder you want to store in and type `git clone https://github.com/collaborative-music-lab/MLE/`
  * To pull, navigate to the MLE directory and type `git pull`
  * The main MLE directory is the one that contains the folders for code, doc, externals, etc
   
* **I don't seem to have git installed**
If you don't have the git tools installed on your computer, follow the directions here:
  * https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
  
## Troubleshooting

* **git pull doesn't work!**
  * If git pull is saying that there is a conflict, trying typing `git stash` and then `git pull`
  * If get pull is saying `failed: not a git repository` you may be in the wronng folder (see the question above for the command to pull a repo)
  * If you are in the right folder but still get a failure message, you may want to trash and reclone the MLE library. 
  * Make sure your folder is not in a dropbox or google drive or anything like that.
  * If nothing else works, try trashing your local NIME folder and recloning frmo github. Or you can also do a cirect download of all of these files. You'll need to reset your file preferences in PD if you do this.
  
* **I don't see data getting to PD**
You can check communication in the python script by enabling either one or the other of the below settings to 1. 

  * RAW_INCOMING_SERIAL_MONITOR = 1
   * - will show raw data coming over serial from ESP32
  * PACKET_INCOMING_SERIAL_MONITOR = 1
  * - will show packets being sent over UDP
  
  * You can also monitor data in the dataMonitoring PD patch, but you have to enable monitoring by clicking the toggle or else you won't see anything.

  * Make sure to set these back to 0 after debugging as they slow things down a lot
  
* **I can see data in the Arduino monitor but don't see it in another program (Pure Data, max, Python)**

* You may need to turn DTR on for your serial monitoring in these programs:
https://docs.platformio.org/en/latest/projectconf/section_env_monitor.html#monitor-rts
* For Max/MSP you can use the attribute @DTR 1 in the serial object.
* For Python try calling ser.flushInput() after setting up the serial connection

* **I set 'RAW_INCOMING_SERIAL_MONITOR' to 1 and don't see anything in the Python console'**
  * Try reprogramming the ESP32 with a recent firmware

* **I can see raw data, and packets in python but don't see anything in PD**
  * Make sure there isn't another PD or python script running in the background. Try looking in your activity monitor or other list of running processes and kill any python scripts, and quit and restart PD.

