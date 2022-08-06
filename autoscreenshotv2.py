import tkinter as tk
import cv2
from PIL import ImageGrab
import mouse
import numpy as np
from io import BytesIO
import win32clipboard as clip
import win32con
import pyautogui


class auto_screenshot:

    SS_REGION = []
    SAMPLE_REGION = []
    

    def autoscreenshot(self):
        
        # Okay baby, pay attention. We are going to go on a coding adventure. Starting with the autoscreenshot program!!!!
        # Reminders: this function is contained in a recursion loop until cancelled.
        # This function will take 2 snapshots of sample region, x seconds apart.
        # After the second snapshot is taken, compare the first and the second snapshot to each other, spotting for difference between them.
        # If the difference goes past a N threshold, perform screenshot and paste into document.
        
        snapshot1 = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0], self.SAMPLE_REGION[0][1], self.SAMPLE_REGION[1][0], self.SAMPLE_REGION[1][1]))), cv2.COLOR_BGR2GRAY)
        #print("snapshot1 is taken")
        cv2.waitKey(500)
        snapshot2 = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0], self.SAMPLE_REGION[0][1], self.SAMPLE_REGION[1][0], self.SAMPLE_REGION[1][1]))), cv2.COLOR_BGR2GRAY)
        #print("snapshot2 is taken")
        
        # INSERT CODE HERE >>>>>....
        self.subtracted = cv2.subtract(snapshot1, snapshot2)
        #cv2.imshow('window', self.subtracted)
        if np.sum(self.subtracted) > 0:
            
            # copy screenshot to clipboard
            self.output = BytesIO()            
            self.take_screenshot = ImageGrab.grab(bbox=(self.SS_REGION[0][0], self.SS_REGION[0][1], self.SS_REGION[1][0], self.SS_REGION[1][1]))
            self.take_screenshot.convert('RGB').save(self.output, 'BMP')
            self.ss_data = self.output.getvalue()[14:]
            clip.OpenClipboard()
            clip.EmptyClipboard()
            clip.SetClipboardData(win32con.CF_DIB, self.ss_data)
            clip.CloseClipboard()
            
            print("Screenshot!")    
            cv2.waitKey(500)
            
            if gui.auto_paste_activation:
                pyautogui.hotkey('ctrl','v')
                print("paste")
            else:
                print("no paste")

        # ....... <<< END INSERT CODE 
        
        if end_auto:
            return
        gui.toggle_screenshot.after(100, self.autoscreenshot)
        
    def set_ss_zone(self):
        self.CLICK_COUNT = 0
        self.SS_REGION = []
        def manager_ss():
            
            def delay():
                mouse.unhook_all()
                gui.set_ss_area['text'] = "Set screenshot region"

                print(self.SS_REGION)

            
            self.SS_REGION.append(pyautogui.position())
            self.CLICK_COUNT += 1
            
            if self.CLICK_COUNT == 1:
                gui.set_ss_area['text'] = f"Corner1: {pyautogui.position()}"

            
            if self.CLICK_COUNT == 2:
                gui.set_ss_area['text'] = f"Corner2: {pyautogui.position()}"
                gui.set_ss_area.after(1000, lambda: delay())
                
        mouse.on_click(lambda: manager_ss())
        
        
    def set_sample_zone(self):
        self.CLICK_COUNT = 0
        self.SAMPLE_REGION = []
        def manager_sample():
            
            
            def delay():
                mouse.unhook_all()
                gui.set_sample_area['text'] = "Set sample area"
                print(self.SAMPLE_REGION)
            
            self.SAMPLE_REGION.append(pyautogui.position())
            
            self.CLICK_COUNT += 1
            
            if self.CLICK_COUNT == 1:
                gui.set_sample_area['text'] = f"Corner1: {pyautogui.position()}"
            
            elif self.CLICK_COUNT == 2:
                gui.set_sample_area['text'] = f"Corner2: {pyautogui.position()}"
                gui.set_sample_area.after(1000, lambda: delay())
            
            
        mouse.on_click(lambda: manager_sample())            
    
    
    def view_screenshot_region(self,state=1):
        if state:
            global screenshot
            self.screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SS_REGION[0][0], self.SS_REGION[0][1], self.SS_REGION[1][0], self.SS_REGION[1][1]))), cv2.COLOR_RGB2BGR)
            cv2.imshow('screenshot', self.screenshot)
            
        elif not state:
            try:
                cv2.destroyWindow('screenshot')
            except:
                print("already gone chief")


    def view_sample_region(self, state=1):
        if state:
    
            self.screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0], self.SAMPLE_REGION[0][1], self.SAMPLE_REGION[1][0], self.SAMPLE_REGION[1][1]))), cv2.COLOR_RGB2BGR)
            cv2.imshow('SAMPLE', self.screenshot)

        elif not state:
            try:
                cv2.destroyWindow('SAMPLE')
            except:
                print("already gone chief")            


