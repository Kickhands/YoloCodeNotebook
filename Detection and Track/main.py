import cv2
from ultralytics import YOLO
import cvzone

# Load YOLOv8 model
model = YOLO("best150.pt")
names = model.names

# X position of the vertical counting line
line_y = 550

# Store previous center positions for tracking
track_hist = {}

# Vehicle counters
car_in = 0
# car_out = 0
mtc_in = 0
# mtc_out = 0

# Open video file or webcam (use 0 for webcam)
cap = cv2.VideoCapture("1div4-videojalanraya4.mp4")

# Mouse callback function
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Mouse moved to: X={x}, Y={y}")

# Create a named a OpenCV window and set mouse callback
cv2.namedWindow("Track&Count")
cv2.setMouseCallback("Track&Count", RGB)
frame_counter = 0
while True:
    # Read video from frame
    ret, frame = cap.read()
    if not ret:
        break
    frame_counter += 1
    if frame_counter % 2 != 0:
        continue
    frame = cv2.resize(frame, (800, 600))

    # Detect and track class
    results = model.track(frame, persist=True, classes=[0,1])

    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        for box,track_id,class_id in zip(boxes,ids,class_ids):
            x1, y1, x2, y2 = box
            name=names[class_id]
            
            cx=int((x1+x2)/2)
            cy=int((y1+y2)/2)
            if track_id in track_hist:
                prev_cx, prev_cy = track_hist[track_id]
                if(prev_cy < line_y<=cy):
                    if 'car'in name:
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                        car_in += 1
                    if 'Motorcycle' in name:
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                        mtc_in += 1
                # elif(prev_cy > line_y>=cy):
                #     if 'car' in name:
                #         car_out += 1
                #     elif 'motorcycle' in name:
                #         mtc_out += 1
            
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(frame,(cx,cy),4,(255,0,0),-1)
            cvzone.putTextRect(frame,f'{name}',(x1,y1),scale=2,thickness=2,colorT=(255,255,255),colorR=(0,128,0))
            cvzone.putTextRect(frame,f'{track_id}',(x2,y2),scale=2,thickness=2,colorT=(255,255,255),colorR=(0,128,120))
            track_hist[track_id] = (cx, cy)


    
    cvzone.putTextRect(frame, f'car_in: {car_in}', (60, 40), scale=2, thickness=2,
                   colorT=(255, 255, 255), colorR=(0, 128, 0))
    # cvzone.putTextRect(frame, f'car_out: {car_out}', (640, 40), scale=2, thickness=2,
    #                colorT=(255, 255, 255), colorR=(0, 0, 120))
    cvzone.putTextRect(frame, f'mtc_in: {mtc_in}', (60, 90), scale=2, thickness=2,
                    colorT=(255, 255, 255), colorR=(120, 0, 120))
    # cvzone.putTextRect(frame, f'mtc_out: {mtc_out}', (640, 90), scale=2, thickness=2,
    #                 colorT=(255, 255, 255), colorR=(0, 120, 120))

    print(track_hist)
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 255, 255), 2)
    print(frame.shape)

    # Show the frame
    cv2.imshow("Track&Count", frame)
    print(track_hist)

    # Press 'Esc' to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break
