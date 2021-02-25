# 21M.370 Python Scripts

Requirements:
* Python 3.5 or greater (tested on 3.7)
* The python-osc module: https://pypi.org/project/python-osc/
(Note you also will want to use the pip python package installer. You probably already have it - if not, installation instructions are here: https://pip.pypa.io/en/stable/installing/)
* The pyserial module: follow instructions here to install: https://pip.pypa.io/en/stable/installing/
* I highly recommend using Sublime Text to edit and run python scripts. You can of course use other editors, and run scripts from the command line if you wish.
https://www.sublimetext.com

## FAQ
* **How do I know if I have python 3 installed?** 
	* Open the terminal and use the command `python --version`. This will give you the default version of python your computer uses. You may also try using `python3 --version`. This will only give a valid response if python 3 is installed.

* **How do I install Python packages?**
	* Use pip to install modules. In the terminal: `pip install python-osc` and `pip install pyserial`.
	* You may need to use `pip3` to install modules for python 3

	* If you have python 3 you almost certainly also have pip. If not, you can download it here:
	* https://pip.pypa.io/en/stable/installing/

* **How can I run Python3 scripts in Sublime?**
	* You'll need to set up a custom build system. It's easy - here's a video tutorial:
		* https://youtu.be/xqcTfplzr7c

	* Once you have the Python 3 build system set up and selected under Tools->Build System, then you can hit Cmd/Ctrl-B to run a script, and Ctrl-C to cancel a running script.