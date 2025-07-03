import pyperclip
from src.threads import *
import time


class ClipboardManager:
    def __init__(self,program) -> None:
        self.clipboard=""    
        self.program=program

    def start(self):
        self.clipboard=pyperclip.paste()
        def getclipfunc(self:ClipboardManager,thread:Thread):
            while thread.running:
                if self.clipboard != pyperclip.paste():
                    self.clipboard = pyperclip.paste()
                    self.program.tcpSocket.send_message(self,self.clipboard)
                    print("sending: ",pyperclip.paste())
                time.sleep(0.5)
        self.reading_thread=Thread(self.program,getclipfunc,[self])
        self.reading_thread.start()

    def stop(self):
        self.reading_thread.stop()


    def copy_to_clipboard(self,msg):
        pyperclip.copy(msg)


