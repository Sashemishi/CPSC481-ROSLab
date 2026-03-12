import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ubuntu/Documents/ROS/CPSC481-ROSLab/install/hello_pkg'
