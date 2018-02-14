# Basic Usage:
## cdrom_ecc.py
Modified EDC/ECC regeneration functions. Credit to abyssonym for the original.

```
# original_data (12sync, 4header, 2048data, 4ecc, 8zero, 276 edc)
# modified_data (12sync, 4header, 2048data, 4ecc, 8zero, 276 edc) (Needs new EDC/ECC)

data = modified_data[:2076]
regenerated_data = cdrom_ecc.get_edc_ecc(data)[2]

# regenerated_data (12sync, 4header, 2048data, 4ecc, 8zero, 276 edc) (New EDC/ECC)
```

# Iso Editing:
## splitter.py:
This splits out each 2352 region into a file of stacked 2048 byte blocks. Makes it more convenient for editing.

``` python2 splitter.py source.iso split.bin sync.txt```


## create_patch.py:
Creates a text patch file from a modified split file and an original split file.

``` python2 create_patch.py split.bin modified.bin patchfile.txt ```


## apply_patch.py:
Applies the patch file to an original iso.

``` python2 apply_patch.py source.iso patchfile.txt sync.txt patched.iso ```


### WIP:
Still needs testing, error catching.
splitter.py should probably split by more than just the sync pattern (Problems if that pattern can occur elsewhere)