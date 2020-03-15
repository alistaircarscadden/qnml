## QUICK NML

## Deisgned and developed by Alistair Carscadden
## March 2020

import sys
import os
import time

time_start = time.perf_counter()

qnml_header_comment = '''/* nml generated with qnml preprocessor
*/
 
 '''

qnml_pre_file_comment = '''
/* {}
*/
 
 '''

src = 'src/'
qnml_extension = '.qnml'
header = f'header{qnml_extension}'

def print_usage():
    usage = 'Usage: qnml.py <output_file>'
    print(usage, file=sys.stderr)

def warn_filesize(file_path):
    warn = f'Warning: {file_path} is empty'
    print(warn, file=sys.stderr)

def fatal_header_missing():
    warn = 'Fatal: source directory is missing header.qnml'
    print(warn, file=sys.stderr)
    
def warn_no_files():
    warn = f'Warning: no non-header qnml files in {src}'
    print(warn, file=sys.stderr)

def warn_extension():
    warn = 'Warning: the output file does not have a .nml extension. This script does not add one.'
    print(warn, file=sys.stderr)

def warn_non_qnml_files(amt):
    warn = f'Warning: {amt} files in {src} are not qnml and were skipped'
    print(warn, file=sys.stderr)

if __name__ == '__main__':
    try:
        nml_out = sys.argv[1]
    except IndexError:
        print_usage()
        exit(1)
        
    # If the output file does not have the '.nml' extension it is warned
    if os.path.splitext(nml_out)[1] != '.nml':
        warn_extension()
    
    with open(nml_out, 'w') as nml:
        # Write the qnml opening comment
        nml.write(qnml_header_comment)
        
        # Discover and store all the files in the source directory
        qnml_list = os.listdir('src')
        
        # Remove the header.qnml from the list, as it will be written first
        try:
            qnml_list.remove(header)
        except ValueError:
            # and if there is no header.qnml it is fatal
            fatal_header_missing()
            exit(1)
        
        num_files_in_src = len(qnml_list)
        
        # Remove all the non-.qnml files from qnml_list
        qnml_list = [f for f in qnml_list if os.path.splitext(f)[1] == qnml_extension]
        
        # Warn if there are non-qnml files in the src
        num_non_qnml_files_in_src = num_files_in_src - len(qnml_list)
        if num_non_qnml_files_in_src > 0:
            warn_non_qnml_files(num_non_qnml_files_in_src)
        
        # Sort the list. To add, uh, determinism
        qnml_list.sort()
        
        # If the list is empty (there are no qnml files apart from the header)
        if not qnml_list:
            warn_no_files()
    
        # Append header.qnml into the output file
        header_path = os.path.join(src, header)
        with open(header_path, 'r') as file:
            print(f'{nml_out} < {header_path}')
            nml.write(qnml_pre_file_comment.format(header_path))
            filesize = nml.write(file.read())
            
            # If any files are empty, warn about it
            if filesize == 0:
                warn_filesize(header_path)
        
        # Append the rest of the .qnml's into the output file
        for qnml_file in qnml_list:
            file_path = os.path.join(src, qnml_file)
            with open(file_path, 'r') as file:
                print(f'{nml_out} < {file_path}')
                nml.write(qnml_pre_file_comment.format(file_path))
                filesize = nml.write(file.read())
            
                if filesize == 0:
                    warn_filesize(header_path)

    time_end = time.perf_counter()
    time_elapsed = time_end - time_start
    print(f'Done in {time_elapsed:.6}s')