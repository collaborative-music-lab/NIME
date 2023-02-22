# 21M.370 Pure Data Repo

## Note RE MacOS 13
For those of you with Macs having trouble, this version of PD seems to be working OK for me. In my tests it is stable except when switching audio devices - in particular something about having my iphone show up as an input over wifi seems to cause problems. 

Hopefully this ends up being a stable solution for all of us. Let me know if you run into any unexpected problems, and we can take a look together on tuesday.

http://msp.ucsd.edu/Software/pd-0.53-2test1.macos.zip

If the link above doesn't work you can try the downloads page:
http://msp.ucsd.edu/Software/
and search for pd-0.53-2test1.macos

## Automatonism

We will use a port of the excellent Automatonism library by Johan Eriksson.

https://www.automatonism.com is Johan's website and original version

The autoMITonism repo is available here: https://github.com/collaborative-music-lab/autoMITonism

This library attempts to recreated the Eurorack modular experience within Pure Data, and also simplifies some issues regarding saving the current state of your patch. The autoMITonism version just extends the functionality of the original.

To use this, first download the Vanilla version of PD:
https://puredata.info/downloads/pure-data

Then within the `Automatonism 3.0` folder open the file `main.pd`.

## To create new PD patches

One of the quirks of PD and automatonism is that you need to duplicate the ENTIRE automatonism folder everytime you create a new patch. The file called `main.pd` must be located in the main directory of your new patch, and must be left called `main.pd`. You can rename the folder itself however you like. c.f. MyCrazyPDPatch. . . 

## Notes
1. If your automatonism modules don't look correct when you first create them, try saving your patch using PD's file->save, or the associated hotkey.
2. The pd-refcard is a handy overview of available basic pd modules, and is available from https://puredata.info/docs/tutorials/pd-refcard
3. There are different versions of PD. We are using the vanilla version, which contains just the basic objects. Other versions exist with many more objects but they may not be compatible with the Raspberry Pi or other small computers.
4. For math operations the 'expr' object is extremely useful. Check out its documentation: http://yadegari.org/expr/expr.html There is also an expr~ object which will work with audio signals.

### FAQ
- PD can't find an object, either the console gives a warning or the object outline is dashed.

First off, you must set your file paths so PD knows where to find custom objects. There is at least one folder you must include- github/NIME/Puredata/externals
- PD isn't aware of subfolders so set each folder individually

This can also happen if your file preferences aren't set correctly. I recommend having two folders on your computer: one for the github repo,  which will only contain files pulled from github and another folder for your own files. In PD->Preferences->Path make sure to add both folders. You may also need to directly include the externals folder from NIME/Puredata/externals

- PD doesn't remember my filepaths even though I set them

Try selecting PD->preferences->save all preferences. This should save them in a standard location for your OS. This link talks about where that location might be so you can take a look and see if the preferences are being saved correctly:
https://puredata.info/docs/faq/pdsettings


- How can I clear the PD console? 

Control/Command + Shift + L

- How do i create an object?

Make sure you are in edit mode, and then go to the 'put' menu. All of the available object types and their hot keys will be displayed. For a list of the available objects check the cheat sheet below, or right click the blank PD canvas and select 'help'.

# PD resources
1. The PD cheat sheet - overview of all available objects in vanilla; https://puredata.info/docs/tutorials/pd-refcard
2.FLOSS manual: http://write.flossmanuals.net/pure-data/introduction2/
3. https://puredata.info/docs
4. Miller Puckette's (the creator of PD) book 'Theory and Technique of Electronic Music' http://msp.ucsd.edu/techniques.htm
5. http://www.pd-tutorial.com

**
