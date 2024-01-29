#!/usr/bin/env python
"""
INSTRUCTIONS:
(1) Place this file in you YSFlight Directory at the same level as your aircraft, scenery, and ground folders
(2) Run this file
(3) Be patient... Lots of DAT files to process.

Note: this was writen and tested with Python 3.11.4. Older versions may encounter errors. Only tested succesfully on Mac Os 10.13.6. Other operating systems may encounter errors.

Note: May change characters, especially Japaneese characters in text files, so please see the original addon files for full REM notes.

"""

__author__ = "Decaff42"
__contributor__ = "waspe414 a.k.a. Ultraviolet"
__version__ = "1.1"
__date__ = "27 January 2024"
__license__ = "CC BY-NC, https://creativecommons.org/licenses/by-nc/4.0/"


# import python modules
import os


# Define custom functions
def import_dat(filepath):
    """Import a dat file as a list of lists"""
    data = list()
    with open(filepath, mode='r', encoding='utf-8-sig', errors='ignore') as dat_file:
        data = dat_file.readlines()

    return data

def write_dat(filepath, data):
    """Overwrite a dat file with files. Assume that all entries in data end with \n"""
    with open(filepath, mode='w',  encoding='utf-8-sig') as dat_file:
        for line in data:
            dat_file.write(line)

# define the script 
                    
# Find all dat files in the ysflight directory
list_of_files = list()
for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for filename in filenames:
        if filename.lower().endswith('.dat'):
            list_of_files.append(os.path.join(dirpath, filename))

num_dats = len(list_of_files)

# For each file, deterine if it is for a helicopter.
patch_adder = ['\n','REM Helo Patch for 2015\n','PSTMPWR1 -0.1\n','PSTMPWR2 -0.1\n']  # Ensure all end with \n
for file_idx, filepath in enumerate(list_of_files):
    # let the user know how the code's progress is going.
    if file_idx > 0 and file_idx % 50 == 0:
        print("Processing DAT file {} of {}".format(file_idx + 1, num_dats))

    # import the dat file as a list of strings.
    try:
        dat_lines = import_dat(filepath)
        old_dat_lines = dat_lines
        
        if any(item.startswith("AIRCLASS HELICOPTER") for item in dat_lines) is True:
            # Determine if the helicopter patch is already installed
            print(os.path.relpath(filepath, os.getcwd()))
            if any(item.startswith("PSTMPWR1") for item in dat_lines) is True:
                # We will assume that it is already installed.
                print("  Determined that {} already had the patch installed.".format(os.path.basename(filepath)))
            else: 
                # Need to add the helicopter patch at the end
                if 'AUTOCALC' in dat_lines:
                    idx = dat_lines.index("AUTOCALC") - 1
                elif 'AUTOCALC\n' in dat_lines:
                    idx = dat_lines.index("AUTOCALC\n") - 1
                else:
                    idx = len(dat_lines) - 2
                dat_lines = dat_lines[:idx] + patch_adder + ["\n"] + dat_lines[idx:]

                if 'AUTOCALC\n' not in dat_lines:
                    dat_lines.append('AUTOCALC\n')

                write_dat(filepath, dat_lines)
    except:
        print("  Was unable to proess {} due to an error.".format(os.path.relpath(filepath, os.getcwd())))
