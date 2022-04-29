
import numpy as np
from time import sleep
from random import uniform
import serial
# import/install the libmodbus on linux
import time
import math

# motor lower level congigure map

PKT_HEADER0 = 0
PKT_HEADER1 = 1
PKT_ID = 2
PKT_LENGTH = 3
PKT_INSTRUCTION = 4

#angle limits
MAX_ANGLE = 4095
MIN_ANGLE = 0
MAX_MULTI_ANGLE = 28672
MIN_MULTI_ANGLE = -28672
MAX_MOVE_SPEED = 1023
MIN_MOVE_SPEED = 0

ALL_MOTORS = 254

torque_enable_command_demo = [0xFF, 0xFF,0x01,0x04,0x03,0x18,0x01,0xDE]
move_2048_command_demo = [0xFF, 0xFF,0x01,0x05,0x03,0x1e,0x0,0x08,0xd0]
move_3122_command_demo = [0xFF, 0xFF,0x01,0x05,0x03,0x1e,0x32,0x0c,0x9a]
Ping_command_demo = [0xFF, 0xFF,0x01,0x02,0x02,0xFB]

# In the following commands, replace the 3rd byte with the correct ID
torque_enable_command = [0xFF, 0xFF,0x01,0x04,0x03,0x18,0x01]
torque_disable_command = [0xFF, 0xFF,0x01,0x04,0x03,0x18,0x00]
Ping_command = [0xFF, 0xFF,0x01,0x02,0x02]
move_single_turn_command = [0xFF, 0xFF,0x01,0x05,0x03,0x1e]
move_speed_command = [0xFF, 0xFF,0x01,0x05,0x03,0x20]
move_sync_speed_command = [0xFF, 0xFF,0x01,0x05,0x04,0X20]
Action_command = [0xFF, 0xFF,0xFE,0x02,0x05]
CW_Angle_limit_command = [0xFF, 0xFF,0x01,0x05,0x03,0x06]
CCW_Angle_limit_command = [0xFF, 0xFF,0x01,0x05,0x03,0x08]
resolution_divider_command = [0xFF, 0xFF,0x01,0x05,0x03,0x16]
read_angle_command = [0xFF, 0xFF,0x01,0x04,0x02,0x24,0x00]

# motor drivers: this driver contain all available command for motors 

# motors have 2 basic mode one is position mode the other is speed mode

def Checksum(data):
    CRC=0
    lenght = len(data)-3
    #print(lenght)


    string2 = []
    string2 = data[5:len(data)]
    #print ('string2  [{}]'.format(','.join(hex(x) for x in string2)))
    string_CRC= []
    string_CRC.append(data[2])
    string_CRC.append(lenght)
    string_CRC.append(data[4])
    #print ('string_CRC  [{}]'.format(','.join(hex(x) for x in string_CRC)))
    
    for i in range (len(string2)):
    
        string_CRC.append(string2[i])
        
    #print ('string_CRC  ',string_CRC)
    CRC = 0
    for i in range (len(string_CRC)):
            #print(string_CRC[i])
            CRC = CRC + int(string_CRC[i])
            
    CRC = ~(CRC)
    CRC = CRC & 0xFF
    #print(f"CRC ",CRC)
    #print(f"CRC 0x{CRC:X}")
    return(CRC)

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val  

def ping(motor_ID):
    #print ('Ping_command  [{}]'.format(','.join(hex(x) for x in Ping_command)))

    command = [0xFF, 0xFF,0x01,0x02,0x02]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent ping command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    send_command(command)
    
    return[1]

def reboot(motor_ID):
    print('re-boot motor_ID ',motor_ID)
    #print ('reboot_command  [{}]'.format(','.join(hex(x) for x in rebootcommand)))

    command = [0xFF, 0xFF,0x01,0x02,0x08]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent reboot_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    send_command(command)
    
    return[1]

def action(motor_ID):
    print ('Action_command')
    #print ('Action_command  [{}]'.format(','.join(hex(x) for x in Action_command)))

    #command = Action_command
    command = [0xFF, 0xFF,0xFE,0x02,0x05]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent Action_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    send_command(command)
    
    return[1]


