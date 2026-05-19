from datetime import datetime
import time
from picamera2 import Picamera2
from libcamera import controls
import pathlib

USB_name = '/mnt/Lexar'

def get_time():
        
        now = datetime.now()
        return now.strftime("%b. %-d, %Y, %-I.%M.%S %p")
        
def process_timer(stage):
        if stage == 'stop':
                print(f'time elapsed: {time.time()-start} seconds.')
                
def capture():

        try:
                
                # create folder
                
                ftime = get_time()
                
                folderName = f"{USB_name}/Photos/'{ftime}'"
                pathlib.Path.mkdir(folderName)
                
                # take photos

                cam0.configure(cam0.create_still_configuration())
                
                cam0.start()
                cam0.capture_file(f"{folderName}/photo 1.jpeg")
                cam0.close()

                cam1.configure(cam1.create_still_configuration())
                
                cam1.start()
                cam1.capture_file(f"{folderName}/photo 2.jpeg")
                cam1.close()
                
                cam2.configure(cam2.create_still_configuration())
                
                cam2.start()
                cam2.capture_file(f"{folderName}/photo 3.jpeg")
                cam2.close()

                cam3.configure(cam3.create_still_configuration())
                
                cam3.start()
                cam3.capture_file(f"{folderName}/photo 4.jpeg")
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
