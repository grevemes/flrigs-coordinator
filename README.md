# flrigs-coordinator

This program was created to facilitate the coordination of settings across multiple radios.  Actual radio control is handled by flrig instances.

```angular2html
usage: flrigs-coordinator [-h] [-v] [-c CONFIG] [-d] {show,save,restore,set,swap} 

Coordinate settings across multiple flrig instances

positional arguments:
    show                Display current radio settings
    save                Store the current radio settings
    restore             Restore the radio settings from saved values
    set                 Set destination radio to match the source radio settings
    swap                Swap the settings between two radios

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
  -d, --debug
```

## Configuration:  
Configuration is defined in an ini-format file.  The following is provided as an exmaple.

```
[IC7300]
description = ICOM 7300
server = 192.168.5.11
port = 12345

[KX3]
description = Elecraft KX3
server = 192.168.5.42
port = 12345
```

## Examples:    

**flrigs-coordinator show IC7300**  
Show the settings from a specific defined radio:
```
KX3: "Elecraft KX3" 28362000Hz USB 50W
```

**flrigs-coordinator save KX3**    
Save the current radio settings to the INI file:
```
Saving KX3 settings of 28362000 USB
```

**flrigs-coordiantor restore KX3**
Restore the setting from the INI file to the radio.
```
Resorting KX3 to 28362000 USB
```

**flrigs-coordiantor set IC7300 KX3**     
Copy settings from the source radio, IC7300, to the destination radio, KX3.
```angular2html
Copy settings from IC7300 to KX3 : 7175000 USB
```

**flrigs-coordiantor swap KX3 IC7300**  
Swap the settings between the two radios.
```
Swap settings from IC7300 to KX3
```

### Credits:
This initial version of this program was derived from
FLRig HF Scanner (https://github.com/jrobertfisher/flrig-hf-scanner)