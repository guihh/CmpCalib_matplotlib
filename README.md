## CmpCalib_matplotlib

Tool to display output of the CmpCalib command from MicMac (IGN)

#### Recommanded requirements :

- CPython  >2.6 	
- numpy 1.11 	
- matplotlib 1.5.3	
- scipy 0.18.1	
- collections 
- os 
- argparse

if you have any problem with cm, please try to upgrade matplotlib :
```
$ sudo pip install matplotlib --upgrade 
```	

#### How it works :

1. First, use the mm3d CmpCalib between 2 Ori-{...}/AutoCal{...}.xml files to produce the .txt comparaisons file. 
2. Second give rights the python's scripts. 
3. Then lauch ./CmpCalib_matplotlib.py with the txt file(s) as arg(s) 
```
$ mm3d CmpCalib Ori-XXXX/AutoCal_* Ori-YYYY/AutoCal_* Out=file_to_plot.xml
$ sudo chmod +x CmpCalib_matplotlib.py
$ ./CmpCalib_matplotlib.py file(s)_to_plot.txt 
```


#### Example :

In examples folder, you'll find 5 files which are the comparison between 1 reference calibration and 4 others  : 
```
$ python CmpCalib_matplotlib/scripts/CmpCalib_matplotlib.py CmpCalib_matplotlib/examples/PDV_1/PDV_1__PDV_* -m 0.8 -i cubic
```
*Thresholding to 0.8 pixels delta and choose cubic interpolation.*
*Output is a PNG file located in the same folder as the input file(s).*

#### Optional arguments:
```
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Absolute path to save
  -m MAX_SCALE, --max_scale MAX_SCALE
                        Maximum deviation value to plot. Default is maximum
                        deviation from input file(s).
  -c NBCLASS, --nbclass NBCLASS
                        Number of classes for the LUT. Default is 50.
  -f FONTSIZE, --fontsize FONTSIZE
                        Fontsize. Default is 17.
  -l LINEWIDTH, --linewidth LINEWIDTH
                        Width of the line to plot. Default is 1.75.
  -r RATIO, --ratio RATIO
                        Padding in each "Ecarts Planimetriques" frame (% of
                        maximum value X & Y). Useful to displayed whole
                        plotted arrows. Default is 0.2.
  -sc SCALE_OUTPUT, --scale_output SCALE_OUTPUT
                        coefficient to choose scale of image output.
  -i INTERPOLATION_MODE, --interpolation_mode INTERPOLATION_MODE
                        Choose between: {‘linear’, ‘nearest’,
                        ‘cubic’}. Default is linear
  -w WIDTH_ARROWS, --width_arrows WIDTH_ARROWS
                        Width of the arrows. Default is 0.03

```
###### Authors :

Herault Guillaume & Benjamin Grigoroff