def torque_enable(motor_ID):
    print ('torque_enable ')
    #print ('torque_enable_command  [{}]'.format(','.join(hex(x) for x in torque_enable_command)))

    command = [0xFF, 0xFF,0x01,0x04,0x03,0x18,0x01]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent torque_enable_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    send_command(command)
    
    return[1]

def torque_disable(motor_ID):
    #print ('torque_disable_command  [{}]'.format(','.join(hex(x) for x in torque_disable_command)))

    command = [0xFF, 0xFF,0x01,0x04,0x03,0x18,0x00]
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
     
    command.append(Checksum(command))
    #print ('sent torque_disable_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    send_command(command)
    
    return[1]



def Mode(motor_ID, mode):
    #print ('Mode_command')
    #command_CW = CW_Angle_limit_command  
    command_CW = [0xFF, 0xFF,0x01,0x05,0x03,0x06]
    #print ('original_command_CW [{}]'.format(','.join(hex(x) for x in command_CW)))
    command_CW[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
    #command_CCW = CCW_Angle_limit_command  
    command_CCW = [0xFF, 0xFF,0x01,0x05,0x03,0x08]
    #print ('original_command_CCW [{}]'.format(','.join(hex(x) for x in command_CCW)))
    command_CCW[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID

    if mode == 'Joint':
            
            command_CW.append(MIN_ANGLE & 0x00FF)
            command_CW.append((MIN_ANGLE & 0xFF00)>>8)
            command_CW.append(Checksum(command_CW))
            command_CCW.append(MAX_ANGLE & 0x00FF)
            command_CCW.append((MAX_ANGLE & 0xFF00)>>8)
            command_CCW.append(Checksum(command_CCW))

    elif mode == 'Wheel':
    
            command_CW.append(MIN_ANGLE & 0x00FF)
            command_CW.append((MIN_ANGLE & 0xFF00)>>8)
            command_CW.append(Checksum(command_CW))
            command_CCW.append(MIN_ANGLE & 0x00FF)
            command_CCW.append((MIN_ANGLE & 0xFF00)>>8)
            command_CCW.append(Checksum(command_CCW))

    elif mode == 'Multi-turn':
    
            command_CW.append(MAX_ANGLE & 0x00FF)
            command_CW.append((MAX_ANGLE & 0xFF00)>>8)
            command_CW.append(Checksum(command_CW))
            command_CCW.append(MAX_ANGLE & 0x00FF)
            command_CCW.append((MAX_ANGLE & 0xFF00)>>8)
            command_CCW.append(Checksum(command_CCW))

    print('Mode =',mode)

   # print ('command_CW : [{}]'.format(','.join(hex(x) for x in command_CW)))
    #ser.write(command_CW)
    #time.sleep(0.1)

    send_command(command_CW)
    

    #print ('command_CCW : [{}]'.format(','.join(hex(x) for x in command_CCW)))
    #ser.write(command_CCW)
    #time.sleep(0.1)

    send_command(command_CCW)
    
    return[1]


def send_command(command):
    count1 = 0
    while ser.out_waiting > 0:
        count1 += 1
        print('count1 ',count1)
    
    
    if ser.out_waiting == 0:    
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        ser.write(command)
        
    
    time.sleep(0.02) # time to react to a received comand
    
    response = []
    if command[PKT_ID] != ALL_MOTORS : #broadcast address does dont send repply
        count2 = 0
        while ser.in_waiting == 0:
            count2 += 1
            print('count2 ',count2)       
            
        if ser.in_waiting > 0:
            line = ser.readline()
             
            #print ('Response [{}]'.format(','.join(hex(ord(x)) for x in line)))
            #print(len(line))
            for i in range(len(line)):
                #response.append(ord(line[i]))
                response.append(line[i])          
            
                #print(hex(ord(line[i])))
        #time.sleep(0.1) 
        ser.reset_input_buffer()
        #time.sleep(0.1) 
        return(response)
    else:
   
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        #time.sleep(0.1) 
    return[1]
  
  
def move_single_turn (motor_ID, angle,speed_percentage):


    #mode = "Joint"
    #Mode(motor_ID, mode)

    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    set_speed(motor_ID,speed)



    #command = move_single_turn_command
    command = [0xFF, 0xFF,0x01,0x05,0x03,0x1e] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    #limit the maximum value
    if angle > MAX_ANGLE:
        angle = MAX_ANGLE
    if angle < MIN_ANGLE:
        angle = MIN_ANGLE       
        
    command.append(angle & 0x00FF)
    command.append((angle & 0xFF00)>>8)
    #print ('move_single_turn_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    print ('sent move_single_turn_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    return [1]


def move_multi_turn (motor_ID, angle,speed_percentage,timer):
#This function requires mode = Multi-turn

    torque_disable(motor_ID) 
    mode = "Multi-turn"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 

    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    set_speed(motor_ID,speed)


    #command = move_multi_turn_command
    command = [0xFF, 0xFF,0x01,0x05,0x03,0x1e] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    #limit the maximum value
    if angle > MAX_MULTI_ANGLE:
        angle = MAX_MULTI_ANGLE
    if angle < MIN_MULTI_ANGLE:
        angle = MIN_MULTI_ANGLE       
        
    command.append(angle & 0x00FF)
    command.append((angle & 0xFF00)>>8)
 
    #print ('move_multi_turn_command  [{}]'.format(','.join(hex(x) for x in command)))
    print ('Motor ', motor_ID, ' SP angle ', angle)
        
    command.append(Checksum(command))
    #print ('sent move_multi_turn_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    
    
    if timer == 0:
        return[1]
    elif timer == -1:
        #with timer = 0, it waits for the movement to finish
            angle_reached = False
            while angle_reached == False:
        
                m1_done = read_moving_command(motor_ID)

                if (m1_done):
                    print("angle_reached = ", angle_reached)
                    angle_reached = True
                    
    else:
        time.sleep(timer)  #Super important!!!
        
    return [1]    


def move_multi_turn2 (motor_ID, angle,speed_percentage,sync): 
    #Does not receive explicit direction. The sign of angle set the direction
    # This function requires Mode = Multi-turn

    #mode = "Multi-turn"
    #Mode(motor_ID, mode)

    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    set_speed(motor_ID,speed)
    
    
    print ('Motor ', motor_ID, ' SP angle ', angle)
    '''
    #limit the maximum value
    #limit the maximum value
    if angle > MAX_MULTI_ANGLE:
        angle = MAX_MULTI_ANGLE
    if angle < MIN_MULTI_ANGLE:
        angle = MIN_MULTI_ANGLE  
    print ('angle limited', angle)
    '''

    if angle >= 0:
            angle = angle & 0x03FF  # turn off bit 10
            #angle = 76
    else:
            angle = abs(angle) | 0x0400  #turn on bit 10
            #angle = 1100

    #print ('angle with  direction', angle)

    if sync == True:
        #command = move_sync_angle_command
        command = [0xFF, 0xFF,0x01,0x05,0x04,0x1E] 
    else:    
        #command = move_angle_command
        command = [0xFF, 0xFF,0x01,0x05,0x03,0x1E] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
        
    command.append(angle & 0x00FF)
    command.append((angle & 0xFF00)>>8)
    #print ('move_angle_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_angle_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    
    
    if timer == 0:
        return[1]
    elif timer == -1:
    #with timer = 0, it waits for the movement to finish
        angle_reached = False
        while angle_reached == False:
    
            m1_done = read_moving_command(motor_ID)

            if (m1_done):
                print("angle_reached = ", angle_reached)
                angle_reached = True
                
    else:
        time.sleep(timer)  #Super important!!!
        
    return [1]    


def move_multi_turn_sync (motor_ID, angle,speed_percentage,timer,sync): 
    #Does not receive explicit direction. The sign of angle set the direction
    # This function requires Mode = Multi-turn
    
    #print('move_multi_turn_sync  motor_ID =', motor_ID, 'angle: ', angle)
    
    '''
    torque_disable(motor_ID) 
    mode = "Multi-turn"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 
    
    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    set_speed(motor_ID,speed)
    '''
    
   
    #limit the maximum value
    if angle > MAX_MULTI_ANGLE:
        angle = MAX_MULTI_ANGLE
    if angle < MIN_MULTI_ANGLE:
        angle = MIN_MULTI_ANGLE  
    #print ('angle limited', angle)
    #print ('Motor ', motor_ID, ' SP angle ', angle)

  

    if sync == True:
        #command = move_sync_angle_command
        command = [0xFF, 0xFF,0x01,0x05,0x04,0x1E] 
    else:    
        #command = move_angle_command
        command = [0xFF, 0xFF,0x01,0x05,0x03,0x1E] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
        
    command.append(angle & 0x00FF)
    command.append((angle & 0xFF00)>>8)
    #print ('move_angle_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_angle_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)    #exits either by timer of wait for the movement to finish
    
    
    if timer == 0:
        return[1]
    elif timer == -1:
        #with timer = 0, it waits for the movement to finish
            angle_reached = False
            while angle_reached == False:
        
                m1_done = read_moving_command(motor_ID)

                if (m1_done):
                    print("angle_reached = ", angle_reached)
                    angle_reached = True
                    
    else:
        time.sleep(timer)  #Super important!!!
        
        
        
    return [1]    

def center_motor(motor_ID):
    
    print('///////////////////// Center_motor: motor_ID =', motor_ID)
    
    torque_disable(motor_ID) 
    mode = "Joint"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 

    move_single_turn (motor_ID, 2048,5)
    time.sleep(2) #importante para no traslpar movimientos
    return [1]

def reboot_motors():
    for motor_ID in range(1,4):
            
        reboot(motor_ID)
        time.sleep(0.1)
    return[1]
     
def init_motors_Multi_turn():
    print('////////////////////// init_motors_Multi_turn: ')
    

    
    mode = "Multi-turn"    
    speed_percentage = 10    
    pos_ini = 0
    time_out = 3
    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    
    for motor_ID in range(1,4):
        
    #motor_ID = ALL_MOTORS           
        torque_disable(motor_ID) 
        Mode(motor_ID, mode)
        torque_enable(motor_ID) 
        set_speed(motor_ID,speed)

        move_multi_turn_sync (motor_ID, pos_ini,speed_percentage,time_out,True)
        #time.sleep(2)
    action(ALL_MOTORS)    
    time.sleep(0.1) #importante para no traslpar movimientos

   
def init_motors_Multi_turn2():
    print('////////////////////// init_motors_Multi_turn: ')
    

    
    mode = "Multi-turn"    
    speed_percentage = 10    
    pos_ini = 0
    time_out = 3
    speed = math.trunc(speed_percentage/100.0*MAX_MOVE_SPEED)
    #print 'speed_percentage', speed_percentage
    
    #for motor_ID in range(1,4):
        
    motor_ID = ALL_MOTORS           
    torque_disable(motor_ID) 
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 
    set_speed(motor_ID,speed)

    move_multi_turn_sync (motor_ID, pos_ini,speed_percentage,time_out,True)
    #time.sleep(2)
    action(ALL_MOTORS)    
    time.sleep(0.1) #importante para no traslpar movimientos

    


def move_motor_angles(motor_ID, angles, speed_percentage):
    #Mode  = "Joint" MUST be configured before using this function

    for angle in angles:
        #ping(motor_ID)
        move_single_turn (motor_ID, angle,speed_percentage)
        #time.sleep(2) 
 
    return [1]

def move_motor_multi_turn_angles(motor_ID,angles, speed_percentage,timer):
        #Mode  = "Multi-turn" MUST be configured before using this function

    for angle in angles:
        #ping(motor_ID)
        move_multi_turn (motor_ID, angle,speed_percentage,timer)

    return [1]
    
    
    
    


def set_speed (motor_ID, speed):
    
    #print('////////////// set speed')
    print ('motor_ID ', motor_ID,' speed', speed)
    #command = move_speed_command
    command = [0xFF, 0xFF,0x01,0x05,0x03,0x20] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    #limit the maximum value
    if speed > MAX_MOVE_SPEED:
        speed = MAX_MOVE_SPEED
    if speed < MIN_MOVE_SPEED:
        speed = MIN_MOVE_SPEED       
        
    command.append(speed & 0x00FF)
    command.append((speed & 0xFF00)>>8)
    #print ('move_speed_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_speed_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    
    return [1]    


def stop_speed (motor_ID):

    print ('stop_speed')
    #command = stop_speed_command
    command = [0xFF, 0xFF,0x01,0x05,0x03,0x20] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
    speed = 0    
    command.append(speed & 0x00FF)
    command.append((speed & 0xFF00)>>8)
    #print ('stop_speed_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_motor_speed_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    return [1]    

  
def move_motor_speed (motor_ID, speed,direction,sync,timer):

    #mode = "Wheel"
    #Mode(motor_ID, mode)

    print ('speed ', speed)
    '''
        #limit the maximum value
    if speed > MAX_MOVE_SPEED:
        speed = MAX_MOVE_SPEED
    if speed < MIN_MOVE_SPEED:
        speed = MIN_MOVE_SPEED   
    print ('speed limited', speed)
    '''

    if direction =='CCW':
            speed = speed & 0x03FF  # turn off bit 10
            #speed = 76
    if direction =='CW':
            speed = speed | 0x0400  #turn on bit 10
            #speed = 1100

    print ('speed in correct direction', speed)

    if sync == True:
        #command = move_sync_speed_command
        command = [0xFF, 0xFF,0x01,0x05,0x04,0x20] 
    else:    
        #command = move_motor_speed_command
        command = [0xFF, 0xFF,0x01,0x05,0x03,0x20] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
        
    command.append(speed & 0x00FF)
    command.append((speed & 0xFF00)>>8)
    #print ('move_motor_speed_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_motor_speed_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)


    
    send_command(command)
        
        
    # requested timer for movement
    # timer = 0 do not stop the motor
    if timer != 0:
        time.sleep(timer)     
        stop_speed (motor_ID)  
        
        
    return [1]    


def move_motor_speed2 (motor_ID, speed,sync,timer_speed2): 
        #Does not receive explicit direction. The sign of speed set the direction
    # this function rely on the sign of numbers to 

    #mode = "Wheel"
    #Mode(motor_ID, mode)

    print ('motor: ', motor_ID, ' speed ', speed)
    '''
        #limit the maximum value
    if speed > MAX_MOVE_SPEED:
        speed = MAX_MOVE_SPEED
    if speed < MIN_MOVE_SPEED:
        speed = MIN_MOVE_SPEED   
    print ('speed limited', speed)
    '''

    if speed >= 0:
            speed = speed & 0x03FF  # turn off bit 10
            #speed = 76
    else:
            speed = abs(speed) | 0x0400  #turn on bit 10
            #speed = 1100

    #print ('speed in correct direction', speed)

    if sync == True:
        #command = move_sync_speed_command
        command = [0xFF, 0xFF,0x01,0x05,0x04,0x20] 
    else:    
        #command = move_motor_speed_command
        command = [0xFF, 0xFF,0x01,0x05,0x03,0x20] 
    #print ('original_command  [{}]'.format(','.join(hex(x) for x in command)))
    command[PKT_ID] = motor_ID # replace the 3rd byte with the correct motor_ID
    
        
    command.append(speed & 0x00FF)
    command.append((speed & 0xFF00)>>8)
    #print ('move_motor_speed_command  [{}]'.format(','.join(hex(x) for x in command)))
    
        
    command.append(Checksum(command))
    #print ('sent move_motor_speed_command : [{}]'.format(','.join(hex(x) for x in command)))
    #ser.write(command)
    #time.sleep(0.1)

    send_command(command)
    
        # requested timer for movement
    # timer = 0 do not stop the motor
    if timer_speed2 != 0.0:
        time.sleep(timer_speed2)     
        #stop_speed (motor_ID)  
        
    return [1]    
