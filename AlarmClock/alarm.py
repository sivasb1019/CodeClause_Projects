# Import necessary modules
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from threading import Thread
from PIL import Image, ImageTk
from pygame import mixer
from datetime import datetime
from time import sleep

# Define colors for the GUI
bg_color = "#cce6ff"
font_color = "#394B7C"


# Function to display current time on the GUI
def clock():
    # Get current time and update label
    now = datetime.now().strftime("%I:%M:%S %p")
    time.config(text=now)
    # Call clock function after 200ms for real-time display
    root.after(200, clock)


# Function to activate the alarm
def activate_alarm():
    # Check if a message is provided, if not, set a default message
    if not msg_box.get():
        msg_box.insert(0, "Wake up!!!")

    # Display activation icon, show an alarm activated message
    activate_icon = Label(frame, image=enable_img, bg=bg_color)
    activate_icon.place(x=218, y=15)
    messagebox.showinfo("Alarm", "Alarm Activated")

    # Reinitialize thread and start a thread for alarm checking
    global thread
    thread = Thread(target=check_alarm)
    thread.start()


# Function to deactivate the alarm
def deactivate_alarm():
    # Display deactivation icon, show an alarm deactivated message
    deactivate_icon = Label(frame, image=disable_img, bg=bg_color)
    deactivate_icon.place(x=218, y=16)
    messagebox.showerror("Alarm", "Alarm Deactivated")


# Function to ring the alarm
def ring_alarm():
    # Load and play the alarm sound indefinitely
    mixer.music.load("assets/alarm.mp3")
    mixer.music.play(-1)
    selected.set(0)
    # If snooze is set, snooze the alarm; otherwise, display the alarm message and stop the alarm
    if int(snooze_box.get()) > 0:
        snooze_alarm()
    else:
        messagebox.showinfo("Times Up", msg_box.get())
        mixer.music.stop()


# Function to snooze the alarm
def snooze_alarm():
    # Prompt to snooze the alarm for a specified time, then ring the alarm again or stop
    option = messagebox.askyesno("Times Up",
                                 f"{msg_box.get()}\nSnooze {snooze_box.get()} minutes?")
    if option:
        mixer.music.stop()
        sleep(int(snooze_box.get()) * 60)
        ring_alarm()
    else:
        mixer.music.stop()


# Function to continuously check the alarm time
def check_alarm():
    while run:
        control = selected.get()
        if control == 1:
            now = datetime.now().strftime("%I:%M %p")
            alarm_time = f"{hour_box.get()}:{minutes_box.get()} {period_box.get()}"
            if now == alarm_time:
                ring_alarm()
        sleep(1)


# Function to quit the alarm application
def exit_alarm():
    option = messagebox.askokcancel("Confirmation", "Exit 'Alarm Clock'?")
    if option:
        if thread and thread.is_alive():
            global run
            run = False
        root.quit()


# Create the main Tkinter main window
root = Tk()
root.title("Alarm Clock")
root.geometry("400x220")
root.resizable(width=FALSE, height=FALSE)
root.configure(bg=bg_color)

# Create a frame for the GUI elements
frame = Frame(root, width=300, height=300, bg=bg_color, highlightbackground="#394B6C", highlightthickness=4)
frame.pack(side=TOP, fill=X)

# Load images for icons and labels for the alarm interface
img1 = Image.open("assets/alarmclock.png")
img1 = img1.resize((100, 100))
img1 = ImageTk.PhotoImage(img1)

enable_img = Image.open("assets/enable.png")
enable_img = enable_img.resize((23, 23))
enable_img = ImageTk.PhotoImage(enable_img)

disable_img = Image.open("assets/disable.png")
disable_img = disable_img.resize((20, 20))
disable_img = ImageTk.PhotoImage(disable_img)

# Create labels, entry boxes, and combo boxes for setting the alarm
alarm_icon = Label(frame, height=100, image=img1, bg=bg_color)
alarm_icon.place(x=22, y=25)

time = Label(frame, font=("COPPERPLATE GOTHIC LIGHT", 10, "bold"), fg="#1A2A56", bg=bg_color)
time.place(x=22, y=135)

title = Label(frame, text="Alarm", font=("Arial Black", 15, "bold"), fg="#1A2A56", bg=bg_color)
title.place(x=150, y=10)

hour = Label(frame, text="Hours", font="Calibri 8 bold", fg=font_color, bg=bg_color)
hour.place(x=150, y=45)

hour_box = Combobox(frame, font="Calibri 8", width=3, state="readonly")
hour_box['values'] = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
hour_box.current(11)
hour_box.place(x=153, y=65)

minutes = Label(frame, text="Minutes", font="Calibri 8 bold", fg=font_color, bg=bg_color)
minutes.place(x=200, y=45)

minutes_box = Combobox(frame, font="Calibri 8", width=3, state="readonly")
minutes_box['values'] = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                         "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                         "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44",
                         "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59")
minutes_box.current(0)
minutes_box.place(x=203, y=65)

period = Label(frame, text="Period", font="Calibri 8 bold", fg=font_color, bg=bg_color)
period.place(x=250, y=45)

period_box = Combobox(frame, font="Calibri 8", width=3, state="readonly")
period_box['values'] = ("AM", "PM")
period_box.current(0)
period_box.place(x=253, y=65)

snooze = Label(frame, text="Snooze", font="Calibri 8 bold", fg=font_color, bg=bg_color)
snooze.place(x=300, y=45)

snooze_box = Combobox(frame, font="Calibri 8", width=3, state="readonly")
snooze_box['values'] = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
snooze_box.current(0)
snooze_box.place(x=303, y=65)

msg = Label(frame, text="Alarm Message", font="Calibri 8 bold", fg=font_color, bg=bg_color)
msg.place(x=150, y=90)

msg_box = Entry(frame, font="Calibri 8", width=25, bd=2)
msg_box.place(x=153, y=110)

# Create buttons and associated actions for activation, deactivation, and exit
selected = IntVar()
activate_btn = Radiobutton(frame, text="Activate", font="Helvetica 8 bold", value=1,
                           variable=selected, fg=font_color, bg=bg_color, command=activate_alarm)
activate_btn.place(x=150, y=135)

deactivate_btn = Radiobutton(frame, text="Deactivate", font="Helvetica 8 bold", value=2,
                             variable=selected, fg=font_color, bg=bg_color, command=deactivate_alarm)
deactivate_btn.place(x=220, y=135)

exit_btn = Button(frame, text="EXIT", font=("COPPERPLATE GOTHIC BOLD", 9),
                  width=5, fg="#ffffff", bg=font_color, command=exit_alarm)
exit_btn.place(x=190, y=170)

# Initialize Pygame mixer, set run to True, and start the clock function
mixer.init()
run = True
clock()

# Global variable for the thread handling alarm checks and Initialize thread
global thread
thread = Thread(target=check_alarm)

# Start the main GUI loop
root.mainloop()
