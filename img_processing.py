import os
from qgis.core import (QgsVectorLayer, QgsRasterLayer)
import processing

"""
Generic Methods
"""

def is_desired_raster_band(path, raster_band):
    """Check if the path matches a file with the raster band of interest.

    Args:
        path -- string with the full path
        raster_band -- string with the raster band of interest
    """
    return not (path.find(raster_band) == -1)


def get_all_paths(directory, extension = 'tif', raster_bands = ['B4', 'B5', 'B6']):
    """Get all paths from the specified directoy and return them as a list. It is expected that the specified directory contains subfolders for each brazilian state, and the subfolder name should be the state abbreviation AC, AL, etc.

    Args:
        directory -- string with the directory path
        extension -- string with the extension without the dot (default is 'tif')
        raster_bands -- list with the raster bands of interest (default is ['B4', 'B5', 'B6'])
    """
    ufs = ('AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 
    'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO')

    all_paths = []   

    for uf in ufs:
        subdirectory = directory + uf + "/"
        for path in os.listdir(subdirectory):
            if path[-4:].upper() == str('.' + extension.upper()):
                full_path = os.path.join(subdirectory, path)
                if os.path.isfile(full_path):
                    for raster_band in raster_bands:
                        if is_desired_raster_band(full_path, raster_band):
                            all_paths.append(full_path)

    return sorted(all_paths)


"""
QGIS Methods
"""

def load_layers(paths):
    """Load layers from obtained paths.

    Args:
        paths -- list with the full paths
    """
    layers = []

    for path in paths:
        layer = QgsRasterLayer(path, path)
        if not layer.isValid():
            print('Failed to load layer from path %s!' % path)
        else:
            layers.append({ 'layer': layer, 'path': path })

    return layers


def split_layer_list_and_merge(layers):
    """Split the layers list into sublists (3 layers inside each list) and then applies the merge method. 

    Args:
        layers -- list with the full paths of ALL raster layers
    """
    sublists = [layers[x:x+3] for x in range(0, len(layers), 3)]
    for sublist in sublists:
        path = merge(sublist)
        print('Merged file available at: %s' % path)


def merge(layers):
    """Merge raster layers from obtained paths. 
    IMPORTANT: This is NOT a generic method once it considers the following order: B5, B6, B4.

    Args:
        layers -- list with the full paths of 03 raster layers
    """
    ordered_layers = ['', '', '']

    if not layers[0]['path'].find('B4') == -1:
        ordered_layers[2] = layers[0]['path']

    if not layers[1]['path'].find('B5') == -1:
        ordered_layers[0] = layers[1]['path']

    if not layers[2]['path'].find('B6') == -1:
        ordered_layers[1] = layers[2]['path']

    band_on_string_path = layers[0]['path'].find('_B')
    string_to_be_replaced = layers[0]['path'][band_on_string_path+1:band_on_string_path+3]
    path_and_filename = layers[0]['path'].replace(string_to_be_replaced, 'MERGED')

    parameters = { 
        'INPUT': ordered_layers,
        'PCT': False,
        'SEPARATE': True,
        'DATA_TYPE': 2,
        'NODATA_INPUT': None,
        'NODATA_OUTPUT': 0,
        'OPTIONS': 'BIGTIFF=YES',
        'EXTRA': None,
        'OUTPUT': path_and_filename
    }
    
    processing.run('gdal:merge', parameters)

    return path_and_filename

def generate_merged_files(folder_path):
    """Generate merged files from specified folder path.

    Args:
        folder_path -- string with the full path of the main folder
    """
    paths = get_all_paths(folder_path)
    print('%d files loaded.' % len(paths))
    layers = load_layers(paths)
    print('%d layers loaded.' % len(layers))
    split_layer_list_and_merge(layers)


"""
Main program
"""

# DO NOT FORGET TO REPLACE THIS FOR SOMETHING LIKE C:/your_folder/ 
generate_merged_files('YOUR_FOLDER_PATH')
