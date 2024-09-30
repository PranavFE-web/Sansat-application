import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import serial
import time

def readSensorOptions(filePath):
    try:
        df = pd.read_excel(filePath)
        return df['Sensor Name'].unique().tolist()
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading {filePath}: {e}")
        return []

def readSensorCommands(filePath):
    try:
        df = pd.read_excel(filePath)
        numColumns = len(df.columns)
        dColumns = [f'D{i}' for i in range(1, numColumns-4)]
        df['Command Display'] = df['ID'].astype(str) + " - " + df['NAME']
        columns = ['Command Display', 'ID', 'LENGTH'] + dColumns
        commands = df[columns]
        return commands
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading {filePath}: {e}")
        return pd.DataFrame()

def readSensorType(filePath):
    try:
        df = pd.read_excel(filePath)
        return df['SensorType'].tolist()
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading {filePath}: {e}")

def onButtonClick():
    if not powerVar.get():
        messagebox.showerror("Error", "Power is OFF")
        return
    
    selectedSensor = sensorVar.get()
    selectedCommand = commandVar.get()
    selectedSensorType = sensorTVar.get()

    selectedCommand = commandVar.get()
    commandData = commandsDict.get(selectedCommand, {})
    idValue = commandData.get('ID', '')
    
    if not selectedSensor:
        messagebox.showerror("Input Error", "Please select a sensor.")
        return
    if not selectedCommand:
        messagebox.showerror("Input Error", "Please select a command.")
        return
    
    commandData = commandsDict.get(selectedCommand, {})
    lengthCode = commandData.get('LENGTH', 0)
    idValue = commandData.get('ID', '')
    dColumns = [commandData.get(f'D{i}', '') for i in range(1, 100)]
    
    try:
        bufferEntry = [int(float(idValue))]
    except ValueError:
        messagebox.showerror("Input Error", "Invalid ID value.")
        return
    
    if isEditing:
        insertedValue = insertVar.get().strip()
        userData = insertedValue.split()
        userData = [int(float(value)) for value in userData if value and not pd.isna(float(value))]
        bufferEntry += userData


    elif selectedSensorType == "telecommand" and selectedSensor=="WHEEL1" and idValue==2 or idValue==3:
        wheel_speed_data = WspeedEntry.get().strip()
        duty_cycle_data = duty_cycle_entry.get().strip()

        if wheel_speed_data:  
            wheelspeedvalue = wheel_speed_data
            bufferEntry.append(wheelspeedvalue)
           

        elif duty_cycle_data:  
            dutycyclevalue = duty_cycle_data
            bufferEntry.append (dutycyclevalue)
        else:
            dColumnsFiltered = [int(float(value)) for value in dColumns[:lengthCode] if value and not pd.isna(float(value))]
            bufferEntry += dColumnsFiltered
    
    else:
        dColumnsFiltered = [int(float(value)) for value in dColumns[:lengthCode] if value and not pd.isna(float(value))]
        bufferEntry += dColumnsFiltered
    
    prefix = [0x1F, 0x7F]
    suffix = [0x1F, 0xFF]
    bufferEntry = prefix + bufferEntry + suffix
    bufferEntry = [int(value) for value in bufferEntry]
    for i, entry in enumerate(sendBuffer):
        if entry[2] == bufferEntry[2]:
            sendBuffer[i] = bufferEntry
            break
    else:
        sendBuffer.append(bufferEntry)
    
    print('Send Buffer:', sendBuffer)

def resetAll():
    sensorVar.set('')
    commandVar.set('')
    sensorTVar.set('')
    insertVar.set('')
    sendBuffer.clear()
    commandMenu['values'] = []
    print('Send Buffer reset:', sendBuffer)

def toggleInputs():
    state = tk.NORMAL if powerVar.get() else tk.DISABLED
    sensorMenu.config(state=state)
    commandMenu.config(state=state)
    sensorTMenu.config(state=state)
    ActuatorselectionMenu.config(state=state)
    submitButton.config(state=state)
    editButton.config(state=state)
    sendButton.config(state=state) 

