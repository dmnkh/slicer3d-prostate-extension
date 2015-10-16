import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *


class DataManager:
  
  layout = ("<layout type=\"vertical\" split=\"true\" >"
                  " <item>"
      "  <layout type=\"horizontal\">"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Main\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">R</property>"
      "   <property name=\"viewcolor\" action=\"default\">#F34A33</property>"
      "  </view>"
      " </item>"
      " <item>"
      "  <layout type=\"horizontal\">"
      " <item>"
      "  <layout type=\"vertical\">"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Coronal\">"
      "   <property name=\"orientation\" action=\"default\">Sagittal</property>"
      "   <property name=\"viewlabel\" action=\"default\">Y</property>"
      "   <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "  </view>"
      " </item>"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Sagittal\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">G</property>"
      "   <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "  </view>"
      " </item>"
      " </layout>"     
      " </item>"
      " </layout>"     
      " </item>"
      "</layout>"
      " </item>"
      " <item>"
      "  <layout type=\"horizontal\">"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Axial\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">Y</property>"
      "   <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "  </view>"
      " </item>"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Histology\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">G</property>"
      "   <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "  </view>"
      " </item>"
      " </layout>"     
      " </item>"
      "</layout>")
  
  def __init__(self):
    self.histo = None
    self.mri = None
    self.transformNode = None
    self.cameraNode = None
    self.positionSliderWidget = None
    self.orientationSliderWidget = None
    self.roiLabelMap = None
      
  def getHisto(self):
    return self.histo
  
  def getMRI(self):
    return self.mri
      
  def alignSlices(self):
    '''Aligns the Histology to the MRI slide.'''
    self.setLayout()
    if (not self.checkLoaded()):
      return
  
    volumeNodes = slicer.util.getNodes('*VolumeNode*').values()
    if (len(volumeNodes) == 0):
      return
  
    sliceNodes = slicer.util.getNodes('vtkMRMLSliceNode*').values()
    for node in sliceNodes:
      node.RotateToVolumePlane(volumeNodes[0])
  
#     for color in ['Red', 'Yellow', 'Green']:
#       slicer.app.layoutManager().sliceWidget(color).sliceLogic().GetSliceCompositeNode().SetForegroundVolumeID(self.histo.GetID())
#       slicer.app.layoutManager().sliceWidget(color).sliceLogic().GetSliceCompositeNode().SetForegroundOpacity(0.5)
#       slicer.app.layoutManager().sliceWidget(color).sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.mri.GetID())      
#       #slicer.app.layoutManager().sliceWidget(color).fitSliceToBackground()
#       slicer.app.layoutManager().sliceWidget(color).sliceLogic().FitSliceToAll()
      
    # Main view with both MRI and histology
    node = slicer.app.layoutManager().sliceWidget('Main').sliceLogic().GetSliceCompositeNode()
    
    node.SetForegroundVolumeID(self.histo.GetID())
    node.SetForegroundOpacity(0.5)
    node.SetBackgroundVolumeID(self.mri.GetID())      
    #slicer.app.layoutManager().sliceWidget(color).fitSliceToBackground()
    slicer.app.layoutManager().sliceWidget('Main').sliceLogic().FitSliceToAll()
#     newFOVx = node.GetFieldOfView()[0] * 0.7
#     newFOVy = node.GetFieldOfView()[1] * 0.7
#     newFOVz = node.GetFieldOfView()[2]
#     node = slicer.util.getNode('*SliceNodeRed*')
#     node.SetFieldOfView( newFOVx, newFOVy, newFOVz )
#     node.UpdateMatrices()      

    # MRI only view
    node = slicer.app.layoutManager().sliceWidget('Axial').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(None)
    node.SetBackgroundVolumeID(self.mri.GetID())
    slicer.app.layoutManager().sliceWidget('Axial').sliceLogic().FitSliceToAll()
    node = slicer.util.getNode('*SliceNodeAxial*')
    node.SetOrientationToAxial()
    node.RotateToVolumePlane(volumeNodes[0])
