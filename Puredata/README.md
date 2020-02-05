# 21M.370 Pure Data Repo

We will use the excellent Automatonism library by Johan Eriksson. 

https://www.automatonism.com

This library attempts to recreated the Eurorack modular experience within Pure Data, and also simplifies some issues regarding saving the current state of your patch.

To use this, first download the Vanilla version of PD:
https://puredata.info/downloads/pure-data

Then within the `Automatonism 3.0` folder open the file `main.pd`.

## To create new PD patches

One of the quirks of PD and automatonism is that you need to duplicate the ENTIRE automatonism folder everytime you create a new patch. The file called `main.pd` must be located in the main directory of your new patch, and must be left called `main.pd`. You can rename the folder itself however you like.