from opentrons import robot, containers, instruments

##This protocol automates the washing step for DxSAQ.
##It is only capable of handling 96 wells per run,
##because it needs 3 full tip boxes to do so.

##Note do not have pipette tip loaded before starting this protocol!!

##Initialize containers and locations
buffers = containers.load('trough-12row','B1') ##Buffer 1 in A1 position, Buffer 2 in A2 position, Buffer 3 in A3 position
samples = containers.load('96-flat','C1')
trash = containers.load('point', 'E1')
tip_rack1 = containers.load('tiprack-1000ul', 'B2')
tip_rack2 = containers.load('tiprack-1000ul', 'C2')
tip_rack3 = containers.load('tiprack-1000ul', 'D2')
tip_rack4 = containers.load('tiprack-1000ul', 'E2')
waste = containers.load('point', 'D1')

##Initialize pipette with all necessary specifications
p1000 = instruments.Pipette(axis='a', max_volume=1000, tip_racks=[tip_rack1, tip_rack2, tip_rack3, tip_rack4],trash_container=trash) #THIS IS WHERE YOU ASSIGN WHICH PIPETTE (AXIS) TO USE (ALWAYS A for us)

##Wash settings:
wash_vol = 250
wash1 = 3 #number of washes for buffer 1
wash2 = 2 #number of washes for buffer 2
wash3 = 3 #number of washes for buffer 3


##Begin protocol for one 96 well plate
count1 = 1
count2 = 1
count3 = 1
for i in range(96):
    while count1 < wash1 + 2:
        if count1 == 1:
            p1000.pick_up_tip()
            count1 +=1
        else:
            p1000.transfer(wash_vol,buffers.well('A1'),samples.wells(i),new_tip='never')
            p1000.transfer(wash_vol+10,samples.wells(i),waste,new_tip='never')
            p1000.blow_out(waste)
            count1 +=1
    p1000.drop_tip()
    count1 = 1
    while count2 < wash2 + 2:
        if count2 == 1:
            p1000.pick_up_tip()
            count2 +=1
        else:
            p1000.transfer(wash_vol,buffers.well('A2'),samples.wells(i),new_tip='never')
            p1000.transfer(wash_vol+10,samples.wells(i),waste,new_tip='never')
            p1000.blow_out(waste)
            count2 +=1
    p1000.drop_tip()
    count2 = 1
    while count3 < wash3 + 2:
        if count3 == 1:
            p1000.pick_up_tip()
            count3 +=1
        else:
            p1000.transfer(wash_vol,buffers.well('A3'),samples.wells(i),new_tip='never')
            p1000.transfer(wash_vol+10,samples.wells(i),waste,new_tip='never')
            p1000.blow_out(waste)
            count3 +=1
    p1000.drop_tip()
    count3 = 1







robot.home()




#p200.transfer(amount, big_tubes.wells('A4'), dilutions.wells())

##different dilution for each well
#for i in range(96):
#    p200.transfer(50*(User.dilution_matrix[i]-1), samples.wells(i), dilutions.wells(i), new_tip='always')
#
##different dilution for each row
#for i in range(12):
#    p200.transfer(50, samples.rows(i), dilutions.rows(i))
#
# This part of the protocol adds the dilutions to the requested wells
#
#    print(c)
#robot.simulate()
