# seq2py

## Purpose
Auto-generate basic labscript code from Cicero .seq files for migrating from Cicero/Atticus to labscript. Also contains basic diff functionality for comparing Cicero sequences.

## Usage
First .seq files must be converted to (human-readable) .yaml via the functionality from https://github.com/achuang2718/ciceroSeq2Yaml. The .yaml file can then be directly passed into the various utility functions by specifying the file path.

## Dependencies
See `requirements.txt` and `environments.yml`. Also requires .csv files mapping Cicero channel indices to labscript analog/digital outputs (see e.g. `exampleFiles/channelSettings`).