def updateCommands(event):
    sensor = sensorVar.get()
    sensorType = sensorTVar.get()
    
    
    if sensor == "WHEEL1" and sensorType == "telecommand":
        filePath = "Wheel_telecommand.xlsx"
    elif sensor == "WHEEL1" and sensorType == "telementry":
        filePath = "Wheel_telemetries.xlsx"
    elif sensor == "WHEEL1" and sensorType == "telecommand":
        filePath = "Wheel_telecommand.xlsx"
    elif sensor == "WHEEL1" and sensorType == "telementry":
        filePath = "Wheel_telemetries.xlsx"
    elif sensor == "WHEEL3" and sensorType == "telecommand":
        filePath = "Wheel_telecommand.xlsx"
    elif sensor == "WHEEL3" and sensorType == "telementry":
        filePath = "Wheel_telemetries.xlsx"
    elif sensor == "WHEEL4" and sensorType == "telecommand":
        filePath = "Wheel_telecommand.xlsx"
    elif sensor == "WHEEL4" and sensorType == "telementry":
        filePath = "Wheel_telemetries.xlsx"
    elif sensor == "SUN1" and sensorType == "telecommand":
        filePath = "Sun_telecommands.xlsx"
    elif sensor == "SUN1" and sensorType == "telementry":
        filePath = "Sun_telemetries.xlsx"
    elif sensor == "SUN2" and sensorType == "telecommand":
        filePath = "Sun_telecommands.xlsx"
    elif sensor == "SUN2" and sensorType == "telementry":
        filePath = "Sun_telemetries.xlsx"
    elif sensor == "SUN3" and sensorType == "telecommand":
        filePath = "Sun_telecommands.xlsx"
    elif sensor == "SUN3" and sensorType == "telementry":
        filePath = "Sun_telemetries.xlsx"
    elif sensor == "STAR" and sensorType == "telecommand":
        filePath = "Star_telecommands.xlsx"
    elif sensor == "STAR" and sensorType == "telementry":
        filePath = "Star_telementry.xlsx"
    elif sensor == "MAG1" and sensorType == "telecommand":
        filePath = "MAG_telecommand.xlsx"
    elif sensor == "MAG2" and sensorType == "telecommand":
        filePath = "MAG_telecommand.xlsx"
    elif sensor == "MAG3" and sensorType == "telecommand":
        filePath = "MAG_telecommand.xlsx"
    elif sensor == "MAG1" and sensorType == "telementry":
        filePath = "MAG_telementry.xlsx"
    elif sensor == "MAG2" and sensorType == "telementry":
        filePath = "MAG_telementry.xlsx"
    elif sensor == "MAG3" and sensorType == "telementry":
        filePath = "MAG_telementry.xlsx"
    elif sensor == "GPS1":
        filePath = "GPS1.xlsx"
    elif sensor == "GP2":
        filePath = "GPS2.xlsx"
    elif sensor == "NS1":
        filePath = "NS1.xlsx"
    elif sensor == "NS2" :
        filePath = "NS2.xlsx"
    elif sensor == "NS3":
        filePath = "NS3.xlsx"
    elif sensor == "NS4":
        filePath = "NS4.xlsx"
    elif sensor == "NS5":
        filePath = "NS5.xlsx"
    elif sensor == "NS6" :
        filePath = "NS6.xlsx"
    elif sensor == "NS7":
        filePath = "NS7.xlsx"
    elif sensor == "NS8":
        filePath = "NS8.xlsx"
    elif sensor == "NS9" :
        filePath = "NS9.xlsx"
    elif sensor == "NS10":
        filePath = "NS10.xlsx"
    elif sensor == "NS11" :
        filePath = "NS11.xlsx"
    elif sensor == "NS12":
        filePath = "NS12.xlsx"
    elif sensor == "NS13" :
        filePath = "NS13.xlsx"
    elif sensor == "NS14" :
        filePath = "NS14.xlsx"
    elif sensor == "NS15":
        filePath = "NS15.xlsx"
    
    else:
        #messagebox.showerror("Input Error", "No matching file for this sensor and sensor type combination.")
        return
    
    commandsDf = readSensorCommands(filePath)
    global commandsDict
    commandsDict = {row['Command Display']: row[1:].to_dict() for _, row in commandsDf.iterrows()}
    commandMenu['values'] = list(commandsDict.keys())
    commandMenu.set('')


