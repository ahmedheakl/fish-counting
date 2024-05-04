import json 
import requests
import cv2

url = "http://localhost:8000/fish_feeding"

to_collect = 6
collected = []
video_path = "object_counting.mp4"
cap = cv2.VideoCapture(video_path)

d = {"images": []}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if len(collected) == to_collect:
        d['images'] = d["images"][3:]
        data = requests.post(url, json=d).json()
        collected = []

        break
    
    collected.append(frame)
    d["images"].append(frame.tolist())

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

total_feed, times = data["total_feed"], data["times"]
print(f"Total feed: {total_feed}, Feed times: {times}")
