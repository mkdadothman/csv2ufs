#!/usr/bin/python3

# ufs2csv.py -- Convert an Ultrafast Systems binary .ufs file to .csv
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

def readString(filedata, cursor):
    """Read a string from the filedata at position given by the cursor.
    
    An unsigned 32 bit integer gives length of string in bytes, then string data follows.
    Returns the string and the incremented cursor value as a tuple."""
    
    string_length = struct.unpack_from('>I', filedata, offset=cursor)
    cursor += 4
    string = struct.unpack_from('>{}s'.format(string_length[0]), filedata, offset=cursor)
    cursor += string_length[0]
    return (string[0].decode('utf8'), cursor)

def readUInt(filedata, cursor):
    """Read an unsigned 32 bit integer from the filedata at position given by the cursor.
    
    Returns the number and the incremented cursor value as a tuple."""
    
    number = struct.unpack_from('>I', filedata, offset=cursor)
    cursor += 4
    return (number[0], cursor)
    
def readDouble(filedata, cursor):
    """Read an 64 bit floating point number from the filedata at position given by the cursor.
    
    Returns the number and the incremented cursor value as a tuple."""
    
    number = struct.unpack_from('>d', filedata, offset=cursor)
    cursor += 8
    return (number[0], cursor)

def readDoubles(filedata, cursor, count):
    """Read a series of 64 bit floating point numbers from the filedata at position given by the cursor.
    
    Returns the list of numbers and the incremented cursor value as a tuple."""
    
    numbers = struct.unpack_from('>{}d'.format(count), filedata, offset=cursor)
    cursor += 8*count
    return (list(numbers), cursor)

if __name__ == '__main__':
    # Show file open dialog if no input files specified on command line
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        from tkinter import Tk, filedialog
        tk_root = Tk()
        tk_root.withdraw()
        filenames = list(filedialog.askopenfilenames(parent=None, title='Select ufs input files...'))
        tk_root.destroy()
        if len(filenames) < 1:
            print('No input files selected. Exiting.')
            exit(1)
    
    for filename in filenames:
        f = open(filename, 'rb')
        filedata = f.read()

        # Keep track of our current location through the file
        cursor = 0x0

        (version, cursor) = readString(filedata, cursor)

        (axis1_label, cursor) = readString(filedata, cursor)
        (axis1_units, cursor) = readString(filedata, cursor)
        (axis1_count, cursor) = readUInt(filedata, cursor)
        (axis1_data, cursor) = readDoubles(filedata, cursor, axis1_count)

        (axis2_label, cursor) = readString(filedata, cursor)
        (axis2_units, cursor) = readString(filedata, cursor)
        (axis2_count, cursor) = readUInt(filedata, cursor)
        (axis2_data, cursor) = readDoubles(filedata, cursor, axis2_count)

        (data_label, cursor) = readString(filedata, cursor)
        (data_size0, cursor) = readUInt(filedata, cursor)
        (data_size1, cursor) = readUInt(filedata, cursor)
        (data_size2, cursor) = readUInt(filedata, cursor)

        data_matrix = []
        for row in range(data_size1):
            (row_data, cursor) = readDoubles(filedata, cursor, data_size2)
            row_data.insert(0, round(axis1_data[row], 1))
            row_data = [round(x, 7) for x in row_data]
            data_matrix.append(row_data)

        (metadata, cursor) = readString(filedata, cursor)

        print("Version string: " + version)
        print("Axis1: {}, {} values, {} to {} {}".format(axis1_label, axis1_count, axis1_data[0], axis1_data[-1], axis1_units))
        print("Axis2: {}, {} values, {} to {} {}".format(axis2_label, axis2_count, axis2_data[0], axis2_data[-1], axis2_units))
        print("Data: {} {} x {}".format(data_label, data_size1, data_size2))
        print(metadata)

        axis2_data.insert(0, 0)
        data_matrix.insert(0, axis2_data)

        with open('{}.csv'.format(filename), 'w', newline='') as csvfile:
            print('Writing CSV data to {}.csv'.format(filename))
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerows(data_matrix) 

exit(0)