def updateDisplayBox(text):
    displayBox.config(state=tk.NORMAL)
    displayBox.delete(1.0, tk.END)  
    displayBox.insert(tk.END, text) 
    displayBox.config(state=tk.DISABLED)

def enableEditing():
    global isEditing
    selectedCommand = commandVar.get()
    
    if selectedCommand:
        commandData = commandsDict.get(selectedCommand, {})
        lengthCode = commandData.get('LENGTH', 0)
        messagebox.showinfo("Edit Information", f"You need to enter {lengthCode-1} bytes of data.")
    if editButton['text'] == "Edit":
        insertEntry.config(state=tk.NORMAL) 
        editButton.config(text="Done")
        isEditing = True
    else:
        insertEntry.config(state=tk.DISABLED)  
        editButton.config(text="Edit")
        isEditing = False


def sendBufferData():
    COM=comEntry.get()
    if not sendBuffer:
        messagebox.showerror("Send Error", "No data to send. The send buffer is empty.")
        return
    try:
        timeout = float(timeout_entry.get())
    except ValueError:
        timeout = 15 
    try:
        with serial.Serial(COM, 57600, timeout=1) as ser:
            time.sleep(2) 
            for entry in sendBuffer:
                data = ' '.join(map(str, entry))
                print(f"Sending to Arduino: {data.strip()}")
                ser.write(data.encode('utf-8'))
                ser.flush()
                time.sleep(timeout)
                response = ""
                while ser.in_waiting > 0:
                    response += ser.read(ser.in_waiting).decode('utf-8')
                    time.sleep(0.1)

                if response:
                    print(f"Received from sensor stimulator (before processing): {response.strip()}")
                    response_list = []
                    for item in response.strip().split():
                        try:
                            response_list.append(int(item))  
                        except ValueError:
                            continue  

                    if len(response_list) >= 2 and response_list[0] == 31 and response_list[1] == 127:
                        response_list = response_list[2:]

                    if len(response_list) >= 2 and response_list[-2] == 31 and response_list[-1] == 255:
                        response_list = response_list[:-2]
                    # Check for specific response values
                    if response_list==1:
                        messagebox.showerror("Error", "Invalid Tc ID")
                    elif response_list==2:
                        messagebox.showerror("Error", "Invalid parameters")
                    elif response_list==0:
                        messagebox.INFO("NO ERROR")

                    cleaned_response = ' '.join(map(str, response_list))
                    print(f"stimulator (after processing): {cleaned_response}")
                    updateDisplayBox(cleaned_response)
                    sensor = sensorVar.get()
                    sensorType = sensorTVar.get()
                    selectedCommand = commandVar.get()
                    commandData = commandsDict.get(selectedCommand, {})
                    idValue = commandData.get('ID', '')
                    if sensorType == 'telementry' and sensor in ['WHEEL1', 'WHEEL3', 'WHEEL3']:
                        if idValue == 133:
                            speed_value =response_list
                            SpeedBox.insert(tk.END,speed_value)
                        elif idValue == 134:
                            reference_value = response_list
                            RefernceBox.insert(tk.END,reference_value)
                        elif idValue == 135:
                            current_value = response_list
                            CurrentBox.insert(tk.END,current_value)
                        elif idValue == 138:
                            duty_cycle_value =response_list[0:2]
                            Bu_speed=response_list[2:4]
                            DutyBox.insert(tk.END,duty_cycle_value)
                            BUSpeedBox.insert(tk.END,Bu_speed)

                        elif idValue==130:
                            control_mode_value = response_list[6]
                            print(control_mode_value)
                            if control_mode_value==0:
                                ControlBox.insert(tk.END,"Idle")
                            elif control_mode_value==1:
                                ControlBox.insert(tk.END,"No control")
                            elif control_mode_value==2:
                                ControlBox.insert(tk.END,"DutyCycle I/P")
                            elif control_mode_value==3:
                                ControlBox.insert(tk.END,"SpeedController")
                            backup_mode_value = response_list[7]
                            print(f"backup_mode_value: {backup_mode_value}")
                            backup_mode_bit = (backup_mode_value >> 0) & 1
                            BackupBox.insert(tk.END, backup_mode_bit) 

                            motor_switch_bit = (backup_mode_value >> 1) & 1
                            MotorBox.insert(tk.END, motor_switch_bit)  

                            hall_switch_bit = (backup_mode_value >> 2) & 1
                            HallBox.insert(tk.END, hall_switch_bit)    

                            encoder_switch_bit = (backup_mode_value >> 3) & 1
                            EncoderBox.insert(tk.END, encoder_switch_bit) 

                            error_code_bit = (backup_mode_value >> 4) & 1
                            ErrorBox.insert(tk.END, error_code_bit)    
                else:       
                    print("No data waiting to be read.")

    except serial.SerialException as e:
        print(f"Failed to communicate with Arduino: {e}")



