
from create_normalization_protocol import normalize

normalize(
    dna_file = 'plate_reader.csv',
    data_format = 'plate_reader',
    base_name = 'DM.2022.12.19',
    sample_min = 5,
    total_vol_min = 10,
    final_con = 0.5,
    low_con_add = 10,
    tip_type = 'not_filtered',
    simulate_run= 'yes'
)
