# Monocular Slam for Raspberry Pi 4

this repo was copied and modified from the [GitHub Pages](https://github.com/geohot/twitchslam/tree/master) 
Tweak some lines of code in order to successfully run on my Raspberry Pi.
![image](https://github.com/wisnukusuma/Monocular-Slam/assets/33643189/2a858c49-0966-4b7d-9437-97be28e41199)
```
python3 slam.py
```
Classes
-----

* Frame -- An image with extracted features
* Point -- A 3-D point in the Map and its 2-D Frame correspondence
* Map -- A collection of points and frames
* Display2D -- SDL2 display of the current image
* Display3D -- Pangolin display of the current map

Libraries Used
-----

* SDL2 for 2-D display   : pip install PySDL2
* cv2 for feature extraction : pip install opencv-python
* pangolin for 3-D display : https://github.com/uoip/pangolin/tree/master
* g2opy for optimization (soon!)

LICENSE
-----

All my code is MIT licensed. Videos and libraries follow their respective licenses.

# Monocular-Slam