root = tk.Tk()
root.title("Sensor Command/Actuator Simulator")

sendBuffer = []
commandsDict = {}
isEditing = False

root.configure(bg="#F5F5F5")

style = ttk.Style()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
style.theme_use('clam') 
style.configure('TLabel', background="#F5F5F5", foreground="#333333", font=('Helvetica', 12))
style.configure('TButton', background="#4CAF50", foreground="#FFFFFF", font=('Helvetica', 12, 'bold'), padding=5)
style.configure('TCheckbutton', background="#F5F5F5", foreground="#333333", font=('Helvetica', 12, 'bold'))
style.configure('TCombobox', font=('Helvetica', 12), padding=5)

main=tk.LabelFrame(root)
main.grid(row=1, column=1, padx=30, pady=30, sticky='nsew')

#ACTUATOR TESTING PART
Actuatorlabel=tk.LabelFrame(main,text="ACTUATOR TESTING")
Actuatorlabel.grid(row=0, column=2, padx=10, pady=10, sticky='w')
actuator=tk.LabelFrame(Actuatorlabel)
actuator.grid(row=0, column=2, padx=10, pady=10, sticky='w')
ActuatorselectionVar = tk.StringVar()
ActuatorselectionLabel = tk.Label(actuator, text="Select Actuator:")
ActuatorselectionLabel.grid(row=1, column=2, padx=10, pady=5, sticky='w')
ActuatorselectionOptions = readSensorOptions('Actuator.xlsx')
ActuatorselectionMenu = ttk.Combobox(actuator, textvariable=ActuatorselectionVar, values=ActuatorselectionOptions)
ActuatorselectionMenu.grid(row=1, column=3, padx=10, pady=5, sticky='w')

on_label = ttk.Label(actuator, text="On")
on_label.grid(row=2, column=2, padx=(10, 5), pady=2, sticky='w')
on_var = tk.StringVar()
on_entry =ttk.Combobox(actuator, textvariable=on_var, state="normal")
on_entry['value']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
on_entry.grid(row=2, column=3, padx=(5,10), pady=2, sticky='w')

off_label = ttk.Label(actuator, text="Off")
off_label.grid(row=3, column=2, padx=(10, 5), pady=2, sticky='w')
off_var = tk.StringVar()
off_entry = ttk.Combobox(actuator, textvariable=off_var, state="normal")
off_entry['values']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
off_entry.grid(row=3, column=3, padx=(5,10), pady=2, sticky='w')

motor_frame = ttk.LabelFrame(Actuatorlabel, text="Motor Commands")
motor_frame.grid(row=4, column=2, columnspan=2, padx=10, pady=10, sticky='nsew')

WspeedLabel=ttk.Label(motor_frame,text='Wheel Speed')
WspeedLabel.grid(row=5,column=2,padx=(10, 5), pady=2, sticky='w')
WspeedVar=tk.StringVar()
WspeedEntry=ttk.Combobox(motor_frame,textvariable=WspeedVar)
WspeedEntry.grid(row=5, column=3, padx=(5,10), pady=2, sticky='w')

duty_cycle_label = ttk.Label(motor_frame, text="% Duty Cycle")
duty_cycle_label.grid(row=6, column=2, padx=10, pady=2, sticky='w')
duty_cycle_var = tk.StringVar()
duty_cycle_entry =ttk.Combobox(motor_frame, textvariable=duty_cycle_var, state="normal") 
duty_cycle_entry['values']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
duty_cycle_entry.grid(row=6, column=3, padx=(5,10), pady=2, sticky='w')

