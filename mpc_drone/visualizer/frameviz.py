import matplotlib.pyplot as plt
import numpy as np

class FrameVisualization():

    def __init__(self, xlim = [0, 10], ylim = [0, 10], zlim = [0, 10], alpha_world_axis = 1) -> None:
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')

        self.setScale(xlim,ylim,zlim)
        origin = np.array([0.0,0.0,0.0])
        origin_axes = np.array([ [1.0 , 0.0, 0.0], 
                          [0.0 , 1.0, 0.0], 
                          [0.0 , 0.0, 1.0]])

        self.frames_for_transformation = {}
        self.frames_for_current_ref = {}
        
        self.frames_for_current_ref["World"] = [origin, origin_axes, alpha_world_axis]
        self.frames_for_transformation["World"] = [origin, origin_axes, alpha_world_axis]

        
        self.currentFrame = "World"

    ############################################################################################################################
    
    def addFrame(self, frameName, position, basisVectors, alpha = 1.0, overwrite = False):
        if not overwrite:
            if frameName in self.frames_for_transformation:
                print("Error, Frame with same Name Exists! If you want to overwrite, set overwriting to True while calling this method")
                return
        # Keep Track of transformations with respect to current reference frame
        self.frames_for_current_ref[frameName] = [position, basisVectors, alpha]

        # Keep Track of transformations with respect to World Frameransformation[frameName] 
        self.frames_for_transformation[frameName] = [position - self.frames_for_transformation[self.currentFrame][0], self.frames_for_transformation[self.currentFrame][1].T @ basisVectors, alpha]
        print(self.frames_for_transformation)


    def removeFrame(self,frameName):
        if frameName in self.frames_for_transformation:

            # Pop Frames 
            self.frames_for_current_ref.pop(frameName)
            self.frames_for_transformation.pop(frameName)

            return
        print("Error, Frame Not Found")

    def displayFrame(self, frameName, pauseTime = 0.0, clear = False):
        """
        Display given frame with respect to current reference frame.
        """
        if clear:
            self.ax.clear()
            self.setScale(self.xlim,self.ylim,self.zlim)

        if frameName in self.frames_for_current_ref:
            position = self.frames_for_current_ref[frameName][0]
            basisVectors = self.frames_for_current_ref[frameName][1]
            alpha = self.frames_for_current_ref[frameName][2]
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,0], basisVectors[1,0], basisVectors[2,0],color="red",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,1], basisVectors[1,1], basisVectors[2,1],color="green",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,2], basisVectors[1,2], basisVectors[2,2],color="blue",alpha = alpha)
            if pauseTime:
                plt.pause(pauseTime)
        else:
            print("Frame Does Not Exist")
    
    def displayAllFrames(self, pauseTime = 0.0):
        """
        Display All Frames with respect to current reference frame.
        """
        self.ax.clear()
        self.setScale(self.xlim,self.ylim,self.zlim)
        for frame in self.frames_for_current_ref:
            position = self.frames_for_current_ref[frame][0]
            basisVectors = self.frames_for_current_ref[frame][1]
            alpha = self.frames_for_current_ref[frame][2]
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,0], basisVectors[1,0], basisVectors[2,0],color="red",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,1], basisVectors[1,1], basisVectors[2,1],color="green",alpha = alpha)
            self.ax.quiver(position[0], position[1], position[2], basisVectors[0,2], basisVectors[1,2], basisVectors[2,2],color="blue",alpha = alpha)
        if pauseTime:
                plt.pause(pauseTime)
        else:
            plt.show()
    
    ############################################################################################################################
    
    def updateFramePosition(self, frameName, position):
        if frameName in self.frames_for_transformation:
            self.frames_for_current_ref[frameName][0] = position
            self.frames_for_transformation[frameName][0] = position - self.frames_for_transformation[self.currentFrame][0]

        else:
            print("Frame Does Not Exist")
    
    def updateBasisVectors(self, frameName, basisVectors):
        if frameName in self.frames_for_transformation:
            self.frames_for_current_ref[frameName][1] = basisVectors
            self.frames_for_transformation[frameName][1] = self.frames_for_transformation[self.currentFrame][1].T @ basisVectors
        else:
            print("Frame Does Not Exist")
    
    def updateAlpha(self, frameName, alpha):
        if frameName in self.frames_for_transformation:
            self.frames_for_current_ref[frameName][2] = alpha
            self.frames_for_transformation[frameName][2] = alpha

        else:
            print("Frame Does Not Exist")
    
    def updateFrame(self, frameName, position, basisVectors, alpha = -1):
        self.updateFramePosition(frameName, position)
        self.updateBasisVectors(frameName, basisVectors)
        if not alpha==-1:
            self.updateAlpha(frameName, alpha)


    def translateFrame(self, frameName, TransVec):
        if frameName in self.frames_for_current_ref:
            self.frames_for_current_ref[frameName][0] =+ TransVec
            self.frames_for_transformation[frameName][0] =+ (TransVec - self.frames_for_transformation[self.currentFrame][0])
        else:
            print("Frame Does Not Exist")
    
    def setRotX(self,frameName,angle):
        if frameName in self.frames_for_current_ref:
            self.frames_for_current_ref[frameName][1] = self.getRotX(angle) @ self.frames_for_current_ref[frameName][1]
            self.frames_for_transformation[frameName][1] = self.frames_for_transformation[self.currentFrame][1].T @ self.frames_for_current_ref[frameName][1]
        else:
            print("Frame Does Not Exist")
    
    def setRotY(self,frameName,angle):
        if frameName in self.frames_for_current_ref:
            self.frames_for_current_ref[frameName][1] = self.getRotY(angle) @ self.frames_for_current_ref[frameName][1]
            self.frames_for_transformation[frameName][1] = self.frames_for_transformation[self.currentFrame][1].T @ self.frames_for_current_ref[frameName][1]
        else:
            print("Frame Does Not Exist")
    
    def setRotZ(self,frameName,angle):
        if frameName in self.frames_for_current_ref:
            self.frames_for_current_ref[frameName][1] = self.getRotZ(angle) @ self.frames_for_current_ref[frameName][1]
            self.frames_for_transformation[frameName][1] = self.frames_for_transformation[self.currentFrame][1].T @ self.frames_for_current_ref[frameName][1]
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
        return list(self.frames_for_transformation.keys())
    
    
    def applyEulerRotation(self, frameName, alpha_angle, beta_angle, gamma_angle, order = "ZYX"):
        if frameName in self.frames_for_current_ref:
            rotationMat = self.getEulerRotMatrix(alpha_angle, beta_angle, gamma_angle, order)
            if rotationMat is None:
                return
            self.frames_for_current_ref[frameName][1] = rotationMat @ self.frames_for_current_ref[frameName][1]
            self.frames_for_transformation[frameName][1] = self.frames_for_transformation[self.currentFrame][1].T @ self.frames_for_current_ref[frameName][1]
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

    def changeFrame(self, frameName):
        if frameName in self.frames_for_transformation:
            self.currentFrame = frameName

            for frame in self.frames_for_transformation:
                self.frames_for_current_ref[frame] = [self.frames_for_transformation[frame][0] - self.frames_for_transformation[self.currentFrame][0],self.frames_for_transformation[self.currentFrame][1].T @ self.frames_for_transformation[frame][1],self.frames_for_transformation[frame][2]]
        else:
            print("Frame Does Not Exist")
        

    




