import PIL
import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
from core.yolov3 import YOLOv3, decode
from PIL import Image

word_dict={'자전거':'bicycle',
            '배':'boat',
            '다리':'bridge',
            '버스':'bus',
            '자동차':'car',
            '굴뚝':'chimney',
            '횡단보도':'crosswalk',
            '소화전':'fire hydrant',
            '오토바이':'motorcycle',
            '산':'mountain',
            '야자수':'palm',
            '계단':'stairs',
            '택시':'taxi',
            '트럭':'truck',
            '신호등':'traffic Light',
            '표지판':'traffic Sign',
            }

# Obect Dection 및 Image Division 에 사용할 클래스
class Image_detection():
    def __init__(self,keyword):
        self.keyword=word_dict[keyword]
        self.date=None

    def set_date(self,date):
        self.date=date

    def yoloV3(self,address):
        img=Image.open(address)
        input_size = img.size[0]
        image_path = address

        input_layer = tf.keras.layers.Input([input_size, input_size, 3])
        feature_maps = YOLOv3(input_layer)

        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        original_image_size = original_image.shape[:2]

        image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        bbox_tensors = []
        for i, fm in enumerate(feature_maps):
            bbox_tensor = decode(fm, i)
            bbox_tensors.append(bbox_tensor)

        model = tf.keras.Model(input_layer, bbox_tensors)
        utils.load_weights(model, "./yolov3.weights")
        model.summary()

        pred_bbox = model.predict(image_data)
        pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
        pred_bbox = tf.concat(pred_bbox, axis=0)
        bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
        bboxes = utils.nms(bboxes, 0.45, method='nms')

        # 이미지 그리드 분할
        (img_h, img_w)=img.size
        grid_h,grid_w=100,100

        range_h,range_w=(int)(img_h/grid_h),(int)(img_w/grid_w)

        image_grid=list()
        i=0
        for w in range(range_w):
            for h in range(range_h):
                image_grid.append(((h*grid_h, w*grid_w), ((h+1)*(grid_h), (w+1)*(grid_w))))

        image,keyword_sector= utils.draw_bbox(original_image, bboxes, self.keyword)
        image = Image.fromarray(image)
        #image.show()

        # 키워드 그리드 찾기
        keyword_idx=utils.find_idx(image_grid,keyword_sector,range_h)

        address_after="./captcha_image/AFTER_YOLO_{}.jpg".format(self.date)
        image=np.array(image)
        cv2.imwrite(address_after, image)

        return keyword_idx
