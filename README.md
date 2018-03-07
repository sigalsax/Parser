# Parser

### ABOUT
- parser.py parses through files, unzips them and extracts the important pieces of data according to a set of rules
- crashedLogs.txt records all the folders that could not be unzipped (7Zip)
- formatMisalignmentRule4.txt records all the files that do not have the proper formatting for the program
- must update path in main

### INSTRUCTIONS
- ensure that crashedLog.txt file follows the path C:\Users\Administrator\Desktop\Parser\crashedLog.txt
- ensure that formatMisalignmentRule4.txt file follows the path C:\Users\Administrator\Desktop\Parser\formatMisalignmentRule4.txt

### BUGS
- if folder is 7Zipped, the program will be unable to unzip and will skip folders, logging them in 'crashedLog.txt'.

### FUTURE DEVELOPMENT/NOTES
- the parser is intended to parse through folders, unzip them (if they are not 7Zipped) 
- The program prints the extracted information but in later iterations, the program will save that data into a CSV to be formatted accordingly. 
