from datetime import timedelta
import json 
import numpy as np 

class NpEncoder(json.JSONEncoder):
    '''
    numpy to json format
    '''

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def sec_to_format(td):
    td = timedelta(seconds=round((td) * 10))
    total_seconds = td.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print(f"ETA : {int(hours)}:{int(minutes)}:{int(seconds)}")

def createML_to_coco(bboxes, dim=2):
    '''
     createML format : [x_c , y_c , w ,h]
    coco format : [x1 , y1 , w, h]
    '''
    if dim == 1:
        x_c, y_c, w, h = bboxes
        anno = [x_c - (w // 2), y_c - (h // 2),  w, h]
    else:
        anno = [[x_c - (w // 2), y_c - (h // 2),  w, h]
                for x_c, y_c, w, h in bboxes]
    return anno


def coco_to_cv2(bboxes, dim=2):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    '''
    coco format : [x1,y1, w,h] float or int
    cv2 format : [x1,y1,x2,y2] int
    '''
    if dim == 1:
        x1, y1, w, h = list(map(int, bboxes))
        anno = [x1, y1, x1 + w, y1 + h]
    else:
        anno = [list(map(int, [x1, y1, x1 + w, y1 + h]))
                for x1, y1, w, h in bboxes]
    return anno


def cv2_to_coco(bboxes, dim=2):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    '''
    cv2 format : [x1,y1,x2,y2] int
    coco format : [x1,y1, w,h] float or int
    '''
    if dim == 1:
        x1, y1, x2, y2 = list(map(int, bboxes))
        anno = [x1, y1, x2-x1, y2-y1]
    else:
        anno = [list(map(int, [x1, y1, x2-x1, y2-y1]))
                for x1, y1, x2, y2 in bboxes]
    return anno

def get_area(bbox , dim=2 , dtype = 'cv2'):
    x1, y1 , x2 ,y2 = bbox
    return int((x2-x1) * (y2-y1))

