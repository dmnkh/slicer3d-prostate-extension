import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

import SimpleITK as sitk
import sitkUtils

#
# Prostate
#

class Prostate(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Prostate MRI/Histology Registration"  # TODO make this more human readable by adding spaces
    self.parent.categories = ["Registration"]
    self.parent.dependencies = []
    self.parent.contributors = ["Dominik Hofer", "Matthew DiFranco"]  # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This module facilitates registration of prostate histology slices to MRI volumes.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Dominik Hofer and Matthew DiFranco, Phd.
"""  # replace with organization, grant and thanks.

#
# ProstateWidget
#

class ProstateWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
  def __init__(self, parent=None):
    ScriptedLoadableModuleWidget.__init__(self, parent)
    self.logic = ProstateLogic()
    self.layoutManager = slicer.app.layoutManager()
    self.markupsLogic = slicer.modules.markups.logic()
    self.volumesLogic = slicer.modules.volumes.logic()
    #self.modulePath = slicer.modules.slicetracker.path.replace(self.moduleName + ".py", "")
    #self.iconPath = os.path.join(self.modulePath, 'Resources/Icons')

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    # Instantiate and connect widgets ...

#     #
#     # Parameters Area
#     #
#     parametersCollapsibleButton = ctk.ctkCollapsibleButton()
#     parametersCollapsibleButton.text = "Parameters"
#     self.layout.addWidget(parametersCollapsibleButton)
# 
#     # Layout within the dummy collapsible button
#     parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)
# 
#     #
#     # input volume selector
#     #
#     self.inputSelector = slicer.qMRMLNodeComboBox()
#     self.inputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
#     self.inputSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
#     self.inputSelector.selectNodeUponCreation = True
#     self.inputSelector.addEnabled = False
#     self.inputSelector.removeEnabled = False
#     self.inputSelector.noneEnabled = False
#     self.inputSelector.showHidden = False
#     self.inputSelector.showChildNodeTypes = False
#     self.inputSelector.setMRMLScene(slicer.mrmlScene)
#     self.inputSelector.setToolTip("Pick the input to the algorithm.")
#     parametersFormLayout.addRow("Input Volume: ", self.inputSelector)
# 
#     #
#     # output volume selector
#     #
#     self.outputSelector = slicer.qMRMLNodeComboBox()
#     self.outputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
#     self.outputSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
#     self.outputSelector.selectNodeUponCreation = False
#     self.outputSelector.addEnabled = True
#     self.outputSelector.removeEnabled = True
#     self.outputSelector.noneEnabled = False
#     self.outputSelector.showHidden = False
#     self.outputSelector.showChildNodeTypes = False
#     self.outputSelector.setMRMLScene(slicer.mrmlScene)
#     self.outputSelector.setToolTip("Pick the output to the algorithm.")
#     parametersFormLayout.addRow("Output Volume: ", self.outputSelector)
# 
#     #
#     # check box to trigger taking screen shots for later use in tutorials
#     #
#     self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
#     self.enableScreenshotsFlagCheckBox.checked = 0
#     self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
#     parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)
# 
#     #
#     # scale factor for screen shots
#     #
#     self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
#     self.screenshotScaleFactorSliderWidget.singleStep = 1.0
#     self.screenshotScaleFactorSliderWidget.minimum = 1.0
#     self.screenshotScaleFactorSliderWidget.maximum = 50.0
#     self.screenshotScaleFactorSliderWidget.value = 1.0
#     self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
#     parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)
# 
#     #
#     # Apply Button
#     #
#     self.applyButton = qt.QPushButton("Apply")
#     self.applyButton.toolTip = "Run the algorithm."
#     self.applyButton.enabled = False
#     parametersFormLayout.addRow(self.applyButton)
# 
#     # connections
#     self.applyButton.connect('clicked(bool)', self.onApplyButton)
#     self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
#     self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    # self.layout.addStretch(1)
	
# 	#
# 	# Load Data
# 	#
#     dm = DataManager()
#     loadDataCollapsibleButton = ctk.ctkCollapsibleButton()
#     loadDataCollapsibleButton.text = "Load Data"
#     self.layout.addWidget(loadDataCollapsibleButton)
#     loadDataFormLayout = qt.QFormLayout(loadDataCollapsibleButton)
# 	
# 	# Load MRI Button
# 	
#     self.loadMRIButton = qt.QPushButton("Load MRI")
#     self.loadMRIButton.toolTip = "Load the MRI File."
#     self.loadMRIButton.name = "LoadMRI"
#     loadDataFormLayout.addWidget(self.loadMRIButton)
#     self.loadMRIButton.connect('clicked()', self.logic.loadMRIVolume)
# 
# 	# Load Histology Button
# 	
#     self.loadHistologyButton = qt.QPushButton("Load Histology")
#     self.loadHistologyButton.toolTip = "Load the Histology File."
#     self.loadHistologyButton.name = "LoadHistology"
#     loadDataFormLayout.addWidget(self.loadHistologyButton)
#     self.loadHistologyButton.connect('clicked()', self.logic.loadHistologyVolume)
# 	
#     '''lm = slicer.app.layoutManager()
#     red = lm.sliceWidget('Red')
#     redLogic = red.sliceLogic()
#     # Print current slice offset position
#     print redLogic.GetSliceOffset()
#     # Change slice position
#     redLogic.SetSliceOffset(20)'''
#     self.alignButton = qt.QPushButton("Align Volumes")
#     self.alignButton.toolTip = "Rotate to Volume Plane."
#     self.alignButton.name = "AlignVolumes"
#     loadDataFormLayout.addWidget(self.alignButton)
#     self.alignButton.connect('clicked()', self.logic.alignSlices)	
#     
#     self.positionSliderWidget = slicer.qMRMLTransformSliders()
#     self.positionSliderWidget.Title = 'Position'
#     self.positionSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.TRANSLATION
#     self.positionSliderWidget.CoordinateReference = slicer.qMRMLTransformSliders.LOCAL
#     self.positionSliderWidget.setMRMLScene(slicer.mrmlScene)
#     self.logic.setPositionSliderWidget(self.positionSliderWidget)
#     #self.positionSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))
#     loadDataFormLayout.addRow("Translation", self.positionSliderWidget)    
#     
#     self.orientationSliderWidget = slicer.qMRMLTransformSliders()
#     self.orientationSliderWidget.Title = 'Orientation'
#     self.orientationSliderWidget.setMRMLScene(slicer.mrmlScene)
#     # Setting of qMRMLTransformSliders.TypeOfTransform is not robust: it has to be set after setMRMLScene and
#     # has to be set twice (with setting the type to something else in between).
#     # Therefore the following 3 lines are needed, and they are needed here:
#     self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.ROTATION
#     self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.TRANSLATION
#     self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.ROTATION
#     self.orientationSliderWidget.CoordinateReference=slicer.qMRMLTransformSliders.LOCAL
#     self.orientationSliderWidget.minMaxVisible = False
#     self.logic.setOrientationSliderWidget(self.orientationSliderWidget)
#     #self.orientationSliderWidget.setMRMLTransformNode(self.getPivotToRasTransformNode())
#     loadDataFormLayout.addRow("Orientation", self.orientationSliderWidget)
#     
#     self.applyTransformButton = qt.QPushButton("Apply")
#     self.applyTransformButton.toolTip = "Saves the positioning of the histology slice."
#     self.applyTransformButton.name = "ApplyTransform"
#     loadDataFormLayout.addWidget(self.applyTransformButton)
#     self.applyTransformButton.connect('clicked()', self.logic.applyTransformation)
#     
# 	#
# 	# Bounding Box
# 	#
# 	
#     boundingBoxCollapsibleButton = ctk.ctkCollapsibleButton()
#     boundingBoxCollapsibleButton.text = "Mark Extents"
#     self.layout.addWidget(boundingBoxCollapsibleButton)
#     boundingBoxFormLayout = qt.QFormLayout(boundingBoxCollapsibleButton)
# 	
# 	#
# 	# ROI definition
# 	#
# 	
#     roiDefintitionCollapsibleButton = ctk.ctkCollapsibleButton()
#     roiDefintitionCollapsibleButton.text = "ROI definition"
#     self.layout.addWidget(roiDefintitionCollapsibleButton)
#     roiDefintitionFormLayout = qt.QFormLayout(roiDefintitionCollapsibleButton)
#     roiManager = ROIManager(dm)
#     
#     # Mark Prostate Button
#     
#     self.markProstateButton = qt.QPushButton("Mark Prostate")
#     self.markProstateButton.toolTip = "Mark the boundaries of the prostate."
#     self.markProstateButton.name = "MarkProstate"
#     roiDefintitionFormLayout.addWidget(self.markProstateButton)
#     self.markProstateButton.connect('clicked()', self.logic.markBoundaries)
# 
#     # Mark Urethra Button
#     
#     self.markUrethraButton = qt.QPushButton("Mark Urethra")
#     self.markUrethraButton.toolTip = "Mark the boundaries of the urethra."
#     self.markUrethraButton.name = "MarkUrethra"
#     roiDefintitionFormLayout.addWidget(self.markUrethraButton)
#     self.markUrethraButton.connect('clicked()', roiManager.markUrethra)
# 	
#     # Finished Marking Button
#     
#     self.finishedMarkingButton = qt.QPushButton("Finished Marking")
#     self.finishedMarkingButton.toolTip = "Finished Marking"
#     self.finishedMarkingButton.name = "FinishedMarking"
#     roiDefintitionFormLayout.addWidget(self.finishedMarkingButton)
#     self.finishedMarkingButton.connect('clicked()', self.logic.setMouseModeBack)
#     
#     # 
#     
#     #
#     # PET/MR alignment
# 	#
# 	
#     petMRIAlignmentCollapsibleButton = ctk.ctkCollapsibleButton()
#     petMRIAlignmentCollapsibleButton.text = "PET/MR alignment"
#     self.layout.addWidget(petMRIAlignmentCollapsibleButton)
#     petMRAlignmentFormLayout = qt.QFormLayout(petMRIAlignmentCollapsibleButton)
# 	
#     #
#     # Landmarking on histology and PET/MR
# 	#
# 	
#     landmarksCollapsibleButton = ctk.ctkCollapsibleButton()
#     landmarksCollapsibleButton.text = "Set Landmarks"
#     self.layout.addWidget(landmarksCollapsibleButton)
#     landmarksFormLayout = qt.QFormLayout(landmarksCollapsibleButton)
#     landmarkManager = LandmarkManager(dm)
#     
#     # Set MRI Landmarks Button
#     
#     self.switchToLandmarksLayoutButton = qt.QPushButton("Switch to Landmarks Layout")
#     self.switchToLandmarksLayoutButton.toolTip = "Switch to Landmarks Layout"
#     self.switchToLandmarksLayoutButton.name = "SwitchToLandmarksLayout"
#     landmarksFormLayout.addWidget(self.switchToLandmarksLayoutButton)
#     self.switchToLandmarksLayoutButton.connect('clicked()', landmarkManager.setLayout)
#     
#     self.setMRILandmarksButton = qt.QPushButton("Set MRI Landmarks")
#     self.setMRILandmarksButton.toolTip = "Set MRI Landmarks"
#     self.setMRILandmarksButton.name = "SetMRILandmarks"
#     landmarksFormLayout.addWidget(self.setMRILandmarksButton)
#     self.setMRILandmarksButton.connect('clicked()', self.logic.setLandmarksForMRI)
#     
#     self.finishedMRIButton = qt.QPushButton("Finished MRI")
#     self.finishedMRIButton.toolTip = "Finished MRI Landmarks"
#     self.finishedMRIButton.name = "FinishedMRILandmarks"
#     landmarksFormLayout.addWidget(self.finishedMRIButton)
#     self.finishedMRIButton.connect('clicked()', self.logic.setMouseModeBack)
#     
#     # Set Histology Landmarks Button
#     
#     self.setHistoLandmarksButton = qt.QPushButton("Set Histology Landmarks")
#     self.setHistoLandmarksButton.toolTip = "Set Histology Landmarks"
#     self.setHistoLandmarksButton.name = "SetHistoLandmarks"
#     landmarksFormLayout.addWidget(self.setHistoLandmarksButton)
#     self.setHistoLandmarksButton.connect('clicked()', self.logic.setLandmarksForHisto)
#     
#     self.finishedHistoButton = qt.QPushButton("Finished Histo")
#     self.finishedHistoButton.toolTip = "Finished MRI Landmarks"
#     self.finishedHistoButton.name = "FinishedMRILandmarks"
#     landmarksFormLayout.addWidget(self.finishedHistoButton)
#     self.finishedHistoButton.connect('clicked()', self.logic.setMouseModeBack)
#     
#     self.generateMRIMaskButton = qt.QPushButton("Generate mask from MRI fiducials")
#     self.generateMRIMaskButton.toolTip = "Generate a mask for the MRI volume out of the MRI landmarks"
#     self.generateMRIMaskButton.name = "GenerateMRIMask"
#     landmarksFormLayout.addWidget(self.generateMRIMaskButton)
#     self.generateMRIMaskButton.connect('clicked()', self.logic.generateMRIMask)
# 	
# 	#
#     # Registration Optimization
# 	#
# 	
#     registrationCollapsibleButton = ctk.ctkCollapsibleButton()
#     registrationCollapsibleButton.text = "Optimize Registration"
#     self.layout.addWidget(registrationCollapsibleButton)
#     registrationFormLayout = qt.QFormLayout(registrationCollapsibleButton)
    
    self.loaddataGroup = qt.QGroupBox("Load Data")
    self.layout.addWidget(self.loaddataGroup)
    loaddataLayout = qt.QGridLayout(self.loaddataGroup)
    
    self.loaddataLabel = qt.QLabel("1.")
    loaddataLayout.addWidget(self.loaddataLabel, 0, 0)
    self.loadMRIButton = qt.QPushButton("Load MRI")
    self.loadMRIButton.toolTip = "Load the MRI File."
    self.loadMRIButton.name = "LoadMRI"
    loaddataLayout.addWidget(self.loadMRIButton, 0, 1)
    self.loaddataLabel = qt.QLabel("2.")
    loaddataLayout.addWidget(self.loaddataLabel, 1, 0)
    self.loadMRIButton.connect('clicked()', self.logic.loadMRIVolume)
    self.loadHistologyButton = qt.QPushButton("Load Histology")
    self.loadHistologyButton.toolTip = "Load the Histology File."
    self.loadHistologyButton.name = "LoadHistology"
    loaddataLayout.addWidget(self.loadHistologyButton, 1, 1)
    self.loaddataLabel = qt.QLabel("3.")
    loaddataLayout.addWidget(self.loaddataLabel, 2, 0)
    self.loadHistologyButton.connect('clicked()', self.logic.loadHistologyVolume)
    self.alignButton = qt.QPushButton("Scroll to histology")
    self.alignButton.setStyleSheet("background-color: #7CB567");
    self.alignButton.toolTip = "Rotate to Volume Plane."
    self.alignButton.name = "AlignVolumes"
    loaddataLayout.addWidget(self.alignButton, 2, 1)
    self.alignButton.connect('clicked()', self.logic.alignSlices)    
    
    self.initialalignmentGroup = qt.QGroupBox("Initial Alignment of the histology")
    self.layout.addWidget(self.initialalignmentGroup)
    initialalignmentForm = qt.QGridLayout(self.initialalignmentGroup)
    self.positionSliderWidget = slicer.qMRMLTransformSliders()
    self.positionSliderWidget.Title = 'Position'
    self.positionSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.TRANSLATION
    self.positionSliderWidget.CoordinateReference = slicer.qMRMLTransformSliders.LOCAL
    self.positionSliderWidget.setMRMLScene(slicer.mrmlScene)
    self.logic.setPositionSliderWidget(self.positionSliderWidget)
    #self.positionSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))
    #loadDataFormLayout.addRow("Translation", self.positionSliderWidget)
    initialalignmentForm.addWidget(self.positionSliderWidget, 0, 0)    
    
    self.orientationSliderWidget = slicer.qMRMLTransformSliders()
    self.orientationSliderWidget.Title = 'Orientation'
    self.orientationSliderWidget.setMRMLScene(slicer.mrmlScene)
    # Setting of qMRMLTransformSliders.TypeOfTransform is not robust: it has to be set after setMRMLScene and
    # has to be set twice (with setting the type to something else in between).
    # Therefore the following 3 lines are needed, and they are needed here:
    self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.ROTATION
    self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.TRANSLATION
    self.orientationSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.ROTATION
    self.orientationSliderWidget.CoordinateReference=slicer.qMRMLTransformSliders.LOCAL
    self.orientationSliderWidget.minMaxVisible = False
    self.logic.setOrientationSliderWidget(self.orientationSliderWidget)
    #self.orientationSliderWidget.setMRMLTransformNode(self.getPivotToRasTransformNode())
    #loadDataFormLayout.addRow("Orientation", self.orientationSliderWidget)
    initialalignmentForm.addWidget(self.orientationSliderWidget, 1, 0)
    
    self.applyTransformButton = qt.QPushButton("Apply Transformation")
    self.applyTransformButton.setStyleSheet("background-color: #7CB567");
    self.applyTransformButton.toolTip = "Saves the positioning of the histology slice."
    self.applyTransformButton.name = "ApplyTransform"
    #loadDataFormLayout.addWidget(self.applyTransformButton)
    initialalignmentForm.addWidget(self.applyTransformButton, 2, 0)
    self.applyTransformButton.connect('clicked()', self.logic.applyTransformation)
    
    self.histologymaskGroup = qt.QGroupBox("Add Mask for Histology")
    self.layout.addWidget(self.histologymaskGroup)
    self.converthistologyLabel = qt.QLabel("1.")
    histologymaskLayout = qt.QGridLayout(self.histologymaskGroup)
    self.converthistologyButton = qt.QPushButton("Convert Histology to Greyscale")
    self.converthistologyButton.connect('clicked()', self.logic.convertHistology)
    histologymaskLayout.addWidget(self.converthistologyButton, 0, 1)
    histologymaskLayout.addWidget(self.converthistologyLabel, 0, 0)
    
    self.markprostateLabel = qt.QLabel("2.")
    histologymaskLayout.addWidget(self.markprostateLabel, 1, 0)
    self.markProstateButton = qt.QPushButton("Resample histology to match MRI spacing")
    self.markProstateButton.toolTip = "Resample histology to match MRI spacing."
    self.markProstateButton.name = "ResampleHistology"
    histologymaskLayout.addWidget(self.markProstateButton, 1, 1)
    self.markProstateButton.connect('clicked()', self.logic.resampleHistology)
    
    self.markprostateLabel = qt.QLabel("3.")
    histologymaskLayout.addWidget(self.markprostateLabel, 2, 0)
    self.markProstateButton = qt.QPushButton("Mark Boundaries of the histology")
    self.markProstateButton.toolTip = "Mark the boundaries of the histology."
    self.markProstateButton.name = "MarkHistology"
    histologymaskLayout.addWidget(self.markProstateButton, 2, 1)
    self.markProstateButton.connect('clicked()', self.logic.markBoundaries)
    
    self.markprostateLabel = qt.QLabel("4.")
    histologymaskLayout.addWidget(self.markprostateLabel, 3, 0)
    self.markProstateButton = qt.QPushButton("Fill Histology")
    self.markProstateButton.toolTip = "Click on the inside of the histology to fill it."
    self.markProstateButton.name = "FillHistology"
    histologymaskLayout.addWidget(self.markProstateButton, 3, 1)
    self.markProstateButton.connect('clicked()', self.logic.fillHole)
    
    self.markprostateLabel = qt.QLabel("5.")
    histologymaskLayout.addWidget(self.markprostateLabel, 4, 0)
    self.markProstateButton = qt.QPushButton("Delete Urethra")
    self.markProstateButton.toolTip = "Delete the urethra from the histology."
    self.markProstateButton.name = "DeleteHistology"
    histologymaskLayout.addWidget(self.markProstateButton, 4, 1)
    self.markProstateButton.connect('clicked()', self.logic.deleteUrethraHisto)
    
    self.markmriGroup = qt.QGroupBox("Add Mask for MRI")
    self.layout.addWidget(self.markmriGroup)
    markmriLayout = qt.QGridLayout(self.markmriGroup)
    self.setlandmarksLabel = qt.QLabel("1.")
    markmriLayout.addWidget(self.setlandmarksLabel, 0, 0)
    
    self.setMRILandmarksButton = qt.QPushButton("Set MRI Landmarks")
    self.setMRILandmarksButton.toolTip = "Set MRI Landmarks"
    self.setMRILandmarksButton.name = "SetMRILandmarks"
    markmriLayout.addWidget(self.setMRILandmarksButton, 0, 1)
    self.setMRILandmarksButton.connect('clicked()', self.logic.setLandmarksForMRI)
    
    self.setlandmarksLabel = qt.QLabel("2.")
    markmriLayout.addWidget(self.setlandmarksLabel, 1, 0)
    
    self.finishedMRIButton = qt.QPushButton("Finished")
    self.finishedMRIButton.toolTip = "Finished MRI Landmarks"
    self.finishedMRIButton.name = "FinishedMRILandmarks"
    markmriLayout.addWidget(self.finishedMRIButton, 1, 1)
    self.finishedMRIButton.connect('clicked()', self.logic.setMouseModeBack)
    
    self.setlandmarksLabel = qt.QLabel("3.")
    markmriLayout.addWidget(self.setlandmarksLabel, 2, 0)
    
    self.generateMRIMaskButton = qt.QPushButton("Generate mask from landmarks")
    self.generateMRIMaskButton.toolTip = "Generate a mask for the MRI volume out of the MRI landmarks"
    self.generateMRIMaskButton.name = "GenerateMRIMask"
    markmriLayout.addWidget(self.generateMRIMaskButton, 2, 1)
    self.generateMRIMaskButton.connect('clicked()', self.logic.generateMRIMask)
    
    self.setlandmarksLabel = qt.QLabel("4.")
    markmriLayout.addWidget(self.setlandmarksLabel, 3, 0)
    
    self.generateMRIMaskButton = qt.QPushButton("Delete urethra from Mask")
    self.generateMRIMaskButton.toolTip = "Mark the urethra to delete it from the labelmap"
    self.generateMRIMaskButton.name = "DeleteUrethra"
    markmriLayout.addWidget(self.generateMRIMaskButton, 3, 1)
    self.generateMRIMaskButton.connect('clicked()', self.logic.deleteUrethraMRI)
    
    self.registrationGroup = qt.QGroupBox("Register MRI with histology")
    self.layout.addWidget(self.registrationGroup)
    
    registrationmaskLayout = qt.QGridLayout(self.registrationGroup)
    
    self.histoComboBoxLabel = qt.QLabel("Select the histology volume")
    registrationmaskLayout.addWidget(self.histoComboBoxLabel, 0, 0)
    
    self.histoComboBox = slicer.qMRMLNodeComboBox()
    registrationmaskLayout.addWidget(self.histoComboBox, 0, 1)
    self.histoComboBox.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.histoComboBox.selectNodeUponCreation = True
    self.histoComboBox.addEnabled = True
    self.histoComboBox.removeEnabled = False
    self.histoComboBox.renameEnabled = True
    self.histoComboBox.noneEnabled = False
    self.histoComboBox.showHidden = False
    self.histoComboBox.showChildNodeTypes = True
    self.histoComboBox.setMRMLScene(slicer.mrmlScene)
    #self.histoComboBox.connect('currentNodeChanged(vtkMRMLNode*)', self.logic.setHistologyVolume(self.histoComboBox.currentNode().GetID()))
    
    self.histoComboBoxLabel = qt.QLabel("Select the MRI volume")
    registrationmaskLayout.addWidget(self.histoComboBoxLabel, 1, 0)
    
    self.mriComboBox = slicer.qMRMLNodeComboBox()
    registrationmaskLayout.addWidget(self.mriComboBox, 1, 1)
    self.mriComboBox.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.mriComboBox.selectNodeUponCreation = True
    self.mriComboBox.addEnabled = True
    self.mriComboBox.removeEnabled = False
    self.mriComboBox.renameEnabled = True
    self.mriComboBox.noneEnabled = False
    self.mriComboBox.showHidden = False
    self.mriComboBox.showChildNodeTypes = True
    self.mriComboBox.setMRMLScene(slicer.mrmlScene)
    #self.mriComboBox.connect('currentNodeChanged(vtkMRMLNode*)', self.logic.setMRIVolume(self.mriComboBox.currentNode().GetID()))
    
    self.histoComboBoxLabel = qt.QLabel("Select the histology label map")
    registrationmaskLayout.addWidget(self.histoComboBoxLabel, 2, 0)
    
    self.histoLabelMapComboBox = slicer.qMRMLNodeComboBox()
    registrationmaskLayout.addWidget(self.histoLabelMapComboBox, 2, 1)
    self.histoLabelMapComboBox.nodeTypes = ["vtkMRMLLabelMapVolumeNode"]
    self.histoLabelMapComboBox.selectNodeUponCreation = True
    self.histoLabelMapComboBox.addEnabled = True
    self.histoLabelMapComboBox.removeEnabled = False
    self.histoLabelMapComboBox.renameEnabled = True
    self.histoLabelMapComboBox.noneEnabled = False
    self.histoLabelMapComboBox.showHidden = False
    self.histoLabelMapComboBox.showChildNodeTypes = True
    self.histoLabelMapComboBox.setMRMLScene(slicer.mrmlScene)
    
    self.histoComboBoxLabel = qt.QLabel("Select the MRI label map")
    registrationmaskLayout.addWidget(self.histoComboBoxLabel, 3, 0)
    
    self.mriLabelMapComboBox = slicer.qMRMLNodeComboBox()
    registrationmaskLayout.addWidget(self.mriLabelMapComboBox, 3, 1)
    self.mriLabelMapComboBox.nodeTypes = ["vtkMRMLLabelMapVolumeNode"]
    self.mriLabelMapComboBox.selectNodeUponCreation = True
    self.mriLabelMapComboBox.addEnabled = True
    self.mriLabelMapComboBox.removeEnabled = False
    self.mriLabelMapComboBox.renameEnabled = True
    self.mriLabelMapComboBox.noneEnabled = False
    self.mriLabelMapComboBox.showHidden = False
    self.mriLabelMapComboBox.showChildNodeTypes = True
    self.mriLabelMapComboBox.setMRMLScene(slicer.mrmlScene)
    
    self.registrationButton1 = qt.QPushButton("Apply Rigid DistanceMap Registration")
    self.registrationButton1.connect('clicked()', self.onApplyDistanceMapRegistration)
    self.registrationButton1.setStyleSheet("background-color: #7CB567");
    registrationmaskLayout.addWidget(self.registrationButton1, 4, 1)
    
    self.registrationButton2 = qt.QPushButton("Apply Affine Volume Registration")
    self.registrationButton2.connect('clicked()', self.onApplyRegistration)
    self.registrationButton2.setStyleSheet("background-color: #7CB567");
    registrationmaskLayout.addWidget(self.registrationButton2, 5, 1)

  def onApplyRegistration(self):
    self.logic.setMRIVolume(self.mriComboBox.currentNode())
    self.logic.setHistologyVolume(self.histoComboBox.currentNode())
    self.logic.setMRILabelMap(self.mriLabelMapComboBox.currentNode())
    self.logic.setHistologyLabelMap(self.histoLabelMapComboBox.currentNode())
    self.logic.applyRegistration()
    
  def onApplyDistanceMapRegistration(self):
    self.logic.setMRIVolume(self.mriComboBox.currentNode())
    self.logic.setHistologyVolume(self.histoComboBox.currentNode())
    self.logic.setMRILabelMap(self.mriLabelMapComboBox.currentNode())
    self.logic.setHistologyLabelMap(self.histoLabelMapComboBox.currentNode())
    self.logic.applyDistanceMapRegistration()
    
  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = ProstateLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), enableScreenshotsFlag, screenshotScaleFactor)

#
# ProstateLogic
#

class ProstateLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
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
    
  def __init__(self, parent=None):
    self.mriVolume = None
    self.histoVolume = None
    self.histoVolumeBW = None
    self.mriVolumeRegistration = None
    self.mriVolumeHistology = None
    self.mriLabelmap = None
    self.histoLabelmap = None
    self.mriLandmarks = None
    self.histoLandmarks = None
    self.wholeSceneTransform = None
    self.mriTransform = None
    self.transformNode = None
    self.cameraNode = None
    self.positionSliderWidget = None
    self.orientationSliderWidget = None
    self.roiLabelMap = None
    self.labelMapValues = {'PROSTATE': 238, 'URETHRA': 227}

  def setMRIVolume(self, mriVolume):
    self.mriVolumeRegistration = mriVolume

  def setHistologyVolume(self, histologyVolume):
    self.histoVolumeRegistration = histologyVolume

  def setMRILabelMap(self, mriLabelMap):
    self.mriLabelmap = mriLabelMap
    
  def setHistologyLabelMap(self, histologyLabelMap):
    self.histoLabelmap = histologyLabelMap

  def loadMRIVolume(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.mriVolume = slicer.util.getNode('*ScalarVolumeNode*')
    self.mriVolume.SetName('MRI_Volume')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
      
  def getMRIVolume(self):
    if self.mriVolume is not None:
      return self.mriVolume
  
  def loadHistologyVolume(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.histoVolume = slicer.util.getNode('*VectorVolumeNode*')
    self.histoVolume.SetName('Histo_Volume')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
      
  def getHistologyVolume(self):
    if self.histoVolume is not None:
        return self.histoVolume

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
      
    # Main view with both MRI and histology
    node = slicer.app.layoutManager().sliceWidget('Main').sliceLogic().GetSliceCompositeNode()
    
    node.SetForegroundVolumeID(self.histoVolume.GetID())
    node.SetForegroundOpacity(0.5)
    node.SetBackgroundVolumeID(self.mriVolume.GetID())      
    slicer.app.layoutManager().sliceWidget('Main').sliceLogic().FitSliceToAll() 

    # MRI only view
    node = slicer.app.layoutManager().sliceWidget('Axial').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(None)
    node.SetBackgroundVolumeID(self.mriVolume.GetID())
    slicer.app.layoutManager().sliceWidget('Axial').sliceLogic().FitSliceToAll()
    node = slicer.util.getNode('*SliceNodeAxial*')
    node.SetOrientationToAxial()
    node.RotateToVolumePlane(volumeNodes[0])
    
    # Histology only view
    node = slicer.app.layoutManager().sliceWidget('Histology').sliceLogic().GetSliceCompositeNode()
    node.SetBackgroundVolumeID(self.histoVolume.GetID())
    node.SetLabelVolumeID(None)
    node = slicer.util.getNode('*SliceNodeHistology*')
    node.SetOrientationToAxial()
    node.RotateToVolumePlane(volumeNodes[0])
    
    # Coronal view
    node = slicer.app.layoutManager().sliceWidget('Coronal').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(self.histoVolume.GetID())
    node.SetBackgroundVolumeID(self.mriVolume.GetID())
    node.SetForegroundOpacity(0.5)
    node = slicer.util.getNode('*SliceNodeCoronal*')
    node.SetOrientationToCoronal()
    slicer.app.layoutManager().sliceWidget('Coronal').sliceLogic().FitSliceToAll()
    node.RotateToVolumePlane(volumeNodes[0])    
    
    # Sagittal view
    node = slicer.app.layoutManager().sliceWidget('Sagittal').sliceLogic().GetSliceCompositeNode()
    node.SetForegroundVolumeID(self.histoVolume.GetID())
    node.SetBackgroundVolumeID(self.mriVolume.GetID())
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
    node = slicer.util.getNode('*SliceNodeMain*')
    node.SetSliceOffset(float(histoOffset))
    node = slicer.util.getNode('*SliceNodeHistology*')
    node.SetSliceOffset(float(histoOffset))
    node = slicer.util.getNode('*SliceNodeAxial*')
    node.SetSliceOffset(float(histoOffset))

  def setupTransform(self):
    self.cameraNode = slicer.util.getNode('*CameraNode*')
    self.transformNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLLinearTransformNode())
    self.transformNode.SetName('MRI_Transform')
    self.mriVolume.SetAndObserveTransformNodeID(self.transformNode.GetID())    
    self.positionSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))  
    self.orientationSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))  

  def setPositionSliderWidget(self, positionSliderWidget):
    self.positionSliderWidget = positionSliderWidget
          
  def setOrientationSliderWidget(self, orientationSliderWidget):
    self.orientationSliderWidget = orientationSliderWidget        
          
  def checkLoaded(self):
    '''Checks if both the Histology and MRI are loaded.'''
    if (self.mriVolume is not None and self.histoVolume is not None):
      return True
    else:
      return False
  
  def applyTransformation(self):
    if (self.transformNode is not None):
      print('bla')
      logic = slicer.vtkSlicerTransformLogic()
      logic.hardenTransform(self.mriVolume)
      
  def setLayout(self):
    layoutManager = slicer.app.layoutManager()
    self.customLayoutId = 502
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(self.customLayoutId, self.layout)                                         
    layoutManager.setLayout(self.customLayoutId)
    
  def convertHistology(self):
    node = slicer.mrmlScene.AddNode(slicer.vtkMRMLScalarVolumeNode())
    node.SetName('Histo_Volume_BW')
    params = {'InputVolume': slicer.util.getNode('Histo_Volume'), 'OutputVolume': node}
    #self.histoVolumeBW = node
    # run vectortoscalarvolume-CLI Module
    #slicer.cli.run(slicer.modules.vectortoscalarvolume, None, params, wait_for_completion=True)
    # check for input data
    inputVolume = params['InputVolume']
    outputVolume = params['OutputVolume']
    # Code from Convert Vector to Scalar Volume Plugin
    if not (inputVolume and outputVolume):
      qt.QMessageBox.critical(
          slicer.util.mainWindow(),
          'Luminance', 'Input and output volumes are required for conversion')
      return
    # check that data has enough components
    inputImage = inputVolume.GetImageData()
    if not inputImage or inputImage.GetNumberOfScalarComponents() < 3:
      qt.QMessageBox.critical(
          slicer.util.mainWindow(),
          'Vector to Scalar Volume', 'Input does not have enough components for conversion')
      return
    # run the filter
    # - extract the RGB portions
    extract = vtk.vtkImageExtractComponents()
    extract.SetComponents(0,1,2)
    luminance = vtk.vtkImageLuminance()
    if vtk.VTK_MAJOR_VERSION <= 5:
      extract.SetInput(inputVolume.GetImageData())
      luminance.SetInput(extract.GetOutput())
      luminance.GetOutput().Update()
    else:
      extract.SetInputConnection(inputVolume.GetImageDataConnection())
      luminance.SetInputConnection(extract.GetOutputPort())
      luminance.Update()
    ijkToRAS = vtk.vtkMatrix4x4()
    inputVolume.GetIJKToRASMatrix(ijkToRAS)
    outputVolume.SetIJKToRASMatrix(ijkToRAS)
    if vtk.VTK_MAJOR_VERSION <= 5:
      outputVolume.SetAndObserveImageData(luminance.GetOutput())
    else:
      outputVolume.SetImageDataConnection(luminance.GetOutputPort())
    # make the output volume appear in all the slice views
    selectionNode = slicer.app.applicationLogic().GetSelectionNode()
    selectionNode.SetReferenceActiveVolumeID(outputVolume.GetID())
    slicer.app.applicationLogic().PropagateVolumeSelection(0)
    self.histoVolumeBW = outputVolume  
      
  def applyRegistration(self):
    print(self.histoVolume.GetID())
    print(self.mriVolume.GetID())
    if self.wholeSceneTransform is None:
        self.wholeSceneTransform = slicer.mrmlScene.AddNode(slicer.vtkMRMLLinearTransformNode())
    paramsRigid = {'fixedVolume': self.histoVolumeBW,
                   'movingVolume': self.mriVolume,
                   'fixedBinaryVolume': self.histoLabelmap,
                   'movingBinaryVolume': self.mriLabelmap,
                   'outputTransform': self.wholeSceneTransform.GetID(),
                   #'outputVolume': self.currentResult.rigidVolume.GetID(),
                   'maskProcessingMode': "ROI",
                   'useRigid': False,
                   'useAffine': True,
                   'useBSpline': False,
                   'useScaleVersor3D': False,
                   'useScaleSkewVersor3D': False,
                   'useROIBSpline': False}
    slicer.cli.run(slicer.modules.brainsfit, None, paramsRigid, wait_for_completion=True) 
    
  def markBoundaries(self):
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    if self.histoLabelmap is None:
      self.histoLabelmap = slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.histoVolumeBW, 'Histo_Label_Map')
    #lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.dataManager.getMRI().GetID())
    lm.sliceWidget('Histology').sliceLogic().GetSliceCompositeNode().SetLabelVolumeID(self.histoLabelmap.GetID())
    paintEffectOptions = EditorLib.PaintEffectOptions()
    paintEffectOptions.setMRMLDefaults()
    paintEffectOptions.__del__()
    #slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.dataManager.getMRI(), 'prostateLabelMap')
    editUtil.setLabel(self.labelMapValues['PROSTATE'])
    #self.delayDisplay('Paint radius is %s' % parameterNode.GetParameter('PaintEffect,radius'))
    sliceWidget = lm.sliceWidget('Histology')
    size = min(sliceWidget.width,sliceWidget.height)
    step = size / 12
    center = size / 2
    parameterNode.SetParameter('PaintEffect,radius', '2')
    paintTool = EditorLib.PaintEffectTool(sliceWidget)
  
  def deleteUrethraMRI(self):
    # TODO: create copy of MRI mask  
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    if self.mriLabelmap is None:
      return
    #lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.dataManager.getMRI().GetID())
    lm.sliceWidget('Axial').sliceLogic().GetSliceCompositeNode().SetLabelVolumeID(self.mriLabelmap.GetID())
    paintEffectOptions = EditorLib.PaintEffectOptions()
    paintEffectOptions.setMRMLDefaults()
    paintEffectOptions.__del__()
    #slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.dataManager.getMRI(), 'prostateLabelMap')
    editUtil.setLabel(0)
    #self.delayDisplay('Paint radius is %s' % parameterNode.GetParameter('PaintEffect,radius'))
    sliceWidget = lm.sliceWidget('Axial')
    size = min(sliceWidget.width,sliceWidget.height)
    step = size / 12
    center = size / 2
    parameterNode.SetParameter('PaintEffect,radius', '3')
    paintTool = EditorLib.PaintEffectTool(sliceWidget)
    
  def deleteUrethraHisto(self):
    # TODO: create copy of MRI mask  
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    if self.histoLabelmap is None:
      return
    #lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.dataManager.getMRI().GetID())
    lm.sliceWidget('Histology').sliceLogic().GetSliceCompositeNode().SetLabelVolumeID(self.histoLabelmap.GetID())
    paintEffectOptions = EditorLib.PaintEffectOptions()
    paintEffectOptions.setMRMLDefaults()
    paintEffectOptions.__del__()
    #slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.dataManager.getMRI(), 'prostateLabelMap')
    editUtil.setLabel(0)
    #self.delayDisplay('Paint radius is %s' % parameterNode.GetParameter('PaintEffect,radius'))
    sliceWidget = lm.sliceWidget('Histology')
    size = min(sliceWidget.width,sliceWidget.height)
    step = size / 12
    center = size / 2
    parameterNode.SetParameter('PaintEffect,radius', '3')
    paintTool = EditorLib.PaintEffectTool(sliceWidget)        
  
  def fillHole(self):
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    lm = slicer.app.layoutManager()
    if self.histoLabelmap is None:
      self.histoLabelmap = slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.histoVolumeBW, 'Histo_Label_Map')
    #lm.sliceWidget('Red').sliceLogic().GetSliceCompositeNode().SetBackgroundVolumeID(self.dataManager.getMRI().GetID())
    lm.sliceWidget('Histology').sliceLogic().GetSliceCompositeNode().SetLabelVolumeID(self.histoLabelmap.GetID())
    paintEffectOptions = EditorLib.PaintEffectOptions()
    paintEffectOptions.setMRMLDefaults()
    paintEffectOptions.__del__()
    #slicer.modules.volumes.logic().CreateAndAddLabelVolume(self.dataManager.getMRI(), 'prostateLabelMap')
    editUtil.setLabel(self.labelMapValues['PROSTATE'])
    #self.delayDisplay('Paint radius is %s' % parameterNode.GetParameter('PaintEffect,radius'))
    sliceWidget = lm.sliceWidget('Histology')
    size = min(sliceWidget.width,sliceWidget.height)
    step = size / 12
    center = size / 2
    parameterNode.SetParameter('ChangeIslandEffect,radius', '2')
    paintTool = EditorLib.PaintEffectTool(sliceWidget)      
    
  def setMouseModeBack(self):
    interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
    interactionNode.SwitchToViewTransformMode()
    # also turn off place mode persistence if required
    interactionNode.SetPlaceModePersistence(0)
    
  def __setMouseModeToFiducial(self):
    placeModePersistence = 1
    slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
  
  def createFiducialMap(self, name):
    if slicer.util.getNode(name) is None:
      fiducial = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsFiducialNode())
      fiducial.SetName(name)
              
  def setLandmarksForMRI(self):
    self.createFiducialMap('MRI_Landmarks')
    self.__setMouseModeToFiducial()
    
  def setLandmarksForHisto(self):
    self.createFiducialMap('Histo_Landmarks')
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
         
  def generateMRIMask(self):
    import VolumeClipWithModel
    volumeClipLogic = VolumeClipWithModel.VolumeClipWithModelLogic()
    self.clippingModelNode = slicer.vtkMRMLModelNode()
    self.clippingModelNode.SetName('clipModelNode')
    slicer.mrmlScene.AddNode(self.clippingModelNode)
    volumeClipLogic.updateModelFromMarkup(slicer.util.getNode('MRI_Landmarks'), self.clippingModelNode)
    outputLabelMap = slicer.vtkMRMLScalarVolumeNode()
    name = ('MRIMask-label')
    outputLabelMap.SetName(name)
    slicer.mrmlScene.AddNode(outputLabelMap)
    volumeLogic = slicer.modules.volumes.logic()
    label = slicer.util.getNode('*MRIMask*')
    volumeLogic.CreateAndAddLabelVolume(slicer.mrmlScene, label, 'MRI_Label_Map')
    outputLabelMap = slicer.util.getNode('MRI_Label_Map')
    self.mriLabelmap = outputLabelMap
    #slicer.mrmlScene.AddNode(outputLabelMap)

    # define params
    params = {'sampleDistance': 0.1, 'labelValue': 5, 'InputVolume': slicer.util.getNode('MRI_Volume'),
              'surface': self.clippingModelNode.GetID(), 'OutputVolume': outputLabelMap.GetID()}

    # run ModelToLabelMap-CLI Module
    slicer.cli.run(slicer.modules.modeltolabelmap, None, params, wait_for_completion=True)
  
  def generateDistanceMap(self, labelID, smoothingSteps):
    # TODO : crop distance maps
    # Smooth label  
    if smoothingSteps > 0:
      smoothedLabelMap = sitkUtils.CreateNewVolumeNode(labelID.GetName()+'_Smoothed',overwrite=True)
      storageNode = slicer.vtkMRMLNRRDStorageNode()
      slicer.mrmlScene.AddNode(storageNode)
      smoothedLabelMap.SetAndObserveStorageNodeID(storageNode.GetID())
      initLabelMap = labelID
      for i in range(0, smoothingSteps):
        print(i)
        smoothingParameters = {'inputImageName':initLabelMap.GetID(), 'outputImageName':smoothedLabelMap.GetID()}
        cliNode = slicer.cli.run(slicer.modules.segmentationsmoothing, None, smoothingParameters, wait_for_completion = True)
        initLabelMap = smoothedLabelMap          
    # Set up filter  
    dt = sitk.SignedMaurerDistanceMapImageFilter()
    dt.SetSquaredDistance(False)
    dt.SetUseImageSpacing(False)
    dt.SetInsideIsPositive(False)
    if smoothingSteps == 0:
      labelAddress = sitkUtils.GetSlicerITKReadWriteAddress(labelID.GetName())
    else:
      labelAddress = sitkUtils.GetSlicerITKReadWriteAddress(smoothedLabelMap.GetName())
    labelImage = sitk.ReadImage(labelAddress)
    # Execute filter
    distanceImage = dt.Execute(labelImage)
    sitkUtils.PushToSlicer(distanceImage, labelID.GetName()+'_DistanceMap', overwrite=True)
  
  def resampleHistology(self):
    params = {'inputVolume': self.histoVolumeBW,
              'referenceVolume': self.mriVolume,
              'outputVolume': self.histoVolumeBW}
    slicer.cli.run(slicer.modules.brainsresample, None, params, wait_for_completion=True)
  
  def applyDistanceMapRegistration(self):
    self.generateDistanceMap(self.mriLabelmap, 0)
    self.generateDistanceMap(self.histoLabelmap, 0)
    histoDistanceMap = slicer.util.getNode(self.histoLabelmap.GetName()+'_DistanceMap')
    mriDistanceMap = slicer.util.getNode(self.mriLabelmap.GetName()+'_DistanceMap')
    distanceMapTransform = slicer.mrmlScene.AddNode(slicer.vtkMRMLLinearTransformNode())
    distanceMapTransform.SetName('DistanceMapTransform')
    paramsRigid = {'fixedVolume': histoDistanceMap,
                   'movingVolume': mriDistanceMap,
                   'fixedBinaryVolume': self.histoLabelmap,
#                    'movingBinaryVolume': self.mriLabelmap,
                   'outputTransform': distanceMapTransform.GetID(),
                   #'outputVolume': self.currentResult.rigidVolume.GetID(),
                   'maskProcessingMode': "NOMASK",
                   'useRigid': False,
                   'useAffine': True,
                   'useBSpline': False,
                   'useScaleVersor3D': False,
                   'useScaleSkewVersor3D': False,
                   'useROIBSpline': False}
    slicer.cli.run(slicer.modules.brainsfit, None, paramsRigid, wait_for_completion=True) 
                
  def hasImageData(self, volumeNode):
    """This is a dummy logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def takeScreenshot(self, name, description, type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage, imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self, inputVolume, outputVolume, enableScreenshots=0, screenshotScaleFactor=1):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    self.enableScreenshots = enableScreenshots
    self.screenshotScaleFactor = screenshotScaleFactor

    self.takeScreenshot('Prostate-Start', 'Start', -1)

    return True


class ProstateTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Prostate1()

  def test_Prostate1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url, name, loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ProstateLogic()
    self.assertTrue(logic.hasImageData(volumeNode))
    self.delayDisplay('Test passed!')

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
      self.createFiducialMap('MRI_Landmarks')
      self.__setMouseModeToFiducial()
      
    def setLandmarksForHisto(self):
      self.createFiducialMap('Histo_Landmarks')
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
    
        
    def generateMRIMask(self):
        import VolumeClipWithModel
        volumeClipLogic = VolumeClipWithModel.VolumeClipWithModelLogic()
        self.clippingModelNode = slicer.vtkMRMLModelNode()
        self.clippingModelNode.SetName('clipModelNode')
        slicer.mrmlScene.AddNode(self.clippingModelNode)
        volumeClipLogic.updateModelFromMarkup(slicer.util.getNode('MRI_Landmarks'), self.clippingModelNode)
        outputLabelMap = slicer.vtkMRMLScalarVolumeNode()
        name = ('MRIMask-label')
        outputLabelMap.SetName(name)
        slicer.mrmlScene.AddNode(outputLabelMap)
        volumeLogic = slicer.modules.volumes.logic()
        label = slicer.util.getNode('*MRIMask*')
        volumeLogic.CreateAndAddLabelVolume(slicer.mrmlScene, label, 'MRI_Label_Map')
        outputLabelMap = slicer.util.getNode('MRI_Label_Map')
        #slicer.mrmlScene.AddNode(outputLabelMap)

        # define params
        params = {'sampleDistance': 0.1, 'labelValue': 5, 'InputVolume': slicer.util.getNode('MRI_Volume'),
                  'surface': self.clippingModelNode.GetID(), 'OutputVolume': outputLabelMap.GetID()}

        # run ModelToLabelMap-CLI Module
        slicer.cli.run(slicer.modules.modeltolabelmap, None, params, wait_for_completion=True)
        
