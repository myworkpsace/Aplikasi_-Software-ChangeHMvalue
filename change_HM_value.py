import serial
import time
from tkinter import *
import array as arr

def quit():
        global tkTop
        tkTop.destroy()

def read_all(port, chunk_size=200):
        #"""
        #    Read all characters on the serial port and return them.
        #"""
        #if not port.timeout:
        #    raise TypeError('Port needs to have a timeout set!')

        read_buffer = b''

        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout. Increase chunk_size to fail quicker
            byte_chunk = port.read(size=chunk_size)
            read_buffer += byte_chunk
            if not len(byte_chunk) == chunk_size:
                break

        return read_buffer


def chekcsum_calc(arr_bytes):
        temp_value = 0
        for i in range(len(arr_bytes)):
            temp_value = temp_value + arr_bytes[i]
        
        checksum_value = 0xFF - (temp_value & 0xFF)
        return checksum_value

def set_button1_state():
        varLabel.set("SENDING_DATA")
        #ser.write(bytes('H', 'UTF-8'))
            
        input_mac = textbox_mac_addrs.get("1.0",'end-1c')
        input_new_hm = textbox_new_hm_value.get("1.0",'end-1c')            

        print(input_mac)
        
        
        list_header = [0x00, 0x01, 0x15, 0x07, 0x50]
        list_tail = [0x0D, 0x0A]
        list_value_mac = []
        list_value_mac.extend(list_header)
        next_capture = 1
        for i in range(17):
            if i == next_capture:
                next_capture = next_capture + 3
                val_str_temp = input_mac[i - 1] + input_mac[i]
                val_int_temp = int(val_str_temp, 16)
                list_value_mac.append(val_int_temp)
         
        print(list_value_mac)
         
        #for i in len(list_value_mac):
        #    temp_value = temp_value + list_value_mac[i]
        #checksum_value = 0xFF - (temp_value & 0xFF)
        
        checksum_value = chekcsum_calc(list_value_mac)
        list_value_mac.append(checksum_value)
        list_value_mac.extend(list_tail)
        
        print(list_value_mac)
        arr_data_ser = arr.array('B', list_value_mac)
        ser.write(arr_data_ser)
        
        time.sleep(1)
        
        buffer_data = read_all(ser)
        print(buffer_data)
        
        if(len(buffer_data) > 0):
            list_header_hm_value = [0x00, 0x01, 0x15, 0x02, 0x51]
            number_real = float(input_new_hm) 
            
            print(number_real)
            number_to_send  = int(number_real * 10)      
            
            list_number = [0, 0, 0, 0]
            
            list_number[0] = (number_to_send >> 24) & 0xFF;
            list_number[1] = (number_to_send >> 16) & 0xFF;
            list_number[2] = (number_to_send >> 8) & 0xFF;
            list_number[3] =  number_to_send & 0xFF;
            
            print(list_number)
            
            list_new_hm_value = []
            list_new_hm_value.extend(list_header_hm_value)
            list_new_hm_value.extend(list_number)
            
            checksum_value2 = chekcsum_calc(list_new_hm_value)
            list_new_hm_value.append(checksum_value2)
            list_new_hm_value.extend(list_tail)
            
            print(list_new_hm_value)
            arr_data_ser2 = arr.array('B', list_new_hm_value)
            ser.write(arr_data_ser2)            
            

def connect_serial():
        global ser 
        input_com = textbox_comport.get("1.0",'end-1c')  
        print(input_com)    
        ser = serial.Serial(input_com, 115200, timeout=2.0)
        print("Connecting port")
        time.sleep(1)
        varLabel.set("connected")

tkTop = Tk()
tkTop.geometry('300x400')
tkTop.title("HM change value")
label3 = Label(text = 'Change HM Value',font=("Courier", 12,'bold')).pack()
tkTop.counter = 0
b = tkTop.counter

varLabel = IntVar()
tkLabel = Label(tkTop, 
    textvariable=varLabel,
)
varLabel.set("disconnected")
tkLabel.pack()


tkLabel00 = Label(tkTop, 
    text = "Inser Com Port"
)
tkLabel00.pack()

textbox_comport = Text(tkTop,
    height = 1,
    width = 15,
)
textbox_comport.pack(side='top', ipadx=5, padx=5, pady=5)

tkLabel01 = Label(tkTop, 
    text = "Inser MAC address device"
)
tkLabel01.pack()

textbox_mac_addrs = Text(tkTop,
    height = 1,
    width = 15,
)
textbox_mac_addrs.pack(side='top', ipadx=5, padx=5, pady=5)

tkLabel02 = Label(tkTop, 
    text = "Inser NEW HM vaue"
)
tkLabel02.pack()

textbox_new_hm_value = Text(tkTop,
    height = 1,
    width = 15,
)
textbox_new_hm_value.pack(side='top', ipadx=5, padx=5, pady=5)

btn_conn_state = Button(
    tkTop,
    text="CONNECT",
    command=connect_serial,
    height = 2,
    fg = "black",
    width = 15,
    bd = 5,
    activebackground='green'
)
btn_conn_state.pack(side='top', ipadx=5, padx=5, pady=5)

button1state = Button(
    tkTop,
    text="SEND HM VALUE",
    command=set_button1_state,
    height = 2,
    fg = "black",
    width = 15,
    bd = 5,
    activebackground='green'
)
button1state.pack(side='top', ipadx=5, padx=5, pady=5)

tkButtonQuit = Button(
    tkTop,
    text="Quit",
    command=quit,
    height = 2,
    fg = "black",
    width = 15,
    bg = 'yellow',
    bd = 5
)
tkButtonQuit.pack(side='top', ipadx=5, padx=5, pady=5)


mainloop()