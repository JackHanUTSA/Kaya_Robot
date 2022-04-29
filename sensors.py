
# this module contain sensor data and reading function

def read_motor_angle(motor_ID):
    #print ('read_angle_command  [{}]'.format(','.join(hex(x) for x in torque_disable_command)))

    command = [0xFF, 0xFF,0x01,0x04,0x02,0x24,0x02]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent read_angle_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.reset_input_buffer()
    line = ''
    line = send_command(command)
    #print ('Response:', line)
    #print ('Response: [{}]'.format(','.join(hex(x) for x in line)))
    time.sleep(0.1)
    
    angle = 0
    
    if len(line) < 8:
        if (line[2] == motor_ID):
            angle = line[5]
            #print('valid response ')
            #print('motor_ID ', motor_ID, ' angle ', angle)            

    
    elif len(line) == 8:
        
        if (line[2] == motor_ID):
            angle = line[6]<<8 | line[5]
            if (line[6] & 0b10000000) != 0:  #its a negative angle in 2's complement
                angle = twos_comp(angle, 16)
            #print('valid response ')
            #print('motor_ID ', motor_ID, ' angle ', angle)
    time.sleep(0.1)
    
    return(angle)


def read_moving_command(motor_ID):
    #print ('read_moving_command  [{}]'.format(','.join(hex(x) for x in torque_disable_command)))

    command = [0xFF, 0xFF,0x01,0x04,0x02,0x2E,0x01]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent read_moving_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    line = send_command(command)
    #time.sleep(0.2) #NECESARIO!! porque tarda en responder el motor ala lectura


    done = 0
    if len(line) > 6:
       
        #print ('Response:', line)
        
        if (line[2] == motor_ID):
            done = line[6] 
            #print('valid response ')
            #if done == 1:
            #    print('motor_ID ', motor_ID, ' done movement ', done)

    #time.sleep(0.1)
    
    return(done)

def read_angles():
    print('/////////////////// read_angles:')
    w1=read_motor_angle(1)
    w2=read_motor_angle(2)
    w3=read_motor_angle(3)
    angles = [w1,w2,w3]
  
    #print(angles)
    position = r/3 * np.dot(kaya_dir_kine, angles)
    print(position)

    position[0] = round(position[0],2)
    position[1] = round(position[1],2)
    position[2] = round(position[2],2)

    return (angles,position)
#///////////////////////////////////////////////////////////////////////////////////
