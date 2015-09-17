import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from DataManager import DataManager
 
class LandmarkManager():
    
    layout = ("<layout type=\"vertical\" split=\"true\" >"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Red\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">R</property>"
      "   <property name=\"viewcolor\" action=\"default\">#F34A33</property>"
      "  </view>"
      " </item>"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Yellow\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">Y</property>"
      "   <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "  </view>"
      " </item>"
      "</layout>")
    
    def __init__(self, dataManager):
      self.dataManager = dataManager
    
    def __setMouseModeToFiducial(self):
      placeModePersistence = 1
      slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
    
    def setMouseModeBack(self):
      interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
      interactionNode.SwitchToViewTransformMode()
      # also turn off place mode persistence if required
      interactionNode.SetPlaceModePersistence(0)
    
    def createFiducialMap(self, name):
      if slicer.util.getNode(name) is None:
        fiducial = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsFiducialNode())
        fiducial.SetName(name)
                
    def setLandmarksForMRI(self):
      self.createFiducialMap('MRI')
      self.__setMouseModeToFiducial()
      
    def setLandmarksForHisto(self):
      self.createFiducialMap('Histo')
      self.__setMouseModeToFiducial()
      
    def getFiducialList(self, name):
       fidList = slicer.util.getNode(name)
       numFids = fidList.GetNumberOfFiducials()
       for i in range(numFids):
        ras = [0,0,0]
        fidList.GetNthFiducialPosition(i,ras)
        # the world position is the RAS position with any transform matrices applied
        world = [0,0,0,0]
        fidList.GetNthFiducialWorldCoordinates(0,world)
        print i,": RAS =",ras,", world =",world
        
    def setLayout(self):
        layoutManager = slicer.app.layoutManager()
        self.customLayoutId = 501
        layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(self.customLayoutId, self.layout)                                         
        layoutManager.setLayout(self.customLayoutId)