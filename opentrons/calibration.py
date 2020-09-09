from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Calibration test',
    'author': 'David Dooley <ddooley2@vols.utk.edu>',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.6'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    trough = protocol.load_labware('nest_12_reservoir_15ml', '2')
    tiprack_200 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')
    tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '6')

    # pipettes
    right_pipette = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_200])
    left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20])

    # commands
#    right_pipette.pick_up_tip()
#    right_pipette.drop_tip()

    left_pipette.pick_up_tip()
    left_pipette.aspirate(10, trough['A1'])
    left_pipette.dispense(10, trough['A2'])
    left_pipette.drop_tip()
