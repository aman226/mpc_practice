import matplotlib.pyplot as plt
import numpy as np

class FrameVisualization():

    def __init__(self, xlim = [0, 10], ylim = [0, 10], zlim = [0, 10], alpha_world_axis = 1) -> None:
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.frames = {}
        self.setScale(xlim,ylim,zlim)

        

        origin = np.array([0,0,0])
        origin_axes = np.array([ [1.0 , 0.0, 0.0], 
                                 [0.0 , 1.0, 0.0], 
                                 [0.0 , 0.0, 1.0]])
        
        self.addFrame("World", origin, origin_axes, alpha_world_axis)


    ############################################################################################################################
    
    def addFrame(self,frameName, position, basisVectors, alpha = 1.0, overwrite = False):
        if not overwrite:
            if frameName in self.frames:
                print("Error, Frame with same Name Exists! If you want to overwrite, set overwriting to True while calling this method")
                return
        self.frames[frameName] = [position, basisVectors, alpha]

    def removeFrame(self,frameName):
        if frameName in self.frames:
            self.frames.pop(frameName)
            return
        print("Error, Frame Not Found")

    def displayFrame(self, frameName, pauseTime = 0.0, clear = False):
        if clear:
            self.ax.clear()
            self.setScale(self.xlim,self.ylim,self.zlim)
        if frameName in self.frames:
            position = self.frames[frameName][0]
            basisVectors = self.frames[frameName][1]
            alpha = self.frames[frameName][2]
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,0], basisVectors[1,0], basisVectors[2,0],color="red",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,1], basisVectors[1,1], basisVectors[2,1],color="green",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,2], basisVectors[1,2], basisVectors[2,2],color="blue",alpha = alpha)
            if pauseTime:
                plt.pause(pauseTime)
        else:
            print("Frame Does Not Exist")
    
    def displayAllFrames(self, pauseTime = 0.0):
        self.ax.clear()
        self.setScale(self.xlim,self.ylim,self.zlim)
        for frame in self.frames:
            position = self.frames[frame][0]
            basisVectors = self.frames[frame][1]
            alpha = self.frames[frame][2]
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,0], basisVectors[1,0], basisVectors[2,0],color="red",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,1], basisVectors[1,1], basisVectors[2,1],color="green",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,2], basisVectors[1,2], basisVectors[2,2],color="blue",alpha = alpha)
        if pauseTime:
                plt.pause(pauseTime)
    
    ############################################################################################################################
    
    def updateFramePosition(self, frameName, Position):
        if frameName in self.frames:
            self.frames[frameName][0] = Position
        else:
            print("Frame Does Not Exist")
    
    def updateBasisVector(self, frameName, basisVectors):
        if frameName in self.frames:
            self.frames[frameName][1] = basisVectors
        else:
            print("Frame Does Not Exist")
    
    def updateAlpha(self, frameName, alpha):
        if frameName in self.frames:
            self.frames[frameName][2] = alpha
        else:
            print("Frame Does Not Exist")
    
    def updateFrame(self, frameName, Position, basisVectors, alpha = -1):
        self.updateFramePosition(frameName, Position)
        self.updateBasisVector(frameName, basisVectors)
        if not alpha==-1:
            self.updateAlpha(frameName, alpha)

    def translateFrame(self, frameName, TransVec):
        if frameName in self.frames:
            self.frames[frameName][0] =+ TransVec
        else:
            print("Frame Does Not Exist")
    
    def setRotX(self,frameName,angle):
        if frameName in self.frames:
            self.frames[frameName][1] = self.getRotX(angle) @ self.frames[frameName][1]
        else:
            print("Frame Does Not Exist")
    
    def setRotY(self,frameName,angle):
        if frameName in self.frames:
            self.frames[frameName][1] = self.getRotY(angle) @ self.frames[frameName][1] 
        else:
            print("Frame Does Not Exist")
    
    def setRotZ(self,frameName,angle):
        if frameName in self.frames:
            self.frames[frameName][1] = self.getRotZ(angle) @ self.frames[frameName][1]
        else:
            print("Frame Does Not Exist")
    
    def setScale(self,xlim,ylim,zlim):
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_zlim(zlim)
        self.xlim = xlim
        self.ylim = ylim
        self.zlim = zlim

    def getRotX(self,angle):
        return np.array([[1, 0, 0],
                         [0, np.cos(angle), -np.sin(angle)],
                         [0, np.sin(angle), np.cos(angle)]])

    def getRotY(self,angle):
        return np.array([[np.cos(angle), 0, np.sin(angle)],
                         [0, 1, 0],
                         [-np.sin(angle), 0, np.cos(angle)]])

    def getRotZ(self,angle):
        return np.array([[np.cos(angle), -np.sin(angle), 0],
                         [np.sin(angle), np.cos(angle), 0],
                         [0, 0, 1]])
    
    def getFrameNames(self):
        return list(self.frames.keys())
    
    def applyEulerRotation(self, frameName, alpha_angle, beta_angle, gamma_angle, order = "ZYX"):
        if frameName in self.frames:
            rotationMat = self.getEulerRotMatrix(alpha_angle, beta_angle, gamma_angle, order)
            if rotationMat is None:
                return
            self.frames[frameName][1] = rotationMat @ self.frames[frameName][1]
        else:
            print("Frame Does Not Exist")
    
    def getEulerRotMatrix(self,alpha_angle, beta_angle, gamma_angle, order):
        if order == "XYZ":
            rotationMat = self.getRotX(alpha_angle) @ self.getRotY(beta_angle) @ self.getRotZ(gamma_angle)

        elif order == "YZX":
            rotationMat = self.getRotY(alpha_angle) @ self.getRotZ(beta_angle) @ self.getRotX(gamma_angle)
        
        elif order == "ZXY":
            rotationMat = self.getRotZ(alpha_angle) @ self.getRotX(beta_angle) @ self.getRotY(gamma_angle)
        
        elif order == "ZYX":
            rotationMat = self.getRotZ(alpha_angle) @ self.getRotY(beta_angle) @ self.getRotX(gamma_angle)
        
        elif order == "YXZ":
            rotationMat = self.getRotY(alpha_angle) @ self.getRotX(beta_angle) @ self.getRotZ(gamma_angle)
        
        elif order == "XZY":
            rotationMat = self.getRotX(alpha_angle) @ self.getRotZ(beta_angle) @ self.getRotY(gamma_angle)

        elif order == "ZXZ":
            rotationMat = self.getRotZ(alpha_angle) @ self.getRotX(beta_angle) @ self.getRotZ(gamma_angle)
        
        elif order == "XYX":
            rotationMat = self.getRotX(alpha_angle) @ self.getRotY(beta_angle) @ self.getRotX(gamma_angle)
        
        elif order == "YZY":
            rotationMat = self.getRotY(alpha_angle) @ self.getRotZ(beta_angle) @ self.getRotY(gamma_angle)
        
        elif order == "ZYZ":
            rotationMat = self.getRotZ(alpha_angle) @ self.getRotY(beta_angle) @ self.getRotZ(gamma_angle)
        
        elif order == "XZX":
            rotationMat = self.getRotX(alpha_angle) @ self.getRotZ(beta_angle) @ self.getRotX(gamma_angle)
        
        elif order == "YXY":
            rotationMat = self.getRotY(alpha_angle) @ self.getRotX(beta_angle) @ self.getRotY(gamma_angle)

        else:
            print("Error! Wrong Rotation Order. Example of correct order XYZ ZYX ZYZ XYX etc.")
            rotationMat = None
        
        return rotationMat

        

    




