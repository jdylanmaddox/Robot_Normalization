# Robot Normalization
Creates normalization protocol for OT-2 Robot

# File Requirements
DNA concentration values (ng/µl) in a csv file

# Arguments
```
# Name of csv file containing concentration values
dna_file = 'plate_reader.csv'

# Format of concentration file
data_format = 'plate_reader' or 'dna_column'

# Naming scheme for output file
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
simulate_run = yes or no
```
