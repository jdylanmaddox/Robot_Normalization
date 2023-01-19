'''
create_normalization_protocol.py v1.1 Dec 2022
Dylan Maddox <dmaddox@fieldmuseum.org>
Creates robot normalization protocol from DNA concentrations

Requires DNA concentrations in a csv file from either
    (1) Tecan plate reader
    (2) single column named dna_con

Requires DM-normalization.py
'''

# import pandas and numpy packages
import pandas as pd
import numpy as np
import os

def normalize(dna_file = 'plate_reader.csv', data_format = 'plate_reader', base_name = '2022_12_04_p1', sample_min = 2.0,
              total_vol_min = 25.0, final_con = 10.0, low_con_add = 0.0, tip_type = 'not_filtered', simulate_run = 'yes'):

    if sample_min < 1.0:
        print('*** Sample minimum (i.e. sample_min) must be greater than 1.0 µl, but 2.0 µl is ideal')
        print('*** You used ' + str(sample_min) + ' µl')
        quit()

    if data_format == 'plate_reader':
        # reading DNA concentrations from plate reader as exported (i.e., in plate format)
        plate = pd.read_csv(dna_file, index_col=0)

        # reformatting plate DNA concentrations into a single column
        plate_col = pd.concat([plate['1'], plate['2'], plate['3'], plate['4'], plate['5'], plate['6'], plate['7'],
                               plate['8'], plate['9'], plate['10'], plate['11'], plate['12']], ignore_index=True)
        plate_con = pd.DataFrame(plate_col)
        plate_con.columns = ['dna_con']

    elif data_format == 'dna_column':
        # reading DNA concentrations from a single column named dna_con
        plate = pd.read_csv(dna_file)
        plate_con = plate

    else:
        print('*** Data Format (data_format) is not correct. It must be plate_reader or dna_column')

    # µl of DNA sample to add to each well
    sample_add = np.where((final_con*total_vol_min)/plate_con > sample_min, (final_con*total_vol_min)/plate_con, sample_min)

    # µl of H2O to add to each well
    water_add = ((plate_con * sample_add)/final_con) - sample_add

    # add columns
    plate_con['dna_ul'] = sample_add
    plate_con['water_ul'] = water_add

    # round numbers to two decimal places
    plate_con = plate_con.round(decimals=2)

    # create well locations
    wells =(    'A1','B1','C1','D1','E1','F1','G1','H1',
                'A2','B2','C2','D2','E2','F2','G2','H2',
                'A3','B3','C3','D3','E3','F3','G3','H3',
                'A4','B4','C4','D4','E4','F4','G4','H4',
                'A5','B5','C5','D5','E5','F5','G5','H5',
                'A6','B6','C6','D6','E6','F6','G6','H6',
                'A7','B7','C7','D7','E7','F7','G7','H7',
                'A8','B8','C8','D8','E8','F8','G8','H8',
                'A9','B9','C9','D9','E9','F9','G9','H9',
                'A10','B10','C10','D10','E10','F10','G10','H10',
                'A11','B11','C11','D11','E11','F11','G11','H11',
                'A12','B12','C12','D12','E12','F12','G12','H12')

    plate_con.insert(loc=0, column='dna_well', value=wells)
    plate_con.insert(loc=1, column='norm_well', value=wells)

    # remove samples with no concentration readings
    # plate_con = (plate_con.loc[plate_con['dna_con'] > 0])

    # calculate basic stats
    dna_con_min = np.min(plate_con['dna_con'])
    dna_con_max = np.max(plate_con['dna_con'])
    dna_con_avg = np.mean(plate_con['dna_con'])
    dna_con_avg = dna_con_avg.round(decimals=2)

    print('---> Minimum DNA Concentration = ' + str(dna_con_min))
    print('---> Maximum DNA Concentration = ' + str(dna_con_max))
    print('---> Average DNA Concentration = ' + str(dna_con_avg))
    print('')

    # create new dataframe for samples with too much liquid (i.e., won't fit into wells)
    overages = plate_con[plate_con['dna_ul'] + plate_con['water_ul'] >= 100]
    overage_num = len(overages. index)
    if overages.empty:
        print('*** All samples have < 100 µl of liquid ***')
    else:
        print('*** ' + str(overage_num) + ' sample(s) have too much liquid ***')
        print('---- See overages.csv file for specifics ----')
        print(overages)
        print('')

    # create new dataframe for samples with too low concentrations
    too_low = plate_con[plate_con['dna_con'] < final_con]
    too_low_num = len(too_low. index)
    if too_low.empty:
        print('*** No samples have too low concentrations ***')
    else:
        print('*** ' + str(too_low_num) + ' samples have too low concentrations ***')
        if low_con_add > 0:
            print('*** However, you choose to add ' + str(low_con_add) + ' µl from each of these samples')
            print('---- See too_low.csv file for specifics ----')
            print(too_low)
        else:
            print('---- See too_low.csv file for specifics ----')
            print(too_low)

    # set values to zero for samples with too much liquid (i.e., won't fit into wells)
    plate_con['water_ul'] = np.where(np.logical_or(plate_con['water_ul'] > 100, plate_con['water_ul'] < 0,
                                                   plate_con['dna_ul'] > 100 ), plate_con['water_ul'] == 0,
                                                   plate_con['water_ul'])

    # set empty water values to 0
    plate_con['water_ul'] = plate_con['water_ul'].fillna(0)

    # this also sets dna_ul to 0 when dna_con < final_con
    plate_con['dna_ul'] = np.where(plate_con['water_ul'] <= 0, plate_con['dna_ul'] == 0, plate_con['dna_ul'])

    # however, when the low_con_add variable > 0, add dna for samples with too low concentrations and cross your fingers
    plate_con['dna_ul'] = np.where(plate_con['dna_con'] < final_con, low_con_add, plate_con['dna_ul'])

    # add base_name to output file names
    outPlateName = base_name + '_normalization.csv'
    outOveragesName = base_name + '_overages.csv'
    outTooLowName = base_name + '_too_low.csv'

    # write files to output directory
    if not os.path.isdir('output_files'):
        os.mkdir('output_files')

    plate_con.to_csv('output_files/' + outPlateName, index=False)
    overages.to_csv('output_files/' + outOveragesName, index=False)
    too_low.to_csv('output_files/' + outTooLowName, index=False)

    # manipulations necessary for robot protocol
    plate_con['new_col'] = plate_con['dna_well'].map(str) + "," + plate_con['norm_well'].map(str) + "," + \
                           plate_con['dna_ul'].map(str) + "," + plate_con['water_ul'].map(str)
    robot_vals = plate_con['new_col'].str.cat(sep="\\\\n")

    # open DM-normalization.py template and add values
    f = open("DM-normalization.py")
    filedata = f.read()
    f.close()

    newdata = filedata.replace('PASTE_DATA_HERE_MUST_END_WITH_QUOTATION_MARK', robot_vals)
    newdata = newdata.replace('Normalization from .csv', base_name + ' Normalization')
    newdata = newdata.replace('tip_type_variable', tip_type)


    f = open('output_files/' + base_name + '_normalization_protocol.py', 'w')
    f.write(newdata)
    f.close()

    # simulate OT-2 run
    from opentrons.simulate import simulate, format_runlog

    # protocol name
    if simulate_run == 'yes':
        protocol_name = 'output_files/' + base_name + '_normalization_protocol.py'
        # read the file
        protocol_file = open(protocol_name)
        # simulate() the protocol, keeping the runlog
        runlog, _bundle = simulate(protocol_file)
        # print the runlog
        print(format_runlog(runlog))
