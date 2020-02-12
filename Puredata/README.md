# 21M.370 Pure Data Repo

We will use the excellent Automatonism library by Johan Eriksson. 

https://www.automatonism.com

This library attempts to recreated the Eurorack modular experience within Pure Data, and also simplifies some issues regarding saving the current state of your patch.

To use this, first download the Vanilla version of PD:
https://puredata.info/downloads/pure-data

Then within the `Automatonism 3.0` folder open the file `main.pd`.

## To create new PD patches

One of the quirks of PD and automatonism is that you need to duplicate the ENTIRE automatonism folder everytime you create a new patch. The file called `main.pd` must be located in the main directory of your new patch, and must be left called `main.pd`. You can rename the folder itself however you like. c.f. MyCrazyPDPatch. . . 

## Notes
1. If your automatonism modules don't look correct when you first create them, try saving your patch using PD's file->save, or the associated hotkey.
2. The included pd-refcard is a handy overview of available basic pd modules, and comes from https://puredata.info/docs/tutorials/pd-refcard
3. There are different versions of PD. We are using the vanilla version, which contains just the basic objects. Other versions exist with many more objects but they may not be compatible with the Raspberry Pi or other small computers.

# PD resources
1. FLOSS manual: http://write.flossmanuals.net/pure-data/introduction2/
2. https://puredata.info/docs
3. Miller Puckette's (the creator of PD) book 'Theory and Technique of Electronic Music' http://msp.ucsd.edu/techniques.htm
