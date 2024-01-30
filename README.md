To use this app firstly you need to install python from python.org 
(you need version less than 12.1, 12.0 or 11.x should work)

Then run setup.py file.
The setup file will install scoop (scoop.sh). Scoop is needed to install ffmpeg, which is needed for the programm.
Than the setup will install all required libraries



To actually use it you need launcher.py, in it you can select model, your audio file and where to process the file.

The bigger the model, the more you will need to download, and the longer it will think before answering. 
But bigger files will answer more accurately.

If you enable remote processing, it will try to send your file to my computer so it can process faster with gpu. 
