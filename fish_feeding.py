import torch
import numpy as np
from PIL import Image
from transformers import pipeline
from ultralytics import YOLO

class FishFeeding:
    
    def __init__(self, focal_length: float = 27.4) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.collected_lengths = []
        self.focal_length = focal_length
        self.final_weight = None
        self.length_model_name = "length_model.pt"
        self.depth_model_name = "vinvino02/glpn-nyu"
        self.counting_model_name = "counting_model.pt"

    def load_models(self) -> None:
        self.fish_keypoints_model = YOLO(self.length_model_name)
        self.depth_model = pipeline(task="depth-estimation", model=self.depth_model_name, device=self.device)
        self.fish_detection_model = YOLO(self.counting_model_name)

    def predict_fish_length(self, frame):
        image_obj = Image.fromarray(frame)
        image_obj = image_obj.resize((640, 640))  # Adjust size as per requirement
        depth = self.depth_model(image_obj)
        depth = depth["predicted_depth"]
        depth = np.array(depth).squeeze()

        results = self.fish_detection_model(frame)[0]
        keypoints = results.keypoints.xyn[0].detach().cpu().numpy()
        head = keypoints[0]
        back = keypoints[1]
        belly = keypoints[2]
        tail = keypoints[3]

        depth_w, depth_h = depth.shape[:2]

        head_x = int(head[0] * depth_w)
        head_y = int(head[1] * depth_h)
        tail_x = int(tail[0] * depth_w)
        tail_y = int(tail[1] * depth_h)

        back_x = int(back[0] * depth_w)
        back_y = int(back[1] * depth_h)
        belly_x = int(belly[0] * depth_w)
        belly_y = int(belly[1] * depth_h)

        head_depth = depth[head_y, head_x]
        tail_depth = depth[tail_y, tail_x]

        fish_length = (
            np.sqrt(
                (head_x * head_depth - tail_x * tail_depth) ** 2
                + (head_y * head_depth - tail_y * tail_depth) ** 2
            )
            / self.focal_length
        )
        # girth = (
        #     np.sqrt(
        #         (back_x * head_depth - belly_x * tail_depth) ** 2
        #         + (back_y * head_depth - belly_y * tail_depth) ** 2
        #     )
        #     / self.focal_length
        # )
        return fish_length

    # def videocapture(self):
    #     cap = cv2.VideoCapture(self.video_path)
    #     assert cap.isOpened(), "Error reading video file"
    #     while True:
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
    #         output = self.predict_fish_length(frame)
    #         self.collected_lengths.append(output)
    #     cap.release()
    #     return self.collected_lengths

    def get_average_weight(self):
        if not self.collected_lengths:
            return 0 
        length_average = sum(self.collected_lengths) / len(self.collected_lengths)
        final_weight = 0.014 * length_average ** 3.02
        return final_weight

    def fish_counting(self, images):
        counting_output = 0
        for im0 in images:
            tracks = self.fish_detection_model(im0)
            counting_output = max(counting_output, len(tracks))
        
        return counting_output

    def final_fish_feed(self, images: list):
        for image in images:
            output = self.predict_fish_length(image)
            self.collected_lengths.append(output)

        average_weight = self.get_average_weight()
        if 0 <= average_weight <= 50:
            feed, times = 3.3, 2
        elif 50 < average_weight <= 100:
            feed, times = 4.8, 2
        elif 100 < average_weight <= 250:
            feed, times = 5.8, 2
        elif 250 < average_weight <= 500:
            feed, times = 8.4, 2
        elif 500 < average_weight <= 750:
            feed, times = 9.4, 1
        elif 750 < average_weight <= 1000:
            feed, times = 10.5, 1
        elif 1000 < average_weight <= 1500:
            feed, times = 11.0, 1
        else: 
            feed, times = 12.0, 1

        fish_count = self.fish_counting(images)
        total_feed = feed * fish_count
        return total_feed, times


# if __name__ == "__main__":
#     to_collect = 6
#     collected = []
#     video_path = "object_counting.mp4"
#     cap = cv2.VideoCapture(video_path)

#     fish_feeding = FishFeeding()
#     fish_feeding.load_models()

#     d = {"images": []}

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if len(collected) == to_collect:
#             total_feed, times = fish_feeding.final_fish_feed(collected)
#             print(f"Total feed: {total_feed}, Feed times: {times}")
#             collected = []

#             break
        
#         collected.append(frame)
#         d["images"].append(frame.tolist())

#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     # save d to json file
#     import json
#     with open("data.json", "w") as f:
#         json.dump(d, f)

