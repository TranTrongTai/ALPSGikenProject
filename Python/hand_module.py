import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode= False, hands_to_track=2,
                    detection_confidence=0.5, tracking_confidence=0.5) -> None:
        self.mode = mode
        self.hands_to_track = hands_to_track
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(
                static_image_mode =self.mode,
                max_num_hands=self.hands_to_track,
                min_detection_confidence = self.detection_confidence,
                min_tracking_confidence  = self.tracking_confidence
        )

        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles 

        self.tips_ids =  [4, 8, 12, 16, 20] #5 đỉnh ngón tay
    def find_hands(self,img, draw=True):
        self.result = self.hands.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        if self.result.multi_hand_landmarks:
            if draw:
                for hand_landmark in self.result.multi_hand_landmarks:
                    self.mp_drawing_utils.draw_landmarks(
                                                        img,
                                                        hand_landmark,
                                                        self.mp_hand.HAND_CONNECTIONS,                            
                                                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                        self.mp_drawing_styles.get_default_hand_connections_style()
                                                        )

        return img

    def find_position(self, img, hand_index=0, draw =True):
        self.land_mank_list = []

        if self.result.multi_hand_landmarks:
            interest_hand = self.result.multi_hand_landmarks[hand_index]

            for id, landmark in enumerate(interest_hand.landmark):
                print(id, landmark)

                h,w,c = img.shape

                cx, cy = int(landmark.x*w),int(landmark.y*h)

                self.land_mank_list.append([id,cx,cy])
                # cv2.putText(img,str(id),(cx,cy), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)

                if draw:
                    cv2.circle(img,(cx,cy),10,(250,0,0),cv2.FILLED)
        return self.land_mank_list 

    def fingers_up(self):

        if len(self.land_mank_list) !=0:
            fingers_counter = []

            for tip_id in range(1,5):
                if self.land_mank_list[self.tips_ids[tip_id]][2] < self.land_mank_list[self.tips_ids[tip_id]-2][2]:
                    fingers_counter.append(1)

                else:
                    fingers_counter.append(0)
            if self.land_mank_list[self.tips_ids[0]][1] > self.land_mank_list[self.tips_ids[0]-1][1]:
                fingers_counter.append(1)
            else:
                fingers_counter.append(0)
            return fingers_counter

