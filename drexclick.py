import tkinter as tk
import customtkinter as ctk
import threading
import time
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
#ty for reviewing my code,have a nice day!

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AutoClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        
        self.title("drexclick")
        self.geometry("400x700")
        self.resizable(False, False)
        
        
        self.cps = tk.IntVar(value=10)
        self.timer_enabled = tk.BooleanVar(value=False)
        self.timer_duration = tk.IntVar(value=5)
        self.hotkey = "f2"
        self.mouse_activation = tk.BooleanVar(value=False)
        self.mouse_button_choice = tk.StringVar(value="left")
        self.is_clicking = False
        self.is_listening_for_hotkey = False
        self.click_thread = None
        self.mouse_controller = MouseController()
        
       
        self.create_ui()
        
        
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def create_ui(self):
        bright_purple = "#BB00FF"  
        dark_purple = "#CC00FF"    
        light_purple = "#430964"   
        accent_purple = "#510C8A" 
        red = "#FF5555"
        green = "#00FF00"
        
        
        main_frame = ctk.CTkFrame(self, fg_color="#1A1A1A")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
       
        title_label = ctk.CTkLabel(
            main_frame, 
            text="drexclick", 
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=light_purple
        )
        title_label.pack(pady=(10, 30))
        
       
        cps_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cps_frame.pack(fill="x", pady=10)
        
        cps_label = ctk.CTkLabel(
            cps_frame, 
            text="cps:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=bright_purple
        )
        cps_label.pack(anchor="w")
        
        self.cps_slider = ctk.CTkSlider(
            cps_frame, 
            from_=1, 
            to=50, 
            number_of_steps=49,
            variable=self.cps,
            progress_color=bright_purple,
            button_color=light_purple,
            button_hover_color=accent_purple
        )
        self.cps_slider.pack(fill="x", pady=5)
        
        cps_value_frame = ctk.CTkFrame(cps_frame, fg_color="transparent")
        cps_value_frame.pack(fill="x")
        
        cps_min_label = ctk.CTkLabel(cps_value_frame, text="1", text_color=bright_purple)
        cps_min_label.pack(side="left")
        
        self.cps_value_label = ctk.CTkLabel(
            cps_value_frame, 
            text=f"{self.cps.get()} CPS",
            text_color=light_purple,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.cps_value_label.pack(side="left", expand=True)
        
        cps_max_label = ctk.CTkLabel(cps_value_frame, text="50", text_color=bright_purple)
        cps_max_label.pack(side="right")
        
        
        self.cps_slider.configure(command=self.update_cps_label)
        
        timer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        timer_frame.pack(fill="x", pady=(20, 10))
        
        timer_header = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_header.pack(fill="x")
        
        timer_label = ctk.CTkLabel(
            timer_header, 
            text="timer:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=bright_purple
        )
        timer_label.pack(side="left")
        
        timer_switch = ctk.CTkSwitch(
            timer_header, 
            text="", 
            variable=self.timer_enabled,
            progress_color=bright_purple,
            button_color=light_purple,
            button_hover_color=accent_purple
        )
        timer_switch.pack(side="right")
        
        timer_duration_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_duration_frame.pack(fill="x", pady=10)
        
        timer_duration_label = ctk.CTkLabel(
            timer_duration_frame, 
            text="duration (seconds):",
            text_color=bright_purple
        )
        timer_duration_label.pack(side="left")
        
        timer_duration_entry = ctk.CTkEntry(
            timer_duration_frame, 
            width=60, 
            textvariable=self.timer_duration,
            border_color=bright_purple,
            fg_color="#2D2D2D"
        )
        timer_duration_entry.pack(side="right")
        
        
        mouse_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mouse_frame.pack(fill="x", pady=(20, 10))
        
        mouse_header = ctk.CTkFrame(mouse_frame, fg_color="transparent")
        mouse_header.pack(fill="x")
        
        mouse_label = ctk.CTkLabel(
            mouse_header, 
            text="activate with mouse (broken)", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=bright_purple
        )
        mouse_label.pack(side="left")
        
        mouse_switch = ctk.CTkSwitch(
            mouse_header, 
            text="", 
            variable=self.mouse_activation,
            progress_color=bright_purple,
            button_color=light_purple,
            button_hover_color=accent_purple,
            command=self.toggle_mouse_options
        )
        mouse_switch.pack(side="right")
        
        
        self.mouse_button_frame = ctk.CTkFrame(mouse_frame, fg_color="#2D2D2D", corner_radius=8)
        
        mouse_button_label = ctk.CTkLabel(
            self.mouse_button_frame, 
            text="mouse Button:",
            text_color=bright_purple,
            font=ctk.CTkFont(size=14)
        )
        mouse_button_label.pack(pady=(10, 5))
        
        mouse_button_selection = ctk.CTkFrame(self.mouse_button_frame, fg_color="transparent")
        mouse_button_selection.pack(pady=(0, 10))
        
        left_radio = ctk.CTkRadioButton(
            mouse_button_selection,
            text="Left Click",
            variable=self.mouse_button_choice,
            value="left",
            text_color=light_purple,
            fg_color=bright_purple,
            hover_color=accent_purple
        )
        left_radio.pack(side="left", padx=10)
        
        right_radio = ctk.CTkRadioButton(
            mouse_button_selection,
            text="right click",
            variable=self.mouse_button_choice,
            value="right",
            text_color=light_purple,
            fg_color=bright_purple,
            hover_color=accent_purple
        )
        right_radio.pack(side="right", padx=10)
        
        
        hotkey_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        hotkey_frame.pack(fill="x", pady=(20, 10))
        
        hotkey_label = ctk.CTkLabel(
            hotkey_frame, 
            text="activation key:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=bright_purple
        )
        hotkey_label.pack(anchor="w")
        
        hotkey_display_frame = ctk.CTkFrame(hotkey_frame, fg_color="transparent")
        hotkey_display_frame.pack(fill="x", pady=10)
        
        self.hotkey_display = ctk.CTkLabel(
            hotkey_display_frame, 
            text=f"Current: {self.hotkey.upper()}",
            text_color=light_purple,
            font=ctk.CTkFont(size=14)
        )
        self.hotkey_display.pack(side="left")
        
        self.change_hotkey_btn = ctk.CTkButton(
            hotkey_display_frame, 
            text="change hotkey", 
            command=self.start_listening_for_hotkey,
            fg_color=bright_purple,
            hover_color=accent_purple,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.change_hotkey_btn.pack(side="right")
        
        
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.pack(fill="x", pady=(30, 10))
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="status: ready", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=light_purple
        )
        self.status_label.pack()
        
        
        instructions_frame = ctk.CTkFrame(main_frame, fg_color="#2D2D2D", corner_radius=10)
        instructions_frame.pack(fill="x", pady=20)
        
        instructions_label = ctk.CTkLabel(
            instructions_frame, 
            text="credits:", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=red
        )
        instructions_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        instructions_text = ( #was the instruction but uhm too tired to wrtie ecrything and to make it scrollable n shi
            "by drexvain\n"
           
        )
        
        instructions_content = ctk.CTkLabel(
            instructions_frame, 
            text=instructions_text,
            justify="left",
            text_color=green
        )
        instructions_content.pack(anchor="w", padx=10, pady=(0, 10))
        
       
        self.toggle_mouse_options()

    def toggle_mouse_options(self):
        if self.mouse_activation.get():
            self.mouse_button_frame.pack(fill="x", pady=10)
        else:
            self.mouse_button_frame.pack_forget()

    def update_cps_label(self, value):
        self.cps_value_label.configure(text=f"{int(value)} CPS")

    def start_listening_for_hotkey(self):
        self.is_listening_for_hotkey = True
        self.change_hotkey_btn.configure(text="press any key...", fg_color="#FF5555")
        self.status_label.configure(text="status : waiting 4 key")

    def on_key_press(self, key):
        
        if self.is_listening_for_hotkey:
            try:
                
                self.hotkey = key.char.lower()
            except AttributeError:
               
                self.hotkey = str(key).replace("Key.", "").lower()
            
            self.hotkey_display.configure(text=f"current: {self.hotkey.upper()}")
            self.change_hotkey_btn.configure(text="change hotkey", fg_color="#B347D9")
            self.status_label.configure(text="status: ready")
            self.is_listening_for_hotkey = False
            return
        
      
        if not self.mouse_activation.get():
            try:
                if hasattr(key, 'char') and key.char and key.char.lower() == self.hotkey:
                    self.toggle_auto_clicker()
                elif str(key).replace("Key.", "").lower() == self.hotkey:
                    self.toggle_auto_clicker()
            except:
                pass

    def on_mouse_click(self, x, y, button, pressed):
       
        if self.mouse_activation.get() and pressed and not self.is_listening_for_hotkey:
            button_name = "left" if button == Button.left else "right"
            if button_name == self.mouse_button_choice.get():
                self.toggle_auto_clicker()

    def toggle_auto_clicker(self):
        if self.is_clicking:
            self.stop_auto_clicker()
        else:
            self.start_auto_clicker()

    def start_auto_clicker(self):
        if self.is_clicking:
            return
            
        self.is_clicking = True
        activation_method = "Mouse" if self.mouse_activation.get() else "Keyboard"
        self.status_label.configure(text=f"status: clicking ({activation_method})")
        
       
        self.click_thread = threading.Thread(target=self.clicking_loop)
        self.click_thread.daemon = True
        self.click_thread.start()

    def stop_auto_clicker(self):
        self.is_clicking = False
        self.status_label.configure(text="status: ready")

    def clicking_loop(self):
        start_time = time.time()
        
        while self.is_clicking:
           
            delay = 1.0 / self.cps.get()
            
            
            self.mouse_controller.click(Button.left)
            
            
            if self.timer_enabled.get():
                elapsed = time.time() - start_time
                if elapsed >= self.timer_duration.get():
                    break
            
           
            time.sleep(delay)
        
        
        if self.is_clicking:  
            self.is_clicking = False
            
            self.after(0, lambda: self.status_label.configure(text="status: ready"))

    def on_closing(self):
        
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()
        self.destroy()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
