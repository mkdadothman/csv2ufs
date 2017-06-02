#!/usr/bin/python3

# csv2ufs.py -- Convert a .csv file to Ultrafast Systems .ufs binary format
# Patrick Tapping 2016

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, csv, struct

def writeString(ufsfile, string):
    ufsfile.write(struct.pack('>I', len(string)))
    ufsfile.write(struct.pack('>{}s'.format(len(string)), string))

def writeUInt(ufsfile, value):
    ufsfile.write(struct.pack('>I', value))

def writeDouble(ufsfile, value):
    ufsfile.write(struct.pack('>d', value))

def writeDoubles(ufsfile, values):
    ufsfile.write(struct.pack('>{}d'.format(len(values)), *values))

if __name__ == '__main__':
    # Show file open dialog if no input files specified on command line
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        from tkinter import Tk, filedialog
        tk_root = Tk()
        tk_root.withdraw()
        filenames = list(filedialog.askopenfilenames(parent=None, title='Select csv input files...'))
        tk_root.destroy()
        if len(filenames) < 1:
            print('No input files selected. Exiting.')
            exit(1)

    for filename in filenames:
        with open(filename, 'r', newline='') as csvfile:
            print('Reading CSV data from {}.csv'.format(filename))
            csvreader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            
            version = b'Version2'
            
            axis1_label = b'Wavelength'
            axis1_units = b'nm'
            axis1_data = []
            
            axis2_label = b'Time'
            axis2_units = b'ps'
            axis2_data = csvreader.__next__()
            axis2_data = axis2_data[1:]
            
            data_label = b'DA'
            data_matrix = []
            try:
                for row in csvreader:
                    axis1_data.append(row[0])
                    data_matrix.append(row[1:])
            except ValueError:
                # TODO, could read metadata block here...
                pass
            
            axis1_count = len(axis1_data)
            axis2_count = len(data_matrix[0])
            
            metadata = "Converted from {}".format(filename)
            metadata = bytearray(metadata, 'ascii')
            
            print("Version string: " + version.decode('utf8'))
            print("Axis1: {}, {} values, {} to {} {}".format(axis1_label.decode('utf8'), axis1_count, axis1_data[0], axis1_data[-1], axis1_units.decode('utf8')))
            print("Axis2: {}, {} values, {} to {} {}".format(axis2_label.decode('utf8'), axis2_count, axis2_data[0], axis2_data[-1], axis2_units.decode('utf8')))
            print("Data: {} {} x {}".format(data_label.decode('utf8'), axis1_count, axis2_count))
            print(metadata.decode('utf8'))
            
            print('Writing UFS data to {}.ufs'.format(filename))
            ufsfile = open('{}.ufs'.format(filename), 'wb')
            
            writeString(ufsfile, version)
            
            writeString(ufsfile, axis1_label)
            writeString(ufsfile, axis1_units)
            writeUInt(ufsfile, axis1_count)
            writeDoubles(ufsfile, axis1_data)
            
            writeString(ufsfile, axis2_label)
            writeString(ufsfile, axis2_units)
            writeUInt(ufsfile, axis2_count)
            writeDoubles(ufsfile, axis2_data)
            
            writeString(ufsfile, data_label)
            writeUInt(ufsfile, 0)
            writeUInt(ufsfile, axis1_count)
            writeUInt(ufsfile, axis2_count)
            for row in range(axis1_count):
                writeDoubles(ufsfile, data_matrix[row])
            
            writeString(ufsfile, metadata)

exit(0)