WheelDatalabel=ttk.LabelFrame(Actuatorlabel,text='WHEEL DATA')
WheelDatalabel.grid(row=7, column=2, padx=10, pady=2, sticky='w')

SpeedLabel=ttk.Label(WheelDatalabel,text='Speed[rpm]')
SpeedLabel.grid(row=8, column=2, padx=(10, 5), pady=2, sticky='w')
SpeedBox=tk.Text(WheelDatalabel, height=1, width=15)
SpeedBox.grid(row=8, column=3, padx=(10, 5), pady=2, sticky='w')

RefernceLabel=ttk.Label(WheelDatalabel,text='Reference[rpm]')
RefernceLabel.grid(row=9, column=2, padx=(10, 5), pady=2, sticky='w')
RefernceBox=tk.Text(WheelDatalabel, height=1, width=15)
RefernceBox.grid(row=9, column=3, padx=(10, 5), pady=2, sticky='w')

CurrentLabel=ttk.Label(WheelDatalabel,text='Current[mA]')
CurrentLabel.grid(row=10, column=2, padx=(10, 5), pady=2, sticky='w')
CurrentBox=tk.Text(WheelDatalabel, height=1, width=15)
CurrentBox.grid(row=10, column=3, padx=(10, 5), pady=2, sticky='w')

DutyLabel=ttk.Label(WheelDatalabel,text='Duty[%]')
DutyLabel.grid(row=11, column=2, padx=(10, 5), pady=2, sticky='w')
DutyBox=tk.Text(WheelDatalabel, height=1, width=15)
DutyBox.grid(row=11, column=3, padx=(10, 5), pady=2, sticky='w')

BUSpeedLabel=ttk.Label(WheelDatalabel,text='BU Speed[rpm]')
BUSpeedLabel.grid(row=12, column=2, padx=(10, 5), pady=2, sticky='w')
BUSpeedBox=tk.Text(WheelDatalabel, height=1, width=15)
BUSpeedBox.grid(row=12, column=3, padx=10, pady=2, sticky='w')

WheelDatalabel=ttk.LabelFrame(Actuatorlabel,text='WHEEL Status')
WheelDatalabel.grid(row=13, column=2, padx=(10, 5), pady=10, sticky='w')

BackupLabel=ttk.Label(WheelDatalabel,text='Backup Mode')
BackupLabel.grid(row=14, column=2, padx=(10, 5), pady=2, sticky='w')
BackupBox=tk.Text(WheelDatalabel, height=1, width=15)
BackupBox.grid(row=14, column=3, padx=(10, 5), pady=2, sticky='w')

ControlLabel=ttk.Label(WheelDatalabel,text='Control Mode')
ControlLabel.grid(row=15, column=2, padx=(10, 5), pady=2, sticky='w')
ControlBox=tk.Text(WheelDatalabel, height=1, width=15)
ControlBox.grid(row=15, column=3, padx=(10, 5), pady=2, sticky='w')

MotorLabel=ttk.Label(WheelDatalabel,text='Motor Mode')
MotorLabel.grid(row=16, column=2, padx=(10, 5), pady=2, sticky='w')
MotorBox=tk.Text(WheelDatalabel, height=1, width=15)
MotorBox.grid(row=16, column=3, padx=(10, 5), pady=2, sticky='w')

HallLabel=ttk.Label(WheelDatalabel,text='Hall Switch')
HallLabel.grid(row=17, column=2, padx=(10, 5), pady=2, sticky='w')
HallBox=tk.Text(WheelDatalabel, height=1, width=15)
HallBox.grid(row=17, column=3, padx=(10, 5), pady=2, sticky='w')

EncoderLabel=ttk.Label(WheelDatalabel,text='Encoder Switch')
EncoderLabel.grid(row=18, column=2, padx=(10, 5), pady=2, sticky='w')
EncoderBox=tk.Text(WheelDatalabel, height=1, width=15)
EncoderBox.grid(row=18, column=3, padx=(10, 5), pady=2, sticky='w')

