# CSV to UFS Conversion

These python scripts convert to and from the text-based comma separated values (.csv) and the binary Ultrafast Systems (.ufs) file format.
These file types are used to store the raw matrix data from transient absorption or time-resolved fluorescence experiments.

The most recent versions of the spectrometer software from Ultrafast Systems save into the binary .ufs format, but older versions of the software save in .csv format. Recent versions of the Surface Xplorer analysis tool can only open .ufs files. These scripts allow the old .csv format data to be converted for use in the new Surface Xplorer, and for new .ufs files to be converted to standard .csv for analysis or plotting in other software.

## Requirements

+ Python 3

Has been tested on Python 3.4 on Windows XP and Python 3.5.2 on Arch Linux.

## Usage

Output filenames will the same as the input filenames, with `.ufs` or `.csv` appended as appropriate, for example `infile1.ufs.csv`. Warning -- If the output file exists, it will be overwritten without prompting!

### Convert .csv file(s) to .ufs:

`python3 csv2ufs.py infile1.csv [infile2.csv...]`

### Convert .ufs file(s) to .csv:

`python3 ufs2csv.py infile1.ufs [infile2.ufs...]`

## CSV File Specification

The comma separated values data is simply a matrix with the first row defining the time axis and the first column defining the wavelength axis. The first cell (row 0, column 0) is not used and is usually set to zero. Cell data is the absorption or intensity value. Following the data matrix is any experiment metadata stored as simple unstructured text.

The exact format of the input file should be somewhat flexible as the scripts use the standard Python CSV libraries. It is likely that space or tab separated values would also work, although this has not been tested.  

## UFS File Specification

The `.ufs` files contain the exact same information as the `.csv`, but stored in a binary format. In general, this consists only of 32-bit unsigned integers, 64-bit (double precision) floating point numbers and text strings (with unspecified encoding, assumed UTF8). All numbers are stored in big-endian. Text strings are prefixed by an unsigned 32-bit integer describing the length of the string in bytes.

The file then composed of the following data blocks:

+ A version string, eg. "Version2"
+ The first axis label string (the label for the row data), eg. "Wavelength"
+ The first axis unit string (units for the row data), eg. "nm"
+ The first axis value count as an integer (the number of rows), eg 123
+ A series of /rows/ double precision numbers for the first axis tic labels, eg 420.4 421.5 422.6...
+ The second axis label string (the label for the column data), eg. "Time"
+ The second axis unit string (units for the column data), eg. "ps"
+ The second axis value count as an integer (the number of columns), eg 456
+ A series of /columns/ double precision numbers for the second axis tic labels, eg -0.05 -0.01 0.03 0.07 ...
+ A string designating the start of the data, eg "DA"
+ The integer value zero (unknown purpose), eg. 0
+ The integer number of rows in the following data matrix (should be same as /rows/ above), eg. 123
+ The integer number of columns in the following data matrix (should be same as /columns/ above), eg. 456
+ A series of /rows/*/columns/ double precision numbers of data values, in row-major order (all time values for a given wavelength first)
+ A single string containing the metadata, eg. "Solvent: H20\r\nDate: 1/9/2016\r\n"




