import win32serviceutil
import win32service
import win32event
import time
import subprocess
import wmi
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ANTI_RUBBER(win32serviceutil.ServiceFramework):
    _svc_name_ = "ANTIRUBBER"
    _svc_display_name_ = "AR"
    
    #email info
    SENDER_EMAIL = "" 
    RECEIVER_EMAIL = ""
    EMAIL_PASSWORD = ""

    AUTHORIZED_HIDS = {
        "0001:0201", #example
    }

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.SENDER_EMAIL
        msg["To"] = self.RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.SENDER_EMAIL, self.EMAIL_PASSWORD)
            server.sendmail(self.SENDER_EMAIL, self.RECEIVER_EMAIL, msg.as_string())
            server.quit()
        except:
            pass

    def shutdown_system(self):
        #command = "shutdown /s /t 5 /f"
        #subprocess.run(command, shell=True)
        print("remove the command to shut down the pc when unauthorised hid is dected")

    def get_devices(self):
        c = wmi.WMI()
        
        for device in c.Win32_PnPEntity():
            if device.PNPDeviceID and "VID_" in device.PNPDeviceID and "PID_" in device.PNPDeviceID:
                try:
                    vid_index = device.PNPDeviceID.find("VID_") + 4
                    pid_index = device.PNPDeviceID.find("PID_") + 4
                    vid = device.PNPDeviceID[vid_index:vid_index+4]
                    pid = device.PNPDeviceID[pid_index:pid_index+4]
                    vid_pid = f"{vid}:{pid}"
                    
                    if vid_pid not in self.AUTHORIZED_HIDS:
                        self.send_email("Unauthorized HID Detected", f"Device: {device.Caption}")
                        self.shutdown_system()
                except:
                    pass

    def SvcDoRun(self):
        while self.running:
            self.get_devices()
            time.sleep(10)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(ANTI_RUBBER)
