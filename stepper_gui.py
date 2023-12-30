import tkinter as tk
import motor
    
class Gui:
    def __init__(self, window):
        self.btn = tk.Button(text="Run motor", command=self.cb_run_motor)
        self.btn.pack()
        self.ent_pos = tk.Entry(width=20)
        self.ent_pos.insert(tk.END, "16")
        self.ent_pos.pack()
        self.ent_vel = tk.Entry(width=20)
        self.ent_vel.insert(tk.END, "10")
        self.ent_vel.pack()
        self.ent_accel = tk.Entry(width=20)
        self.ent_accel.insert(tk.END, "20")
        self.ent_accel.pack()
        self.ent_jerk = tk.Entry(width=20)
        self.ent_jerk.insert(tk.END, "60")
        self.ent_jerk.pack()
        
    def cb_run_motor(self):
        pos = float(self.ent_pos.get())
        vel = float(self.ent_vel.get())
        accel = float(self.ent_accel.get())
        jerk = float(self.ent_jerk.get())
        motor.move(pos, vel, accel, jerk)

window = tk.Tk()
gui = Gui(window)
window.mainloop()