import matplotlib.pyplot as plt
#from gz.math7 import Quaterniond
#from gz import Pose3 
class MatplotlibVisualizer():
    def __init__(self) -> None:
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([0,20]) 

    def appendPosition(self,position):
        self.ax.plot3D(position[0],position[1],-position[2],'bo')
        plt.pause(0.01)

# class GazeboVisualizer():
#     def __init__(self) -> None:
#         a = Quaterniond(0.1,0.5,0.7)
#         print(a.w())
#         pass


# a  = GazeboVisualizer()