
from create_normalization_protocol import normalize

normalize(
    dna_file = 'plate_reader.csv',
    data_format = 'plate_reader',
    base_name = 'DM.2022.12.17',
    sample_min = 2,
    total_vol_min = 10,
    final_con = 5,
    low_con_add = 0,
    simulate_run= 'yes'
)
