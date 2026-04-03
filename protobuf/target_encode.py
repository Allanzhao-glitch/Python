import TargetDetection_pb2
import time
import cv2
import os
import zmq
import numpy as np

def resize_with_padding(img, target_size=(1920, 1080), pad_color=(0, 0, 0)):
    """
    将图片等比例缩放，并填充至目标尺寸
    :param img: 输入图片 (numpy array)
    :param target_size: 目标尺寸 (width, height)
    :param pad_color: 填充颜色 (B, G, R)
    :return: 处理后的图片
    """
    target_w, target_h = target_size
    h, w = img.shape[:2]

    # 计算缩放比例（使图片完全适配目标尺寸）
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # 等比例缩放图片
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # 创建目标画布并填充背景色
    canvas = np.full((target_h, target_w, 3), pad_color, dtype=np.uint8)

    # 计算居中偏移量
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2

    # 将缩放后的图片放置到画布中央
    canvas[offset_y:offset_y + new_h, offset_x:offset_x + new_w] = resized_img

    return canvas




def serialize(detection_data, img_dir=r"./"):
    detection_event = TargetDetection_pb2.TargetDetection()  #创建一个detection检测事件
    detection_event.ImageName = detection_data["img_name"]
    detection_event.timestamp = int(detection_data["timestamp"])  #协议定义的int64
    detection_event.width = detection_data["width"]
    detection_event.height = detection_data["height"]

    for target in detection_data["targetList"]:
        target_event = detection_event.TargetList.add()  #列表添加一个target事件
        target_event.targetId = target['id']
        target_event.box.x1 = target['rect'][0]       #复合类型的赋值
        target_event.box.y1 = target['rect'][1]
        target_event.box.x2 = target['rect'][2]
        target_event.box.y2 = target['rect'][3]
        target_event.boxScore = target['score']
        target_event.labelType = target['type']                         
        img = cv2.imread(os.path.join(img_dir,detection_data["img_name"]))
        result_img = resize_with_padding(img, target_size=(1920, 1080), pad_color=(0, 0, 0))
        x1, y1, x2, y2 = target['rect']       
        imgbytes = cv2.imencode(".jpg", result_img[y1:y2, x1:x2, :])[1].tobytes()   #切割目标小图并转化为字节数据
        target_event.imageData = imgbytes
        target_event.imageType = "jpg"
        target_event.otherData = ""
    print(f"target_event: {target_event}")
    bytesdata = detection_event.SerializeToString()   #最后将整个事件序列化为字节
    return bytesdata


def send_via_zmq(bytesdata, port=5555):
    """通过 ZMQ 发送序列化数据"""
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://*:{port}")
    
    print(f"ZMQ 发送端已启动，监听端口 {port}...")
    print("正在发送数据...")
    
    import struct
    length = len(bytesdata)
    socket.send(struct.pack("!I", length))
    socket.send(bytesdata)
    
    print(f"发送成功! 数据大小: {length} bytes")
    
    time.sleep(1)
    socket.close()
    context.term()


if __name__ == "__main__":
    detection_data = {"img_name": "animal.jpg", "timestamp": "1615882332331", "width": 1920, "height": 1080,
                      "targetList": [{"id": 1, "rect": [150, 50, 960, 893], "score": 0.93, "type": "deer"},
                                      {"id": 2, "rect": [945, 40, 1820, 931], "score": 0.85, "type": "cat"}]}

    print("开始序列化...")
    bytesdata = serialize(detection_data)
    
    if bytesdata:
        print(f"序列化成功! 数据大小: {len(bytesdata)} bytes")
        send_via_zmq(bytesdata, port=5555)
    else:
        print("序列化失败!")