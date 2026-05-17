import customtkinter as ctk
import requests
import webbrowser
import threading
import time
import re

CHANNELS = {
    "ח'3": "debiliili", 
    "ח'4": "debiliili2",
    "ח'5": "debiliili3"
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

class ClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("חיבור אוטומטי לשיעור")
        self.geometry("450x300")
        ctk.set_appearance_mode("dark")
        
        self.last_id = 0
        self.running = False
        self.channel_name = ""
        self.channel_url = ""

        self.label_status = ctk.CTkLabel(self, text="בחר כיתה כדי להתחיל", font=("Arial", 20, "bold"))
        self.label_status.pack(pady=20)

        self.class_var = ctk.StringVar(value="בחר כיתה")
        self.class_menu = ctk.CTkOptionMenu(self, values=list(CHANNELS.keys()), variable=self.class_var, command=self.start_monitoring)
        self.class_menu.pack(pady=10)

        self.last_msg_label = ctk.CTkLabel(self, text="ממתין להודעה...", text_color="gray")
        self.last_msg_label.pack(pady=10)

    def start_monitoring(self, choice):
        self.channel_name = CHANNELS[choice]
        self.channel_url = f"https://t.me/s/{self.channel_name}"
        if not self.running:
            self.running = True
            threading.Thread(target=self.monitor, daemon=True).start()
        else:
            print(f"[DEBUG] Switched to {self.channel_name}")
            self.last_id = 0 

    def monitor(self):
        while True:
            try:
                res = requests.get(f"{self.channel_url}?refresh={time.time()}", headers=HEADERS, timeout=10)
                html = res.text
                current_id = self.get_id(html)

                if self.last_id == 0 and current_id != 0:
                    self.last_id = current_id
                    print(f"[DEBUG] Connected. Current ID: {self.last_id}")
                    self.label_status.configure(text="מחפש הודעות...")

                if current_id > self.last_id and self.last_id != 0:
                    print(f"[DEBUG] New Message! ID: {current_id}")
                    all_links = re.findall(r'href="(https?://[^"]+)"', html)
                    
                    found_link = None
                    for link in all_links:
                        if "meet.google.com" in link:
                            found_link = link
                            break
                    
                    if found_link:
                        print(f"[DEBUG] Found: {found_link}")
                        self.label_status.configure(text="פותח קישור!")
                        webbrowser.open(found_link, new=2)
                    else:
                        print("[DEBUG] No Meet link in message")
                        self.label_status.configure(text="הודעה ללא קישור")
                    
                    self.last_id = current_id
                    self.last_msg_label.configure(text=f"ID הודעה: {current_id}")

            except Exception as e:
                print(f"[DEBUG] Error: {e}")
            
            time.sleep(10)

    def get_id(self, html):
        pattern = r't\.me/[^/]+/(\d+)'
        ids = re.findall(pattern, html)
        if ids:
            return max(map(int, ids))
        return 0

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()