ErrorLabel=ttk.Label(WheelDatalabel,text='Error Code')
ErrorLabel.grid(row=19, column=2, padx=(10, 5), pady=2, sticky='w')
ErrorBox=tk.Text(WheelDatalabel, height=1, width=15)
ErrorBox.grid(row=19, column=3, padx=(10, 5), pady=2, sticky='w')


#submitButton = tk.Button(root, text="Submit")
#submitButton.grid(row=12, column=3, pady=10, sticky='w')

#sensor testing part

SensorTestinglabel=tk.LabelFrame(main,text="SENSOR TESTING")
SensorTestinglabel.grid(row=0, column=0, padx=2, pady=5, sticky='nw')

powerVar = tk.BooleanVar()
powerButton = tk.Checkbutton(SensorTestinglabel, text="Power", variable=powerVar, command=toggleInputs)
powerButton.grid(row=0, column=0, padx=10, pady=10, sticky='w')


sensorVar = tk.StringVar()
sensorLabel = tk.Label(SensorTestinglabel, text="Select Sensor:")
sensorLabel.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')
sensorOptions = readSensorOptions('Sensor_name.xlsx')
sensorMenu = ttk.Combobox(SensorTestinglabel, textvariable=sensorVar, values=sensorOptions,state=tk.DISABLED)
sensorMenu.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')
sensorMenu.bind("<<ComboboxSelected>>", updateCommands)

sensorTVar = tk.StringVar()
sensorTLabel = tk.Label(SensorTestinglabel, text="Select Sensor Type:")
sensorTLabel.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')
sensorTypeOptions = readSensorType('Sensor_type.xlsx')
sensorTMenu = ttk.Combobox(SensorTestinglabel, textvariable=sensorTVar, values=sensorTypeOptions,state=tk.DISABLED)
sensorTMenu.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')
sensorTMenu.bind("<<ComboboxSelected>>", updateCommands)

commandVar = tk.StringVar()
commandLabel = tk.Label(SensorTestinglabel, text="Select Command:")
commandLabel.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')
commandMenu = ttk.Combobox(SensorTestinglabel, textvariable=commandVar,state=tk.DISABLED)
commandMenu.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')


insertVar = tk.StringVar()
insertLabel = tk.Label(SensorTestinglabel, text="Insert Data:")
insertLabel.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')
insertEntry = tk.Entry(SensorTestinglabel, textvariable=insertVar, state=tk.DISABLED, width=100)
insertEntry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='w')

displayBoxLabel = tk.Label(SensorTestinglabel, text="Display Box:")
displayBoxLabel.grid(row=6, column=0, padx=(10, 5), pady=10, sticky='w')
displayBox = tk.Text(SensorTestinglabel, height=4, width=75, state=tk.DISABLED)
displayBox.grid(row=6, column=1, padx=(5, 10), pady=10, sticky='w')

submitButton = tk.Button(SensorTestinglabel, text="Submit", command=onButtonClick)
submitButton.grid(row=5, column=1,padx=(50,5), pady=10, sticky='w')

resetButton = tk.Button(SensorTestinglabel, text="Reset", command=resetAll)
resetButton.grid(row=5, column=1,padx=(5,2), pady=10, sticky='w')

editButton = tk.Button(SensorTestinglabel, text="Edit", command=enableEditing)
editButton.grid(row=5, column=1,padx=(105,20), pady=10, sticky='w')

comLabel=tk.Label(SensorTestinglabel,text="COM")
comLabel.grid(row=2, column=1, padx=(300), pady=10, sticky='w')
comEntry=tk.Entry(SensorTestinglabel)
comEntry.grid(row=2, column=1, padx=(400), pady=10, sticky='w')

timeout_label = tk.Label(SensorTestinglabel, text="Timeout (seconds):")
timeout_label.grid(row=3, column=1, padx=(300), pady=10, sticky='w')
timeout_entry = tk.Entry(SensorTestinglabel)
timeout_entry.grid(row=3, column=1, padx=(400), pady=10, sticky='w')
timeout_entry.insert(0, "15")  

sendButton = ttk.Button(SensorTestinglabel, text="Send", command=sendBufferData, state="disabled") 
sendButton.grid(row=7, column=1, pady=10, sticky='w')
root.mainloop()
