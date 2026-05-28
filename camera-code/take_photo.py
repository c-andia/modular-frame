from datetime import datetime
import time
from picamera2 import Picamera2
from libcamera import controls, Transform
import pathlib

USB_name = '/mnt/Lexar'

def get_time():

        now = datetime.now()
        return now.strftime("%b. %-d, %Y, %-I.%M.%S %p")

def process_timer(stage):
        if stage == 'stop':
                print (f'time elapsed: {time.time()-start} seconds.')

                with open ("timelog.txt", "w") as i:
                        i.write (f'time elapsed: {time.time()-start} seconds.')

def capture():

        try:

                # create folder

                ftime = get_time()

                folderName = f"{USB_name}/Photos/'{ftime}'"
                pathlib.Path.mkdir(folderName)

                # take photos

                cam0.configure(cam0.create_still_configuration(transform=Transform(hflip=True, vflip=True)))
                cam0.start()

                cam0.set_controls({"AfMode":controls.AfModeEnum.Auto})
                cam0.set_controls({"AfRange":controls.AfRangeEnum.Macro})
                cam0.set_controls({"AfTrigger":controls.AfTriggerEnum.Start})
                time.sleep(0.7)
                cam0.capture_file(f"{folderName}/photo 1.png")
#                cam0.set_controls({"AfTrigger":controls.AfTriggerEnum.Cancel})
                cam0.close()

                cam1.configure(cam1.create_still_configuration(transform=Transform(hflip=True, vflip=True)))
                cam1.start()

                cam1.set_controls({"AfMode":controls.AfModeEnum.Auto})
                cam1.set_controls({"AfRange":controls.AfRangeEnum.Macro})
                cam1.set_controls({"AfTrigger":controls.AfTriggerEnum.Start})
                time.sleep(0.7)
                cam1.capture_file(f"{folderName}/photo 2.png")
#                cam1.set_controls({"AfTrigger":controls.AfTriggerEnum.Cancel})
                cam1.close()

                cam2.configure(cam2.create_still_configuration(transform=Transform(hflip=True, vflip=True)))
                cam2.start()

                cam2.set_controls({"AfMode":controls.AfModeEnum.Auto})
                cam2.set_controls({"AfRange":controls.AfRangeEnum.Macro})
                cam2.set_controls({"AfTrigger":controls.AfTriggerEnum.Start})
                time.sleep(0.7)
                cam2.capture_file(f"{folderName}/photo 3.png")
#                cam2.set_controls({"AfTrigger":controls.AfTriggerEnum.Cancel})
                cam2.close()

                cam3.configure(cam3.create_still_configuration(transform=Transform(hflip=True, vflip=True)))
                cam3.start()

                cam3.set_controls({"AfMode":controls.AfModeEnum.Auto})
                cam3.set_controls({"AfRange":controls.AfRangeEnum.Macro})
                cam3.set_controls({"AfTrigger":controls.AfTriggerEnum.Start})
                time.sleep(0.7)
                cam3.capture_file(f"{folderName}/photo 4.png")
#                cam3.set_controls({"AfTrigger":controls.AfTriggerEnum.Cancel})
                cam3.close()

        except FileExistsError:
                print("\nPlease wait before taking another photo.\n")

if __name__ == "__main__":

        cam0 = Picamera2(0)
        cam1 = Picamera2(1)
        cam2 = Picamera2(2)
        cam3 = Picamera2(3)

        start = time.time()

        try:
                capture()

        finally:
                process_timer('stop')
