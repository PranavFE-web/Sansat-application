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
    elif sensor == "WHEEL2" and sensorType == "telecommand":
        filePath = "Wheel_telecommand.xlsx"
    elif sensor == "WHEEL2" and sensorType == "telementry":
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
    if not sendBuffer:
        messagebox.showerror("Send Error", "No data to send. The send buffer is empty.")
        return
    try:
        timeout = float(timeout_entry.get())
    except ValueError:
        timeout = 15 
    try:
        with serial.Serial('COM7', 57600, timeout=1) as ser:
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
                    if 1 in response_list:
                        messagebox.showerror("Error", "Invalid Tc ID")
                    elif 2 in response_list:
                        messagebox.showerror("Error", "Invalid parameters")
                    elif 0 in response_list:
                        messagebox.showerror("NO ERROR")

                    cleaned_response = ' '.join(map(str, response_list))
                    print(f"stimulator (after processing): {cleaned_response}")
                    updateDisplayBox(cleaned_response)
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
style.theme_use('clam')
root.grid_columnconfigure(0, weight=0)  
root.grid_columnconfigure(1, weight=1)  
root.grid_columnconfigure(2, weight=0)  
style.configure('TLabel', background="#F5F5F5", foreground="#333333", font=('Helvetica', 12, 'bold'))
style.configure('TButton', background="#4CAF50", foreground="#FFFFFF", font=('Helvetica', 12, 'bold'), padding=5)
style.configure('TCheckbutton', background="#F5F5F5", foreground="#333333", font=('Helvetica', 12, 'bold'))
style.configure('TCombobox', font=('Helvetica', 12), padding=5)

powerVar = tk.BooleanVar()
powerButton = tk.Checkbutton(root, text="Power", variable=powerVar, command=toggleInputs)
powerButton.grid(row=0, column=0, padx=10, pady=10, sticky='w')

#ACTUATOR TESTING PART
Actuatorlabel=tk.Label(root,text="ACTUATOR TESTING")
Actuatorlabel.grid(row=0, column=2, padx=10, pady=10, sticky='w')

ActuatorselectionVar = tk.StringVar()
ActuatorselectionLabel = tk.Label(root, text="Select Actuator:")
ActuatorselectionLabel.grid(row=1, column=2, padx=10, pady=10, sticky='w')
ActuatorselectionOptions = readSensorOptions('Actuator.xlsx')
ActuatorselectionMenu = ttk.Combobox(root, textvariable=ActuatorselectionVar, values=ActuatorselectionOptions)
ActuatorselectionMenu.grid(row=1, column=3, padx=10, pady=10, sticky='w')

on_label = ttk.Label(root, text="On")
on_label.grid(row=2, column=2, padx=(10, 5), pady=2, sticky='w')
on_var = tk.StringVar()
on_entry =ttk.Combobox(root, textvariable=on_var, state="normal")
on_entry['value']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
on_entry.grid(row=2, column=3, padx=(5,10), pady=2, sticky='w')

off_label = ttk.Label(root, text="Off")
off_label.grid(row=3, column=2, padx=(10, 5), pady=2, sticky='w')
off_var = tk.StringVar()
off_entry = ttk.Combobox(root, textvariable=off_var, state="normal")
off_entry['values']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
off_entry.grid(row=3, column=3, padx=(5,10), pady=2, sticky='w')

duty_cycle_label = ttk.Label(root, text="% Duty Cycle")
duty_cycle_label.grid(row=4, column=2, padx=(10, 5), pady=2, sticky='w')
duty_cycle_var = tk.StringVar()
duty_cycle_entry =ttk.Combobox(root, textvariable=duty_cycle_var, state="normal") 
duty_cycle_entry['values']=('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
duty_cycle_entry.grid(row=4, column=3, padx=(5,10), pady=2, sticky='w')
submitButton = tk.Button(root, text="Submit")
submitButton.grid(row=6, column=3, pady=10, sticky='w')

#sensor testing part

SensorTestinglabel=tk.Label(root,text="SENSOR TESTING")
SensorTestinglabel.grid(row=0, column=1, padx=10, pady=10, sticky='w')

sensorVar = tk.StringVar()
sensorLabel = tk.Label(root, text="Select Sensor:")
sensorLabel.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')
sensorOptions = readSensorOptions('Sensor_name.xlsx')
sensorMenu = ttk.Combobox(root, textvariable=sensorVar, values=sensorOptions)
sensorMenu.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')
sensorMenu.bind("<<ComboboxSelected>>", updateCommands)

sensorTVar = tk.StringVar()
sensorTLabel = tk.Label(root, text="Select Sensor Type:")
sensorTLabel.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')
sensorTypeOptions = readSensorType('Sensor_type.xlsx')
sensorTMenu = ttk.Combobox(root, textvariable=sensorTVar, values=sensorTypeOptions)
sensorTMenu.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')
sensorTMenu.bind("<<ComboboxSelected>>", updateCommands)

commandVar = tk.StringVar()
commandLabel = tk.Label(root, text="Select Command:")
commandLabel.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')
commandMenu = ttk.Combobox(root, textvariable=commandVar)
commandMenu.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')


insertVar = tk.StringVar()
insertLabel = tk.Label(root, text="Insert Data:")
insertLabel.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')
insertEntry = tk.Entry(root, textvariable=insertVar, state=tk.DISABLED, width=100)
insertEntry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='w')

displayBoxLabel = tk.Label(root, text="Display Box:")
displayBoxLabel.grid(row=6, column=0, padx=(10, 5), pady=10, sticky='w')
displayBox = tk.Text(root, height=4, width=75, state=tk.DISABLED)
displayBox.grid(row=6, column=1, padx=(5, 10), pady=10, sticky='w')

submitButton = tk.Button(root, text="Submit", command=onButtonClick)
submitButton.grid(row=5, column=1,padx=(50,5), pady=10, sticky='w')

resetButton = tk.Button(root, text="Reset", command=resetAll)
resetButton.grid(row=5, column=1,padx=(5,2), pady=10, sticky='w')

editButton = tk.Button(root, text="Edit", command=enableEditing)
editButton.grid(row=5, column=1,padx=(105,20), pady=10, sticky='w')

timeout_label = tk.Label(root, text="Timeout (seconds):")
timeout_label.grid(row=3, column=1, padx=(300), pady=10, sticky='w')
timeout_entry = tk.Entry(root)
timeout_entry.grid(row=3, column=1, padx=(400), pady=10, sticky='w')
timeout_entry.insert(0, "15")  

sendButton = ttk.Button(root, text="Send", command=sendBufferData, state="disabled") 
sendButton.grid(row=7, column=1, pady=10, sticky='w')
root.mainloop()
#till Friday 30/08/2024