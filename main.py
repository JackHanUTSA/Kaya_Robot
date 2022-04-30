
import communction
import configeration
import controller 
import locatization_model
import manual
import options
import parameters
import proctcal
import robot_model







try:
    print('Opening Serial')
    ser = serial.Serial('/dev/ttyUSB0',1000000,timeout=1)  # open serial port
    print(ser.name)         # check which port was really used
    #ser.write(b'hello')     # write a string
    ser.reset_input_buffer()

except:
    print('close Serial')
    ser.close()             # close port


reboot_motors()


try:
    print('Starting Server')
    server.start()
    print("Server is running")

    print('Starting ModbusTCP Client')
    client.open()
    print("ModbusTCP Client is running")

    #This is another thread that runs every t_sample Seconds
    def foo():
        #print(time.ctime())
        print('ISR')
        
        robot_position, target_position = get_global_coordinates()

        if enable_control == True:
            print('Position Control  enabled..')
            move_robot_target_real_xyt()

        if enable_trajectory_control == True:
            print('Trajectory Control  enabled..')
            move_robot_trajectory_real_xyt(T1_Pose)   

        threading.Timer(t_sample, foo).start()
    foo()



    torque_disable(ALL_MOTORS) 
    mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 


    DataBank.set_words(8,[proportional_gain])
    while True:

        # Read  Modbus_TCP  server commands/data
        DataBank.set_words(0,[int(uniform(0,100))]) #alive signal
        
        proportional_gain = DataBank.get_words(8)
        proportional_gain = proportional_gain[0]

        emergency_stop = DataBank.get_bits(1)  
        emergency_stop = emergency_stop[0] 
        enable_control = DataBank.get_bits(3)
        enable_control = enable_control[0]
        enable_trajectory_control = DataBank.get_bits(4)
        enable_trajectory_control = enable_trajectory_control[0]
        reset_robot = DataBank.get_bits(2)
        reset_robot = reset_robot[0]

        sleep(0.1)

        
        read_modbus_commands()

except:
    print('Shutdown server')
    server.stop()
    print('Shutdown client')
    client.close()
    print('close Serial')
    ser.close()             # close port


    ser.close()             # close port
        






kaya_volociatey_data
kaya_predicited_v

kaya_position_data
kaya_predicited_position