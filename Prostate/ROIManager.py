import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from DataManager import DataManager

class ROIManager():
    
  def __init__(self, dataManager):
    self.centralGlandLabelMap = None
    self.dataManager = dataManager
    self.labelMapValues = {'PROSTATE': 238, 'URETHRA': 227}

  def getLabelMapValue(self, value):
    return self.labelMapValues[value]

  def markProstate(self):
    self.__markBoundaries(self.getLabelMapValue('PROSTATE'))

  def markUrethra(self):
    self.__markBoundaries(self.getLabelMapValue('URETHRA'))

  def __markBoundaries(self, value):
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    self.dataManager.createROILabelMap()
    #lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.dataManager.getMRI().GetID())
    lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetLabelVolumeID(self.dataManager.getROILabelMap().GetID())
    paintEffectOptions = EditorLib.PaintEffectOptions()
    paintEffectOptions.setMRMLDefaults()
    paintEffectOptions.__del__()
    #slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.dataManager.getMRI(), 'prostateLabelMap')
    editUtil.setLabel(value)
    #self.delayDisplay('Paint radius is %s' % parameterNode.GetParameter('PaintEffect,radius'))
    sliceWidget = lm.sliceWidget('Red')
    size = min(sliceWidget.width,sliceWidget.height)
    step = size / 12
    center = size / 2
    parameterNode.SetParameter('PaintEffect,radius', '5')
    paintTool = EditorLib.PaintEffectTool(sliceWidget)
    
  def setMouseModeBack(self):
    interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
    interactionNode.SwitchToViewTransformMode()
    # also turn off place mode persistence if required
    interactionNode.SetPlaceModePersistence(0)