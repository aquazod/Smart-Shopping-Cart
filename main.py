import sys

import cv2
from ultralytics import YOLO
import numpy as np
import supervision as sv
import socket, re
import threading

#LINE_START = sv.Point(640, 240)
#LINE_END = sv.Point(0, 240)
LINE_START = sv.Point(1920, 540)
LINE_END = sv.Point(0, 540)

# class_Names = {0: 'Indomie', 1: 'CocaCola Can', 2: 'CocaCola Bottle 1 Litre', 3:'El-Arosa Tea', 4:'Halawa El-Bawady' , 5:'Juhayna Guava 1 Litre ' ,6:'Pepsi Can ' , 7:'Dasani Water' }


HOST = "0.0.0.0"
PORT = 80
SOC=0
current_weight=0
Monitor_Ok=1

weights_dict={"CocaCola Bottle 1 Litre":1435,"El-Arosa Tea":115, "Indomie":125 ,"CocaCola Can":330,"Halawa El-Bawady":580,"Juhayna Guava 1 Litre":1040,"Pepsi Can":335,"Dasani Water":580}

def Init_Weight_Monitor():
    global SOC
    try:
        SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOC.bind((HOST, PORT))
        SOC.listen()
    except Exception as e:
        print("[!] Error While Starting Socket error:(%s)"%str(e))


def Weight_Monitor_Thread():
    global SOC,current_weight,Monitor_Ok
    while Monitor_Ok==1:
        conn, addr = SOC.accept()
        data = conn.recv(256)
        w = re.findall(r'\?weight\=(.*)HTTP', str(data))
        current_weight = 0
        if ((len(w) > 0)):
            print(w[0])
            current_weight = float(w[0])*10
            print("W:", current_weight)
            conn.sendall(data)
        if Monitor_Ok==0 :
            sys.exit(1)



    conn.close()


def main():
    global current_weight
    # Init Weight Sensor
    Init_Weight_Monitor()


    MonitorThread = threading.Thread(target=Weight_Monitor_Thread, args=())
    MonitorThread.start()




    line_counter = sv.LineZone(start=LINE_START, end=LINE_END)
    line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )

    #model = YOLO("C:\\Users\\222at\\yolov7-main\\ultralytics-main\\ultralytics-main\\best2m.pt")

    model = YOLO("C:\\Users\\222at\\yolov7-main\\ultralytics-main\\ultralytics-main\\Yolov8l 120 epochs.pt")
    #model = YOLO("C:\\Users\\222at\\yolov7-main\\ultralytics-main\\ultralytics-main\\best3s.pt")
    #source="https://192.168.137.163:8080/video"
    # model = YOLO("C:\\Users\\222at\\yolov7-main\\ultralytics-main\\ultralytics-main\\bestooo.pt")
    # model = YOLO("C:\\Users\\222at\\yolov7-main\\ultralytics-main\\ultralytics-main\\best.pt")
    for result in model.track(source="https://192.168.43.1:8080/video", stream=True, agnostic_nms=True,conf=0.45 ,verbose=False ):




        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # detections = detections[(detections.class_id != 60) & (detections.class_id != 0)]

        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, tracker_id
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        line_counter.trigger(detections=detections, actual_w=current_weight)
        line_annotator.annotate(frame=frame, line_counter=line_counter)



        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            print("Monitor_Ok>>>> 0")
            Monitor_Ok=0
            break


    # qqqqprint(f" {in_list} $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ {out_list} ")


if __name__ == "__main__":
    main()
