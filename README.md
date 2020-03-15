# qnml
### Quick NML preprocessor

Take all of the `.qnml` files in `src/` and concatenates them into one file given as a command line argument.

### Usage

`py qnml <output>`
`output` should be the desired `.nml` (`output.nml` for example)

The `qnml.py` script should be put in the root directory of the GRF project.
All of the .qnml files should be placed in `src/` and should contain valid nml.
The input files are taken from this directory and put into the output file `src/header.qnml` first, and the rest follow in alphabetical order.

### Requirements

Python 3

Tested with 3.8.2 only.