# Robot Normalization
Creates normalization protocol for OT-2 Robot from a file of DNA concentrations

# File Requirements from the User
The user might provide DNA concentration values (ng/µl) in a csv file. The function accepts two format types:
1. A csv file containing a single column named dna_con that contains concentrations in plate order (i.e., A1, B1...G12, H12).
2. A csv file containing DNA concentrations in plate format (i.e., 8x12 matrix). This is the same format produced by our Tecan plate reader. You simply need to deleted any min or max and standard values. The files plate_reader.csv and not_plate.csv are examples of the plate_reader and dna_column formats, respectively. 

# File Requirements for the Function
The function requires two python files to run correctly. The first, DM-normalization.py, is the basic OT-2 Robot protocol for normalization. The second, create_normalization_protocol.py, calculates the volume of DNA and water to add to each well and changes the values in DM-normalization.py accordingly. It also produces the output files listed below. You should not alter either of these files. 

# Arguments
The function has eight arguments. 
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

# Volume of DNA (µl) to add if DNA concentration is less than desired DNA concentration (i.e., final_con)
low_con_add = 10.0

# Simulate protocol in OT-2
simulate_run = 'yes' or 'no'
```

# Output Files
The function produces four files (1 python and 3 csv):
1. base_name_normalization_protocol.py
    - Can be imported directly to the OT-2 robot to run the normalizaiton protocol 
2. base_name_normalization.csv
    - Provides the normalization specifics of the protocol
3. base_name_overages.csv
    - Provides the samples that cannot be normalized in 100 µl (i.e., the DNA concentration is too high). With the information provide, however, you can normalize the samples in centrifuge tubes and add them to the normalization plate
4. base_name_too_low.csv
    - Provides the samples that cannot be normalized because the concentration is too low

# Running the Function
