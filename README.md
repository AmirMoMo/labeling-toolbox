# labeling-toolbox
The toolbox is developed for labeling images for binary classification with an additional class for uncertain samples. The Graphical User Interface (GUI) looks like the following sample with the functionalities explained afterward:
![alt text](https://github.com/AmirMoMo/labeling-toolbox/blob/master/sample.png)
# Functionality:
Please set the directory of original and relabeled datasets in the code. We assumed that the images are saved with \*.png format, and data is organized with the following structure:  
data_dir/train/good/\*.png  
data_dir/train/bad/\*.png  
data_dir/valid/good/\*.png  
data_dir/valid/bad/\*.png  
You can use any arbitrary folder structure and image format and adjust the code. Start the GUI and follow the instructions:
## Start: 
Press the start bottom to initialize the labeling toolbox.
## Label a sample:
Click one of the good/possible reject/bad samples to label a given image, and the next image pups up automatically after you made a decision.
## Back:
You can return to previous samples by clicking the back bottom.
## Save:
Pressing the save bottom moves the labeled data into the target folder based on the labels. 
## Exit:
Press exit after saving the latest labeled data to quit the GUI.