class GUI(auto_screenshot):

    WIDTH = 540
    HEIGHT = 220
    toggle_screenshot_state = 1
    toggle_screenshot_preview_state = 1
    toggle_sample_preview_state = 1
    toggle_autopaste_state = 1
    auto_paste_activation = True
    
    
    def  __init__(self) -> None:
        # GUI Frame
        self.window = tk.Tk()
        self.window.title("AutoScreenshot V2")
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.window.columnconfigure([0,1], weight=1)
        self.window.rowconfigure([0,1,2,3,4,5], minsize=20, weight=1)
        # Create GUI elements
        self.create_elements()
    
    
    def press_toggle_screenshot(self):
        global end_auto
        
        if self.toggle_screenshot_state:
            end_auto = 0
            self.toggle_screenshot['text'] = "AutoScreenshot: ON"
            self.toggle_screenshot_state = 0
            global screenshot_loop
            screenshot_loop = self.toggle_screenshot.after(500, lambda: autoss.autoscreenshot())
        else:
            end_auto = 1
            if screenshot_loop:
                self.toggle_screenshot.after_cancel(screenshot_loop)
                
            self.toggle_screenshot['text'] = "AutoScreenshot: OFF"
            self.toggle_screenshot_state = 1
        

    def press_toggle_sample_preview(self):
        if self.toggle_sample_preview_state:
            try:
                self.toggle_sample_preview_state = 0
                autoss.view_sample_region(1)
            except:
                self.toggle_sample_preview['text'] = "Set sample area first"
                self.toggle_sample_preview['background'] = "red"
                self.toggle_sample_preview['foreground'] = "white"
                self.toggle_sample_preview.after(1000, lambda: self.toggle_sample_preview.config(text="Toggle Sample Preview", background="#F0F0F0", foreground="black"))
                
        else:
            autoss.view_sample_region(0)
            self.toggle_sample_preview_state = 1
        
    
    def press_toggle_screenshot_preview(self):
        if self.toggle_screenshot_state:
            try:
                autoss.view_screenshot_region(1)
                self.toggle_screenshot_state = 0
            except:
                self.toggle_screenshot_preview['text'] = "Set screenshot area first"
                self.toggle_screenshot_preview['background'] = "red"
                self.toggle_screenshot_preview['foreground'] = "white"
                self.toggle_screenshot_preview.after(1000, lambda: self.toggle_screenshot_preview.config(text="Toggle Screenshot Preview", background="#F0F0F0", foreground="black"))
            
        else:
            autoss.view_screenshot_region(0)
            self.toggle_screenshot_state = 1


    def press_set_ss_region(self):
        self.set_ss_area['text'] = "Setting screenshot region..."        
        autoss.set_ss_zone()
    
    
    def press_set_sample_region(self):
        self.set_sample_area['text'] = "Setting sample region..."
        autoss.set_sample_zone()
    

    def press_auto_paste(self):
        if not self.toggle_autopaste_state:
            self.toggle_autopaste['text'] = "Toggle auto-paste: ON"
            self.toggle_autopaste_state = 1
            self.auto_paste_activation = True
        else:
            self.toggle_autopaste['text'] = "Toggle auto-paste: OFF"
            self.auto_paste_activation = False
            self.toggle_autopaste_state = 0
            

    def create_elements(self):
        self.set_ss_area = tk.Button(self.window, text="Set screenshot region", width=self.WIDTH//2, command=self.press_set_ss_region)
        self.set_sample_area = tk.Button(self.window, text="Set sample region", width=self.WIDTH//2, command=self.press_set_sample_region)
        self.toggle_screenshot_preview = tk.Button(self.window, text="Toggle Screenshot Preview", width=self.WIDTH//2, command=self.press_toggle_screenshot_preview)
        self.toggle_sample_preview = tk.Button(self.window, text="Toggle Sample Preview", width=self.WIDTH//2, command=self.press_toggle_sample_preview)
        self.toggle_screenshot = tk.Button(self.window, text="Toggle AutoScreenshot", width=self.WIDTH//2, command=self.press_toggle_screenshot)
        self.toggle_autopaste = tk.Button(self.window, text="Toggle auto-paste: ON", command=self.press_auto_paste)

        self.set_ss_area.grid                   (column=0, row=0, sticky='nsew', rowspan=3)
        self.set_sample_area.grid               (column=1, row=0, sticky='nsew')
        self.toggle_screenshot_preview.grid     (column=1, row=1, sticky='nsew')
        self.toggle_sample_preview.grid         (column=1, row=2, sticky='nsew')
        self.toggle_screenshot.grid             (column=0, row=3, sticky='nsew', rowspan=2, columnspan=2)
        self.toggle_autopaste.grid              (column=0, row=5, sticky='nsew', columnspan=2)


if __name__ == "__main__":
    gui = GUI()
    autoss = auto_screenshot()
    gui.window.mainloop()