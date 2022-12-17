# Robot Normalization
Creates normalization protocol for OT-2 Robot

# File Requirements
DNA concentration values in a csv file.

# Variables
1. dna_file = name of csv file containing DNA concentrations
2. data_format = plate_reader or dna_column
3. base_name = naming scheme for output files
4. sample_min = minimum amount (µl) of DNA to use
5. total_vol_min = minimum volume amount (µl) in each well
6. final_con = desired DNA concentration (ng/µl) of each sample
7. low_con_add = amount (µl) of DNA to add if DNA concentration is less than desired DNA concentration (i.e., final_con)
8. simulate_run = yes or no

# Running Function
