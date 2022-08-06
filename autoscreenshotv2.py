import tkinter as tk
import cv2
from PIL import ImageGrab
import mouse
import numpy as np
from io import BytesIO
import win32clipboard as clip
import win32con


class auto_screenshot:

    SS_REGION = []
    SAMPLE_REGION = []
    
    
    def autoscreenshot(self):
        
        # Okay baby, pay attention. We are going to go on a coding adventure. Starting with the autoscreenshot program!!!!
        # Reminders: this function is contained in an infinite loop until cancelled.
        # This function will take 2 snapshots of sample region, x seconds apart.
        # After the second snapshot is taken, compare the first and the second snapshot to each other, spotting for difference between them.
        # If the difference goes past a N threshold, perform screenshot and paste into document.
        
        snapshot1 = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0]+27, self.SAMPLE_REGION[0][1]+58, self.SAMPLE_REGION[1][0]+170, self.SAMPLE_REGION[1][1]+192))), cv2.COLOR_BGR2GRAY)
        #print("snapshot1 is taken")
        cv2.waitKey(500)
        snapshot2 = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0]+27, self.SAMPLE_REGION[0][1]+58, self.SAMPLE_REGION[1][0]+170, self.SAMPLE_REGION[1][1]+192))), cv2.COLOR_BGR2GRAY)
        #print("snapshot2 is taken")
        
        # INSERT CODE HERE >>>>>....
        self.subtracted = cv2.subtract(snapshot1, snapshot2)
        cv2.imshow('window', self.subtracted)
        if np.sum(self.subtracted) > 0:
            
            # copy screenshot to clipboard
            self.output = BytesIO()            
            self.take_screenshot = ImageGrab.grab(bbox=(self.SS_REGION[0][0]+27, self.SS_REGION[0][1]+58, self.SS_REGION[1][0]+170, self.SS_REGION[1][1]+192))
            self.take_screenshot.convert('RGB').save(self.output, 'BMP')
            self.ss_data = self.output.getvalue()[14:]
            clip.OpenClipboard()
            clip.EmptyClipboard()
            clip.SetClipboardData(win32con.CF_DIB, self.ss_data)
            clip.CloseClipboard()
            
            print("Screenshot!")    
            cv2.waitKey(500)


        # ....... <<< END INSERT CODE 
        
        if end_auto:
            return
        gui.toggle_screenshot.after(100, self.autoscreenshot)
        
    def set_ss_zone(self):
        self.CLICK_COUNT = 0
        self.SS_REGION = []
        def manager_ss():
            self.SS_REGION.append(mouse.get_position())
            self.CLICK_COUNT += 1
            if self.CLICK_COUNT == 2:
                mouse.unhook_all()
                print(self.SS_REGION)
        mouse.on_click(lambda: manager_ss())
        
        
    def set_sample_zone(self):
        self.CLICK_COUNT = 0
        self.SAMPLE_REGION = []
        def manager_sample():
            self.SAMPLE_REGION.append(mouse.get_position())
            self.CLICK_COUNT += 1
            if self.CLICK_COUNT == 2:
                mouse.unhook_all()
                print(self.SAMPLE_REGION)
                
        mouse.on_click(lambda: manager_sample())            
    
    
    def view_screenshot_region(self,state=1):
        if state:
            global screenshot
            self.screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SS_REGION[0][0]+27, self.SS_REGION[0][1]+58, self.SS_REGION[1][0]+170, self.SS_REGION[1][1]+192))), cv2.COLOR_RGB2BGR)
            cv2.imshow('screenshot', self.screenshot)
            
        elif not state:
            try:
                cv2.destroyWindow('screenshot')
            except:
                print("already gone chief")


    def view_sample_region(self, state=1):
        if state:
    
            self.screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(self.SAMPLE_REGION[0][0]+27, self.SAMPLE_REGION[0][1]+58, self.SAMPLE_REGION[1][0]+170, self.SAMPLE_REGION[1][1]+192))), cv2.COLOR_RGB2BGR)
            cv2.imshow('SAMPLE', self.screenshot)

        elif not state:
            try:
                cv2.destroyWindow('SAMPLE')
            except:
                print("already gone chief")            



class GUI(auto_screenshot):
    WIDTH = 540
    HEIGHT = 300
    toggle_screenshot_state = 1
    toggle_screenshot_preview_state = 1
    toggle_sample_preview_state = 1
    
    
    def  __init__(self) -> None:
        # GUI Frame
        self.window = tk.Tk()
        self.window.title("AutoScreenshot V2")
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.window.columnconfigure([0,1], weight=1)
        self.window.rowconfigure([0,1,2,3,4], minsize=20, weight=1)
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
            self.toggle_sample_preview_state = 0
            autoss.view_sample_region(1)
            
        else:
            autoss.view_sample_region(0)
            self.toggle_sample_preview_state = 1
        
    
    def press_toggle_screenshot_preview(self):
        if self.toggle_screenshot_state:
            
            autoss.view_screenshot_region(1)
            self.toggle_screenshot_state = 0
            
        else:
            autoss.view_screenshot_region(0)
            self.toggle_screenshot_state = 1


    def press_set_ss_region(self):
        autoss.set_ss_zone()
    
    
    def press_set_sample_region(self):
        autoss.set_sample_zone()
    

    def create_elements(self):
        self.set_ss_area = tk.Button(self.window, text="Set screenshot region", width=self.WIDTH//2, command=self.press_set_ss_region)
        self.set_sample_area = tk.Button(self.window, text="Set sample area", width=self.WIDTH//2, command=self.press_set_sample_region)
        self.toggle_screenshot_preview = tk.Button(self.window, text="Toggle Screenshot Preview", width=self.WIDTH//2, command=self.press_toggle_screenshot_preview)
        self.toggle_sample_preview = tk.Button(self.window, text="Toggle Sample Preview", width=self.WIDTH//2, command=self.press_toggle_sample_preview)
        self.toggle_screenshot = tk.Button(self.window, text="Toggle AutoScreenshot", width=self.WIDTH//2, command=self.press_toggle_screenshot)

        self.set_ss_area.grid                   (column=0, row=0, sticky='nsew', rowspan=3)
        self.set_sample_area.grid               (column=1, row=0, sticky='nsew')
        self.toggle_screenshot_preview.grid     (column=1, row=1, sticky='nsew')
        self.toggle_sample_preview.grid         (column=1, row=2, sticky='nsew')
        self.toggle_screenshot.grid             (column=0, row=3, sticky='nsew', rowspan=2, columnspan=2)


if __name__ == "__main__":
    gui = GUI()
    autoss = auto_screenshot()
    gui.window.mainloop()