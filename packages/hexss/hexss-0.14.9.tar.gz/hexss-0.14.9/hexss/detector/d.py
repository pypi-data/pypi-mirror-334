from roboflow import Roboflow
from hexss.python import write_proxy_to_env

write_proxy_to_env()

rf = Roboflow(api_key="uFO7gdp5R9CShcXysxCc")
project = rf.workspace("ek-j7xhr").project("segmentation-80cmx")
version = project.version(3)
dataset = version.download("yolov11")
