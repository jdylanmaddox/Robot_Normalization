import math


def get_values(*names):
    import json
    _all_values = json.loads("""{"input_csv":"source plate well,destination plate well,volume sample (µl),volume diluent (µl),\\nPASTE_DATA_HERE_MUST_END_WITH_QUOTATION_MARK","p20_type":"p20_single_gen2","p20_mount":"right","p300_type":"p300_single_gen2","p300_mount":"left","source_type":"nest_96_wellplate_100ul_pcr_full_skirt","dest_type":"nest_96_wellplate_100ul_pcr_full_skirt","reservoir_type":"opentrons_6_tuberack_nest_50ml_conical"}""")
    return [_all_values[n] for n in names]


# metadata
metadata = {
    'protocolName': 'Normalization from .csv',
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
    water = ctx.load_labware(reservoir_type, '6')

    tip_type = 'tip_type_variable'

    if tip_type == 'not_filtered':
        tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
                    for slot in ['11','5']]
        tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
                    for slot in ['10']]
        p20 = ctx.load_instrument(p20_type, p20_mount, tip_racks=tiprack20)
        p300 = ctx.load_instrument(p300_type, p300_mount, tip_racks=tiprack300)

    elif tip_type == 'filtered':
        tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot, '20ul filtered tiprack')
                     for slot in ['11', '5']]
        tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot, '200ul filtered tiprack')
                      for slot in ['10']]
        p20 = ctx.load_instrument(p20_type, p20_mount, tip_racks=tiprack20)
        p300 = ctx.load_instrument(p300_type, p300_mount, tip_racks=tiprack300)

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]]

    # calculating water height in 5 mL tube
    # add calculated water volume from create_normalization_protocol.py
    # must calculate height above 5 mL and add 17 mm because the tube has a v-bottom
    reservoir_water_vol = ADD_CALCULATED_WATER_VOLUME
    int_vol = reservoir_water_vol
    starting_ht = (int_vol - 5000) / (math.pi * (13.25 ** 2))
    tip_ht = 17 + round(starting_ht, 2) - 10
    print('Starting tip height (mm) = ' + str(round(tip_ht, 2)))

    # insure user has added the correct amount of water to 50 mL tube
    ctx.pause('Did you add ' + str(int_vol) + ' µl of water to the 50 mL tube? It needs to be fairly accurate. The pipette tip will start at ' + str(round(tip_ht, 2)) + ' mm from the bottom of the tube. For reference 5 mL is 17 mm from the bottom. *** DO NOT simply fill the tube to 50 mL as the pipette mechanism will get wet and possibly break. *** ')

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
        pip.transfer(vol_w, water['A1'].bottom(tip_ht), d.bottom(2), new_tip='never')
        pip.flow_rate.blow_out = 100  # change blow_out rate
        pip.blow_out(d.top(-2))

        # track water height in 50 mL tube
        used_ht = vol_w / (math.pi * (13.25 ** 2))
        tip_ht += used_ht
        if tip_ht < 15:
            tip_ht = 10

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
            pip.flow_rate.blow_out = 50  # change blow_out rate
            pip.blow_out(d.top(-2))
            pip.drop_tip()
