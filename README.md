# AutoScreenshot

Program for those who intend to attend online classes but unfortunate circumstances have rendered such impossible. (or too lazy to listen).


This program will automatically take screenshots, save it to your clipboard, and paste it onto a online document of your choosing, whether that be Google Docs, Microsoft Word,
or any other platforms which support the ability to paste in images.

# How it works

- Before turning on the autoscreenshot feature of this program, you must designate a `screenshot region`, and `polling region`.
- `screenshot region` is the area that will get screenshotted after a change has been detected in `polling region`.
- When setting the regions, one must first select the **top-left corner** followed by the **bottom-right corner** of the region.
  - Selecting a region in a bottom-right to top-left manner will result in an error. **(Will be fixed in future versions)**
- When both `screenshot region` and `polling region` has been set, you can now toggle on the autoscreenshot feature by pressing `Toggle AutoScreenshot`.
- When the `AutoScreenshot` feature is running, you can also toggle on `auto-paste` which will automatically paste the most recent content on your clipboard,
***(which will most likely be a screenshot taken by the program)***, to any medium of your choosing. ***(Google Docs, Microsoft Word, etc..)***


# Potential Bugs
- When the `AutoScreenshot` feature is running, there might be a delay in button presses of the GUI.
  - This is caused by the program's detect image change algorithm, where it's taking 2 snapshots, separated by time from each other using `cv2.waitKey(1000)`.
  This causes the GUI to wait for 1000ms before registering any user input.
