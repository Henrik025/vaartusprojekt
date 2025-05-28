import calendar
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Praegune aeg, callib datetime moodulit ja sündmuste hoius
current = datetime.now()
year = current.year
month = current.month
day = current.day
events = {}
buttons = {}

# Dialog box mis laseb lisada/muuta ja kustutada syndmusi
def custom_event_dialog(date_key, msg):
    dialog = tk.Toplevel(root)
    dialog.title("Lisa/Muuda sündmust")
    dialog.geometry("350x180")
    dialog.transient(root)
    dialog.grab_set()
    tk.Label(dialog, text=msg, wraplength=320, justify="left").pack(pady=10)

    event_var = tk.StringVar()
    if date_key in events:
        event_var.set(events[date_key])

    entry = tk.Entry(dialog, textvariable=event_var, width=40)
    entry.pack(pady=5)

    result = {"action": None, "event": None}

    def on_save():
        result["action"] = "save"
        result["event"] = event_var.get().strip()
        dialog.destroy()

    def on_delete():
        result["action"] = "delete"
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Lisa/Muuda", command=on_save).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Kustuta", command=on_delete).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Tühista", command=on_cancel).pack(side="left", padx=5)

    root.wait_window(dialog)
    return result

# Funktsioon kuupäeva jaoks
def on_date_click(d):
    date_key = (year, month, d)
    existing_event = events.get(date_key)
    if existing_event:
        msg = f"Sündmus on {year}-{month:02d}-{d:02d}:\n{existing_event}\n\nMuuda või kustuta see sündmus:"
    else:
        msg = f"Sündmus puudub {year}-{month:02d}-{d:02d} kuupäevaks.\n\nLisa uus sündmus:"
    response = custom_event_dialog(date_key, msg)

    if response["action"] == "save" and response["event"]:
        events[date_key] = response["event"]
        messagebox.showinfo("Salvestatud", "Sündmus on edukalt salvestatud!")
    elif response["action"] == "delete":
        if date_key in events:
            del events[date_key]
            messagebox.showinfo("Kustutatud", "Sündmus on eemaldatud.")
    update_button_color(date_key)

# Värvi update
def update_button_color(date_key):
    if date_key in buttons:
        if date_key in events:
            buttons[date_key].config(bg="red")
        else:
            buttons[date_key].config(bg="SystemButtonFace")

# Launch tkinter
root = tk.Tk()
root.title("Sündmuste Kalender")

# Praegune kuupäev ja kellaaeg
current_date = f"Tänane kuupäev: {year}-{month}-{day} {current.hour:02d}:{current.minute:02d}:{current.second:02d}"
tk.Label(root, text=calendar.month_name[month] + " " + str(year), font=("Arial", 20)).pack()
tk.Label(root, text=current_date, font=("Arial", 12)).pack()

# Nuppude frame
frame = tk.Frame(root)
frame.pack(padx=22, pady=22)

# Nädalapäevad koos kalendri nuppudega
for i, dayname in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    tk.Label(frame, text=dayname, font=("Arial", 10, "bold")).grid(row=0, column=i)

mon_day = calendar.monthcalendar(year, month)
for row_idx, week in enumerate(mon_day, start=1):
    for col_idx, d in enumerate(week):
        if d != 0:
            date_key = (year, month, d)
            btn = tk.Button(frame, text=str(d), width=4,
                            command=lambda d=d: on_date_click(d))
            btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            buttons[date_key] = btn
            update_button_color(date_key)

root.mainloop()