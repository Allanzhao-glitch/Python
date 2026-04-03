import TargetDetection_pb2
import time
import cv2
import os
import zmq
import struct


def deserialize(bytesdata):
    """反序列化 protobuf 数据"""
    detection_event = TargetDetection_pb2.TargetDetection()
    detection_event.ParseFromString(bytesdata)
    
    print("=" * 50)
    print("反序列化结果:")
    print("=" * 50)
    print(f"图片名称: {detection_event.ImageName}")
    print(f"时间戳: {detection_event.timestamp}")
    print(f"图片尺寸: {detection_event.width} x {detection_event.height}")
    print(f"目标数量: {len(detection_event.TargetList)}")
    print("-" * 50)
    
    for i, target_event in enumerate(detection_event.TargetList):
        print(f"\n目标 {i+1}:")
        print(f"  ID: {target_event.targetId}")
        print(f"  类型: {target_event.labelType}")
        print(f"  置信度: {target_event.boxScore}")
        print(f"  框坐标: ({target_event.box.x1}, {target_event.box.y1}, {target_event.box.x2}, {target_event.box.y2})")
        print(f"  图片类型: {target_event.imageType}")
        print(f"  图片数据大小: {len(target_event.imageData)} bytes")
        
        # 可选：将图片数据保存为文件
        # if target_event.imageData:
        #     img_array = np.frombuffer(target_event.imageData, dtype=np.uint8)
        #     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        #     cv2.imwrite(f"target_{target_event.targetId}.jpg", img)
    
    print("=" * 50)
    return detection_event


def receive_via_zmq(port=5555):
    """通过 ZMQ 接收序列化数据"""
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(f"tcp://localhost:{port}")
    
    print(f"ZMQ 接收端已启动，连接端口 {port}...")
    print("等待数据...")
    
    # 先接收数据长度
    length_data = socket.recv()
    length = struct.unpack("!I", length_data)[0]
    print(f"即将接收数据长度: {length} bytes")
    
    # 接收实际数据
    bytesdata = socket.recv()
    print(f"接收完成! 实际数据大小: {len(bytesdata)} bytes")
    
    socket.close()
    context.term()
    
    return bytesdata


if __name__ == "__main__":
    # 接收数据
    bytesdata = receive_via_zmq(port=5555)
    
    # 反序列化
    if bytesdata:
        deserialize(bytesdata)
    else:
        print("接收失败!")