#     newFOVx = node.GetFieldOfView()[0] * 2
#     newFOVy = node.GetFieldOfView()[1] * 2
#     newFOVz = node.GetFieldOfView()[2]
#     node.SetFieldOfView( newFOVx, newFOVy, newFOVz )
#     node.UpdateMatrices()  
    
    # Histology only view
    node = slicer.app.layoutManager().sliceWidget('Histology').sliceLogic().GetSliceCompositeNode()
    node.SetBackgroundVolumeID(self.histo.GetID())
    node = slicer.util.getNode('*SliceNodeHistology*')
    node.SetOrientationToAxial()
    #slicer.app.layoutManager().sliceWidget('Histology').sliceLogic().FitSliceToAll()
    node.RotateToVolumePlane(volumeNodes[0])
    
    # Coronal view
    node = slicer.app.layoutManager().sliceWidget('Coronal').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(self.histo.GetID())
    node.SetBackgroundVolumeID(self.mri.GetID())
    node.SetForegroundOpacity(0.5)
    node = slicer.util.getNode('*SliceNodeCoronal*')
    node.SetOrientationToCoronal()
    slicer.app.layoutManager().sliceWidget('Coronal').sliceLogic().FitSliceToAll()
    node.RotateToVolumePlane(volumeNodes[0])    
    
    # Sagittal view
    node = slicer.app.layoutManager().sliceWidget('Sagittal').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(self.histo.GetID())
    node.SetBackgroundVolumeID(self.mri.GetID())
    node.SetForegroundOpacity(0.5)
    node = slicer.util.getNode('*SliceNodeSagittal*')
    node.SetOrientationToSagittal()
    slicer.app.layoutManager().sliceWidget('Sagittal').sliceLogic().FitSliceToAll()
    node.RotateToVolumePlane(volumeNodes[0])
    
    slicer.app.layoutManager().sliceWidget('Histology').fitSliceToBackground()
    mainNode = slicer.app.layoutManager().sliceWidget('Main').sliceLogic().GetSliceCompositeNode()
    histoOffset = slicer.app.layoutManager().sliceWidget('Histology').sliceLogic().GetSliceOffset()
    print(histoOffset)
    print(type(histoOffset))
    #slicer.app.layoutManager().sliceWidget('Main').sliceLogic().SetSliceOffset(histoOffset)
    node = slicer.util.getNode('*SliceNodeMain*')
    node.SetSliceOffset(float(histoOffset))
    node = slicer.util.getNode('*SliceNodeHistology*')
    node.SetSliceOffset(float(histoOffset))
    node = slicer.util.getNode('*SliceNodeAxial*')
    node.SetSliceOffset(float(histoOffset))

  def loadMRI(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.mri = slicer.util.getNode('*ScalarVolumeNode*')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
  
  def loadHistology(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.histo = slicer.util.getNode('*VectorVolumeNode*')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
  
  def setupTransform(self):
    self.cameraNode = slicer.util.getNode('*CameraNode*')
    self.transformNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLLinearTransformNode())
    self.mri.SetAndObserveTransformNodeID(self.transformNode.GetID())    
    self.positionSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))  
    self.orientationSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))  

  def setPositionSliderWidget(self, positionSliderWidget):
    self.positionSliderWidget = positionSliderWidget
          
  def setOrientationSliderWidget(self, orientationSliderWidget):
    self.orientationSliderWidget = orientationSliderWidget        
          
  def checkLoaded(self):
    '''Checks if both the Histology and MRI are loaded.'''
    if (self.mri is not None and self.histo is not None):
      return True
    else:
      return False
  
  def createROILabelMap(self):
    if self.roiLabelMap is None:
      self.roiLabelMap = slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.getMRI(), 'prostateLabelMap')

  def getROILabelMap(self):
    if self.roiLabelMap is not None:
      return self.roiLabelMap
  
  def applyTransformation(self):
    if (self.transformNode is not None):
      print('bla')
      logic = slicer.vtkSlicerTransformLogic()
      logic.hardenTransform(self.mri)
      
  def setLayout(self):
    layoutManager = slicer.app.layoutManager()
    self.customLayoutId = 502
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(self.customLayoutId, self.layout)                                         
    layoutManager.setLayout(self.customLayoutId)