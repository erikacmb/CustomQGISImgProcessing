# Custom QGIS Image Processing Algorithm

This is a custom Python algorithm to load, convert to raster layer and merge several images of brazilian states. 

## Set Up

1. Create a main folder, i.e. `project`. 
2. Create subfolders with brazilian states abbreviations and the federal district: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP and TO. You need to create them even if you don't have images to put inside them right now.

IMPORTANT: Make sure you put the images corresponding to the raster bands B4, B5 and B6.

**Python version:** 3.8.2 and above.

## Use

On QGIS Python console, run the full script. 

IMPORTANT: do not forget to replace YOUR_FOLDER_PATH by your folder full path. 

```python
generate_merged_files('YOUR_FOLDER_PATH')
```

## How does it work?

The main purpose is to go through each subfolder looking for TIF files ending in B4, B5 and B6. The algorithm will get the full path for each file.

After that, each file will be converted into a raster layer. The algorithm will generate a list of raster layers with corresponding names.

Finally, the algorithm will group the files into sublists containing B4, B5 and B6 bands, merge and generate a MERGED file.
