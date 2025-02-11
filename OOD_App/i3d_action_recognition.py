
from tensorflow.keras.models import Sequential,load_model
import numpy as np
import cv2,os
from collections import Counter
from tensorflow.keras.optimizers import legacy

from tensorflow.keras.losses import *
import tensorflow as tf
from tensorflow.keras.losses import *
from tensorflow.keras.layers import *

class I3DModel:
    def __init__(self):
        optimizer = legacy.Adam()
        self.classes=['ApplyEyeMakeup', 'ApplyLipstick', 'Archery', 'BabyCrawling', 'BalanceBeam', 'BandMarching', 'BaseballPitch', 'Basketball', 'BasketballDunk', 'BenchPress', 'Biking', 'Billiards', 'BlowDryHair', 'BlowingCandles', 'BodyWeightSquats', 'Bowling', 'BoxingPunchingBag', 'BoxingSpeedBag', 'BreastStroke', 'BrushingTeeth', 'CleanAndJerk', 'CliffDiving', 'CricketBowling', 'CricketShot', 'CuttingInKitchen', 'Diving', 'Drumming', 'Fencing', 'FieldHockeyPenalty', 'FloorGymnastics', 'FrisbeeCatch', 'FrontCrawl', 'GolfSwing', 'Haircut', 'Hammering', 'HammerThrow', 'HandstandPushups', 'HandstandWalking', 'HeadMassage', 'HighJump', 'HorseRace', 'HorseRiding', 'HulaHoop', 'IceDancing', 'JavelinThrow', 'JugglingBalls', 'JumpingJack', 'JumpRope', 'Kayaking', 'Knitting', 'LongJump', 'Lunges', 'MilitaryParade', 'Mixing', 'MoppingFloor', 'Nunchucks', 'ParallelBars', 'PizzaTossing', 'PlayingCello', 'PlayingDaf', 'PlayingDhol', 'PlayingFlute', 'PlayingGuitar', 'PlayingPiano', 'PlayingSitar', 'PlayingTabla', 'PlayingViolin', 'PoleVault', 'PommelHorse', 'PullUps', 'Punch', 'PushUps', 'Rafting', 'RockClimbingIndoor', 'RopeClimbing', 'Rowing', 'SalsaSpin', 'ShavingBeard', 'Shotput', 'SkateBoarding', 'Skiing', 'Skijet', 'SkyDiving', 'SoccerJuggling', 'SoccerPenalty', 'StillRings', 'SumoWrestling', 'Surfing', 'Swing', 'TableTennisShot']
        self.model = Sequential()
        self.model.add(Dense(len(self.classes), activation = 'softmax',input_shape=(2048,)))

        ########################################################################################################################
        self.model.load_weights('cross_plus_kl')
        self.model.compile(optimizer = optimizer,loss =self.custom_loss_function, metrics = ["accuracy"])

    def custom_loss_function(self,y_true, y_pred):
        cce=CategoricalCrossentropy()
        kl=KLDivergence()

        cross=cce(y_true, y_pred)
        test=tf.fill(tf.shape(y_true),1/90)
        kl_d=kl(test,y_pred)
        loss=cross+kl_d
        return loss
    


    def recognize(self,video_features,video_file_path,output_file_path):

        index=0
        i3d_time=2.56

        
        predictions=self.model.predict(video_features)
        
        video_reader = cv2.VideoCapture(video_file_path)
        original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        video_writer = cv2.VideoWriter(output_file_path, fourcc, 
                                    video_reader.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))
        fps = video_reader.get(cv2.CAP_PROP_FPS)
        actions_dict={}
        actions=[]
        without_unseen={}
        probs_dict=[]
        index+=1
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        thickness = 2
        text_color = (255, 255, 255)
        while video_reader.isOpened():
            ok, frame = video_reader.read() 
            if not ok:
                break
            time_of_frame=round(video_reader.get(cv2.CAP_PROP_POS_MSEC))/1000
            try:
                val=np.argmax(predictions[index])
                if np.max(predictions[index])>=0.10:
                    text=self.classes[val]
                    actions.append(text)
                    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                    rectangle_bgr = (0, 0, 0)
                    rectangle_position = (10, 30)
                    rectangle_size = (text_width, text_height + 5)
                    cv2.rectangle(frame, (0,10), (rectangle_position[0] + rectangle_size[0], rectangle_position[1] + rectangle_size[1]), rectangle_bgr, cv2.FILLED)
                    cv2.putText(frame, text, rectangle_position, font, font_scale, text_color, thickness)
                    
                else:
                    text='Unseen'
                    actions.append(text)
                    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                    rectangle_bgr = (0, 0, 0)
                    rectangle_position = (10, 30)
                    rectangle_size = (text_width, text_height + 5)
                    cv2.rectangle(frame, (0,10), (rectangle_position[0] + rectangle_size[0], rectangle_position[1] + rectangle_size[1]), rectangle_bgr, cv2.FILLED)
                    cv2.putText(frame, text, rectangle_position, font, font_scale, text_color, thickness)
                    
                if self.classes[val] not in without_unseen:
                    without_unseen[self.classes[val]]=[]
                without_unseen[self.classes[val]].append(np.max(predictions[index]))
            except:
                pass
            if time_of_frame>=i3d_time:
                word_counts = Counter(actions)
                try:
                    most_common_action = word_counts.most_common(1)[0][0]
                    actions_dict[round(i3d_time-2.56, 2)]=most_common_action
                    max_key = max(without_unseen, key=lambda k: len(without_unseen[k]))
                    probs_dict.append(f"{max_key},{round(sum(without_unseen[max_key])/len(without_unseen[max_key]),3)}")
                except:
                    print("Size is less")
                actions.clear()
                without_unseen.clear()
                i3d_time+=2.56
                index+=1
            video_writer.write(frame)
        video_reader.release()
        video_writer.release()
        return actions_dict,probs_dict
    
    # def clear_gpu_memory(self):
    #     self.model.reset_states()
    #     tf.keras.backend.clear_session()
    #     gpus = tf.config.experimental.list_physical_devices('GPU')
    #     if gpus:
    #         for gpu in gpus:
    #             tf.config.experimental.set_memory_growth(gpu, True)
        