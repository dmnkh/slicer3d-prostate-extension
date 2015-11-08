import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# Prostate
#

class Prostate(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Prostate"  # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
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

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
    self.inputSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.inputSelector.setToolTip("Pick the input to the algorithm.")
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
    self.outputSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    self.outputSelector.setToolTip("Pick the output to the algorithm.")
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # scale factor for screen shots
    #
    self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
    self.screenshotScaleFactorSliderWidget.singleStep = 1.0
    self.screenshotScaleFactorSliderWidget.minimum = 1.0
    self.screenshotScaleFactorSliderWidget.maximum = 50.0
    self.screenshotScaleFactorSliderWidget.value = 1.0
    self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
    parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    # self.layout.addStretch(1)
	
	#
	# Load Data
	#
    dm = DataManager()
    loadDataCollapsibleButton = ctk.ctkCollapsibleButton()
    loadDataCollapsibleButton.text = "Load Data"
    self.layout.addWidget(loadDataCollapsibleButton)
    loadDataFormLayout = qt.QFormLayout(loadDataCollapsibleButton)
	
	# Load MRI Button
	
    self.loadMRIButton = qt.QPushButton("Load MRI")
    self.loadMRIButton.toolTip = "Load the MRI File."
    self.loadMRIButton.name = "LoadMRI"
    loadDataFormLayout.addWidget(self.loadMRIButton)
    self.loadMRIButton.connect('clicked()', dm.loadMRI)

	# Load Histology Button
	
    self.loadHistologyButton = qt.QPushButton("Load Histology")
    self.loadHistologyButton.toolTip = "Load the Histology File."
    self.loadHistologyButton.name = "LoadHistology"
    loadDataFormLayout.addWidget(self.loadHistologyButton)
    self.loadHistologyButton.connect('clicked()', dm.loadHistology)
	
    '''lm = slicer.app.layoutManager()
    red = lm.sliceWidget('Red')
    redLogic = red.sliceLogic()
    # Print current slice offset position
    print redLogic.GetSliceOffset()
    # Change slice position
    redLogic.SetSliceOffset(20)'''
    self.alignButton = qt.QPushButton("Align Volumes")
    self.alignButton.toolTip = "Rotate to Volume Plane."
    self.alignButton.name = "AlignVolumes"
    loadDataFormLayout.addWidget(self.alignButton)
    self.alignButton.connect('clicked()', dm.alignSlices)	
    
    self.positionSliderWidget = slicer.qMRMLTransformSliders()
    self.positionSliderWidget.Title = 'Position'
    self.positionSliderWidget.TypeOfTransform = slicer.qMRMLTransformSliders.TRANSLATION
    self.positionSliderWidget.CoordinateReference = slicer.qMRMLTransformSliders.LOCAL
    self.positionSliderWidget.setMRMLScene(slicer.mrmlScene)
    dm.setPositionSliderWidget(self.positionSliderWidget)
    #self.positionSliderWidget.setMRMLTransformNode(slicer.util.getNode(self.transformNode.GetID()))
    loadDataFormLayout.addRow("Translation", self.positionSliderWidget)    
    
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
    dm.setOrientationSliderWidget(self.orientationSliderWidget)
    #self.orientationSliderWidget.setMRMLTransformNode(self.getPivotToRasTransformNode())
    loadDataFormLayout.addRow("Orientation", self.orientationSliderWidget)
    
    self.applyTransformButton = qt.QPushButton("Apply")
    self.applyTransformButton.toolTip = "Saves the positioning of the histology slice."
    self.applyTransformButton.name = "ApplyTransform"
    loadDataFormLayout.addWidget(self.applyTransformButton)
    self.applyTransformButton.connect('clicked()', dm.applyTransformation)
    
	#
	# Bounding Box
	#
	
    boundingBoxCollapsibleButton = ctk.ctkCollapsibleButton()
    boundingBoxCollapsibleButton.text = "Mark Extents"
    self.layout.addWidget(boundingBoxCollapsibleButton)
    boundingBoxFormLayout = qt.QFormLayout(boundingBoxCollapsibleButton)
	
	#
	# ROI definition
	#
	
    roiDefintitionCollapsibleButton = ctk.ctkCollapsibleButton()
    roiDefintitionCollapsibleButton.text = "ROI definition"
    self.layout.addWidget(roiDefintitionCollapsibleButton)
    roiDefintitionFormLayout = qt.QFormLayout(roiDefintitionCollapsibleButton)
    roiManager = ROIManager(dm)
    
    # Mark Prostate Button
    
    self.markProstateButton = qt.QPushButton("Mark Prostate")
    self.markProstateButton.toolTip = "Mark the boundaries of the prostate."
    self.markProstateButton.name = "MarkProstate"
    roiDefintitionFormLayout.addWidget(self.markProstateButton)
    self.markProstateButton.connect('clicked()', roiManager.markProstate)

    # Mark Urethra Button
    
    self.markUrethraButton = qt.QPushButton("Mark Urethra")
    self.markUrethraButton.toolTip = "Mark the boundaries of the urethra."
    self.markUrethraButton.name = "MarkUrethra"
    roiDefintitionFormLayout.addWidget(self.markUrethraButton)
    self.markUrethraButton.connect('clicked()', roiManager.markUrethra)
	
    # Finished Marking Button
    
    self.finishedMarkingButton = qt.QPushButton("Finished Marking")
    self.finishedMarkingButton.toolTip = "Finished Marking"
    self.finishedMarkingButton.name = "FinishedMarking"
    roiDefintitionFormLayout.addWidget(self.finishedMarkingButton)
    self.finishedMarkingButton.connect('clicked()', roiManager.setMouseModeBack)
    
    # 
    
    #
    # PET/MR alignment
	#
	
    petMRIAlignmentCollapsibleButton = ctk.ctkCollapsibleButton()
    petMRIAlignmentCollapsibleButton.text = "PET/MR alignment"
    self.layout.addWidget(petMRIAlignmentCollapsibleButton)
    petMRAlignmentFormLayout = qt.QFormLayout(petMRIAlignmentCollapsibleButton)
	
    #
    # Landmarking on histology and PET/MR
	#
	
    landmarksCollapsibleButton = ctk.ctkCollapsibleButton()
    landmarksCollapsibleButton.text = "Set Landmarks"
    self.layout.addWidget(landmarksCollapsibleButton)
    landmarksFormLayout = qt.QFormLayout(landmarksCollapsibleButton)
    landmarkManager = LandmarkManager(dm)
    
    # Set MRI Landmarks Button
    
    self.switchToLandmarksLayoutButton = qt.QPushButton("Switch to Landmarks Layout")
    self.switchToLandmarksLayoutButton.toolTip = "Switch to Landmarks Layout"
    self.switchToLandmarksLayoutButton.name = "SwitchToLandmarksLayout"
    landmarksFormLayout.addWidget(self.switchToLandmarksLayoutButton)
    self.switchToLandmarksLayoutButton.connect('clicked()', landmarkManager.setLayout)
    
    self.setMRILandmarksButton = qt.QPushButton("Set MRI Landmarks")
    self.setMRILandmarksButton.toolTip = "Set MRI Landmarks"
    self.setMRILandmarksButton.name = "SetMRILandmarks"
    landmarksFormLayout.addWidget(self.setMRILandmarksButton)
    self.setMRILandmarksButton.connect('clicked()', landmarkManager.setLandmarksForMRI)
    
    self.finishedMRIButton = qt.QPushButton("Finished MRI")
    self.finishedMRIButton.toolTip = "Finished MRI Landmarks"
    self.finishedMRIButton.name = "FinishedMRILandmarks"
    landmarksFormLayout.addWidget(self.finishedMRIButton)
    self.finishedMRIButton.connect('clicked()', landmarkManager.setMouseModeBack)
    
    # Set Histology Landmarks Button
    
    self.setHistoLandmarksButton = qt.QPushButton("Set Histology Landmarks")
    self.setHistoLandmarksButton.toolTip = "Set Histology Landmarks"
    self.setHistoLandmarksButton.name = "SetHistoLandmarks"
    landmarksFormLayout.addWidget(self.setHistoLandmarksButton)
    self.setHistoLandmarksButton.connect('clicked()', landmarkManager.setLandmarksForHisto)
    
    self.finishedHistoButton = qt.QPushButton("Finished Histo")
    self.finishedHistoButton.toolTip = "Finished MRI Landmarks"
    self.finishedHistoButton.name = "FinishedMRILandmarks"
    landmarksFormLayout.addWidget(self.finishedHistoButton)
    self.finishedHistoButton.connect('clicked()', landmarkManager.setMouseModeBack)
    
    self.generateMRIMaskButton = qt.QPushButton("Generate mask from MRI fiducials")
    self.generateMRIMaskButton.toolTip = "Generate a mask for the MRI volume out of the MRI landmarks"
    self.generateMRIMaskButton.name = "GenerateMRIMask"
    landmarksFormLayout.addWidget(self.generateMRIMaskButton)
    self.generateMRIMaskButton.connect('clicked()', landmarkManager.generateMRIMask)
	
	#
    # Registration Optimization
	#
	
    registrationCollapsibleButton = ctk.ctkCollapsibleButton()
    registrationCollapsibleButton.text = "Optimize Registration"
    self.layout.addWidget(registrationCollapsibleButton)
    registrationFormLayout = qt.QFormLayout(registrationCollapsibleButton)

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
  def __init__(self, parent=None):
    self.mriVolume = None
    self.histoVolume = None
    self.mriLabelmap = None
    self.histoLabelmap = None
    self.mriLandmarks = None
    self.histoLandmarks = None
    self.wholeSceneTransform = None
    self.mriTransform = None

  def loadMRI(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.mriVolume = slicer.util.getNode('*ScalarVolumeNode*')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
      
  def getMRIVolume(self):
    if self.mriVolume is not None:
      return self.mriVolume
  
  def loadHistology(self):
    volumeLoaded = slicer.util.openAddVolumeDialog()
    #if (volumeLoaded):
    self.mriVolume = slicer.util.getNode('*VectorVolumeNode*')
    if (self.checkLoaded()):
      self.alignSlices()
      self.setupTransform()
      
  def getHistologyVolume(self):
    if self.histoVolume is not None:
        return self.histoVolume

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
        volumeClipLogic.updateModelFromMarkup(slicer.util.getNode('MRI'), self.clippingModelNode)
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
        params = {'sampleDistance': 0.1, 'labelValue': 5, 'InputVolume': slicer.util.getNode('CTChest'),
                  'surface': self.clippingModelNode.GetID(), 'OutputVolume': outputLabelMap.GetID()}

        # run ModelToLabelMap-CLI Module
        slicer.cli.run(slicer.modules.modeltolabelmap, None, params, wait_for_completion=True)
        