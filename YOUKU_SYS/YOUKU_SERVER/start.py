
import sys,os
sys.path.append(
    os.path.dirname(__file__)         #将当前脚本所在的目录添加到 Python 的搜索路径中，以便导入同目录下的模块
)
from tcp_server import server
if __name__ == '__main__':
    server.run()