# Robot Normalization
Creates normalization protocol for OT-2 Robot when given DNA concentrations

# File Requirements
DNA concentration values (ng/µl) in a csv file. The function accepts two format types:
1. A csv file containing a single column named dna_con that contains concentrations in plate order (i.e., A1, B1...G12, H12).
2. A csv file containing DNA concentrations in plate format (i.e., 8x12 matrix). This is the same format produced by our Tecan plate reader. You simply need to deleted any min or max and standard values. The files plate_reader.csv and not_plate.csv are examples of the plate_reader and dna_column formats, respectively. 

# Arguments
The function has eight arguments that can be changed. 
```
# Name of csv file containing concentration values
dna_file = 'plate_reader.csv'

# Format of concentration file
data_format = 'plate_reader' or 'dna_column'

# Naming scheme for output files
base_name = 'DM.2022.12.17'

# Minimum volume (µl) of DNA to use for normalization. The minimum is 1 µl but 2 µl is ideal
sample_min = 5.0

# Minimum volume (µl) in each well after normalization
total_vol_min = 25.0

# Final DNA concentration (ng/µl) of each sample
final_con = 5.0

# Voleum of DNA (µl) to add if DNA concentration is less than desired DNA concentration (i.e., final_con)
low_con_add = 10.0

# Simulate protocol in OT-2
simulate_run = 'yes' or 'no'
```

# Output Files
The function produces four files (3 csv and 1 python):
1. basename_normalization_protocol.py
2. basename_normalization.csv
3. basename_overages.csv
4. basename_too_low.csv
