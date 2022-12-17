def get_values(*names):
    import json
    _all_values = json.loads("""{"input_csv":"source plate well,destination plate well,volume sample (µl),volume diluent (µl)A1,A1,0.0,0.0\\nB1,B1,3.09,6.91\\nC1,C1,2.0,34.28\\nD1,D1,3.4,6.6\\nE1,E1,2.0,18.25\\nF1,F1,2.0,17.94\\nG1,G1,2.0,16.97\\nH1,H1,3.63,6.37\\nA2,A2,2.0,16.44\\nB2,B2,2.0,16.99\\nC2,C2,2.0,23.98\\nD2,D2,3.04,6.96\\nE2,E2,2.0,11.08\\nF2,F2,2.0,19.01\\nG2,G2,2.0,11.88\\nH2,H2,2.0,23.24\\nA3,A3,2.0,65.26\\nB3,B3,2.41,7.59\\nC3,C3,2.0,19.59\\nD3,D3,2.0,19.57\\nE3,E3,2.0,29.18\\nF3,F3,2.0,19.0\\nG3,G3,2.0,25.74\\nH3,H3,2.0,13.06\\nA4,A4,2.0,29.46\\nB4,B4,2.0,11.42\\nC4,C4,2.0,19.44\\nD4,D4,2.0,15.97\\nE4,E4,2.0,28.5\\nF4,F4,2.0,14.49\\nG4,G4,2.0,20.18\\nH4,H4,2.0,17.32\\nA5,A5,2.0,11.91\\nB5,B5,2.15,7.85\\nC5,C5,2.0,9.19\\nD5,D5,2.0,14.12\\nE5,E5,2.0,15.29\\nF5,F5,2.0,16.43\\nG5,G5,2.0,31.7\\nH5,H5,2.0,38.9\\nA6,A6,2.0,32.39\\nB6,B6,2.0,18.89\\nC6,C6,2.53,7.47\\nD6,D6,2.0,24.38\\nE6,E6,2.0,26.11\\nF6,F6,2.0,19.53\\nG6,G6,2.0,23.72\\nH6,H6,2.0,36.26\\nA7,A7,2.0,31.96\\nB7,B7,2.0,52.34\\nC7,C7,2.0,43.51\\nD7,D7,2.0,40.3\\nE7,E7,2.0,16.84\\nF7,F7,2.0,25.31\\nG7,G7,2.0,41.75\\nH7,H7,2.0,16.36\\nA8,A8,2.0,18.33\\nB8,B8,5.01,4.99\\nC8,C8,2.38,7.62\\nD8,D8,2.0,14.4\\nE8,E8,2.5,7.5\\nF8,F8,2.0,12.18\\nG8,G8,2.0,21.06\\nH8,H8,2.0,8.95\\nA9,A9,2.0,19.4\\nB9,B9,2.0,8.1\\nC9,C9,2.0,13.09\\nD9,D9,2.0,31.79\\nE9,E9,2.0,15.77\\nF9,F9,2.0,20.28\\nG9,G9,2.0,22.81\\nH9,H9,2.0,54.98\\nA10,A10,2.0,10.12\\nB10,B10,2.0,8.4\\nC10,C10,2.0,34.67\\nD10,D10,2.0,16.5\\nE10,E10,3.11,6.89\\nF10,F10,2.99,7.01\\nG10,G10,2.0,8.49\\nH10,H10,2.0,12.36\\nA11,A11,2.0,15.07\\nB11,B11,5.23,4.77\\nC11,C11,2.0,10.4\\nD11,D11,2.0,17.7\\nE11,E11,2.0,10.16\\nF11,F11,2.0,22.84\\nG11,G11,2.0,23.94\\nH11,H11,4.44,5.56\\nA12,A12,2.0,14.7\\nB12,B12,7.3,2.7\\nC12,C12,2.0,50.96\\nD12,D12,2.0,31.87\\nE12,E12,3.69,6.31\\nF12,F12,2.0,8.3\\nG12,G12,2.0,52.58\\nH12,H12,2.0,22.71","p20_type":"p20_single_gen2","p20_mount":"right","p300_type":"p300_single_gen2","p300_mount":"left","source_type":"nest_96_wellplate_100ul_pcr_full_skirt","dest_type":"nest_96_wellplate_100ul_pcr_full_skirt","reservoir_type":"nest_12_reservoir_15ml"}""")
    return [_all_values[n] for n in names]


# metadata
metadata = {
    'protocolName': 'DM.2022.12.17 Normalization',
    'author': 'Modified from Opentrons by Dylan Maddox',
    'source': 'Opentrons',
    'apiLevel': '2.11'
}


def run(ctx):

    [input_csv, p20_type, p20_mount, p300_type, p300_mount, source_type,
        dest_type, reservoir_type] = get_values(  # noqa: F821
        'input_csv', 'p20_type', 'p20_mount', 'p300_type', 'p300_mount',
        'source_type', 'dest_type', 'reservoir_type')

    # labware
    source_plate = ctx.load_labware(source_type, '8', 'source plate')
    destination_plate = ctx.load_labware(dest_type, '9', 'destination plate')
    water = ctx.load_labware(
        reservoir_type, '6',
        'reservoir for water (position A1)').wells()[0].bottom(1)
    tiprack20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
        for slot in ['11','5']
    ]
    tiprack300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
        for slot in ['10']
    ]

    # pipettes
    p20 = ctx.load_instrument(p20_type, p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument(p300_type, p300_mount, tip_racks=tiprack300)

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]]

    # perform normalization
    for line in data:
        s, d, vol_s, vol_w = line[:4]

        if not vol_w:
            vol_w = 0
        else:
            vol_w = float(vol_w)

        d = destination_plate.wells_by_name()[d]

        # pre-transfer diluent
        pip = p300 if vol_w > 20 else p20
        if not pip.has_tip:
            pip.pick_up_tip()

        pip.transfer(vol_w, water, d.bottom(2), new_tip='never')
        pip.blow_out(d.top(-2))

    for pip in [p20, p300]:
        if pip.has_tip:
            pip.drop_tip()

    # perform normalization
    for line in data:
        s, d, vol_s, vol_w = line[:4]
        if not vol_s:
            vol_s = 0
        else:
            vol_s = float(vol_s)

        s = source_plate.wells_by_name()[s]
        d = destination_plate.wells_by_name()[d]

        # transfer sample
        pip = p300 if vol_s > 20 else p20
        if vol_s != 0:
            pip.pick_up_tip()
            pip.transfer(vol_s, s, d, new_tip='never')
            pip.blow_out(d.top(-2))
            pip.drop_tip()
