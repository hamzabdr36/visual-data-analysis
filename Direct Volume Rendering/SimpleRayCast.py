

#!/usr/bin/env python

# noinspection PyUnresolvedReferences
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper

from timeit import default_timer as timer

class FpsObserver:
    '''Counts the number of frames rendered by the given renderer
    and writes the resulting fps to the terminal once a second.'''
    def __init__(self, renderer, x=0, y=0):
        self.mRenderer = renderer
        self.mRenderer.AddObserver(vtkCommand.EndEvent, self)       
        
        self.mFrameCount    = 0         # Number of frames collected since last FPS was calculated.
        self.mStartTime     = timer()   # The last time FPS was calculated.
        self.mFpsUpdateRate = 1         # How often to update FPS in seconds.
        
    def __call__(self, caller, event):
        if event == "EndEvent":
            self.mFrameCount = self.mFrameCount + 1
            
            if timer() - self.mStartTime > self.mFpsUpdateRate:
                _currentTime     = timer()
                _duration        = _currentTime - self.mStartTime
                
                _fps = self.mFrameCount/_duration
                print("fps={:.3f}".format(_fps))
                
                self.mStartTime  = _currentTime
                self.mFrameCount = 0

class MyInteractorStyle(vtkInteractorStyleTrackballCamera):
    '''Custom interactor that adjusts the given volumeProperty when user
    presses certain keys. TFList should be a list whose items are pairs of
    color and opacity transfer functions. It will be cycled over when
    user presses 't'.
    The render window is passed in so that we can trigger updates.'''
    def __init__(self,renWin,volumeProperty,TFList):
        # Initialize parent class
        super().__init__()
        self.AddObserver('CharEvent', self.OnChar)
        self.mRenWin = renWin
        self.mVolumeProperty = volumeProperty
        self.mTFList = TFList
        self.mIndex = 0
        self.mNearest = False
        
    def OnChar(self, obj, event):
        key = obj.GetInteractor().GetKeySym()
        if key == 't' or key == 'T':
            self.mIndex = (self.mIndex+1) % len(self.mTFList)
            print("Switching to transfer function #" + str(self.mIndex))
            self.mVolumeProperty.SetColor(self.mTFList[self.mIndex][0])
            self.mVolumeProperty.SetScalarOpacity(self.mTFList[self.mIndex][1])
        elif key == 'i' or key == 'I':
            self.mNearest = not self.mNearest
            interpolation_type = "Nearest Neighbor" if self.mNearest else "Trilinear"
            print("Interpolation Type: " + interpolation_type)
            self.mVolumeProperty.SetInterpolationType(0 if self.mNearest else 1)
        self.mRenWin.Render()
        super(MyInteractorStyle, self).OnChar()


def ReadInputFile(InputFilename):
    '''Read input, selecting reader class based on file extension'''
    reader=None
    if InputFilename.endswith('.mhd'):
        reader=vtkMetaImageReader()
    if InputFilename.endswith('.vti'):
        reader=vtkXMLImageDataReader()
    if InputFilename.endswith('.vtk'):
        reader=vtkStructuredPointsReader()
    if reader:
        reader.SetFileName(InputFilename)
        reader.Update()
    return reader

def main():
    fileName = get_program_parameters()
    colors = vtkNamedColors()

    # This framework is based on VTK's simple volume rendering example that
    # uses a vtkFixedPointVolumeRayCastMapper

    # Create a renderer, render window, and interactor.
    ren1 = vtkRenderer()

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)

    # Show frames per second
    fpsObserver = FpsObserver(ren1)
    
    # Create the reader for the data.
    reader = ReadInputFile(fileName)
    
    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0, 0.0, 0.667, 0.0)
    colorTransferFunction.AddRGBPoint(96, 0.925, 0.463, 0.0)
    colorTransferFunction.AddRGBPoint(130, 0.667, 0.463, 0.0)
    colorTransferFunction.AddRGBPoint(255, 0.376, 0.188, 0.0)


    # Create transfer mapping scalar value to opacity.
    opacityTransferFunction = vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0, 0.0)
    opacityTransferFunction.AddPoint(255, 1.0)

   
    newOpacityTransferFunction = vtkPiecewiseFunction()
    newOpacityTransferFunction.AddPoint(10, 0.0)
    newOpacityTransferFunction.AddPoint(35, 0.0)
    newOpacityTransferFunction.AddPoint(50, 0.50, )
    #newOpacityTransferFunction.AddPoint(200, 1.0)
    #newOpacityTransferFunction.AddPoint(255, 1.0)


    

    # available transfer functions
    TFList=[]
    TFList.append((colorTransferFunction,opacityTransferFunction))
    TFList.append((colorTransferFunction, newOpacityTransferFunction))
    
    # The property describes how the data will look.
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    # The mapper / ray cast function know how to render the data.
    volumeMapper = vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())
    volumeMapper.SetAutoAdjustSampleDistances(1)

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # Actors are added to the renderer.
    ren1.AddVolume(volume)
    ren1.SetBackground(colors.GetColor3d("Wheat"))

    # The renderer is added to the render window.
    renWin.SetSize(600, 600)
    renWin.Render()

    # The custom interactor style.
    style = MyInteractorStyle(renWin,volumeProperty,TFList)

    print("Press 't' to toggle transfer function.")
    print("Press 'i' toggle between trilinear and nearest neighbor interpolation.")
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.SetInteractorStyle(style)

    # Initialize the event loop and then start it.
    iren.Initialize()
    iren.Start()

def get_program_parameters():
    import argparse
    description = 'Basic Volume Rendering Demo.'
    epilogue = '''
     This is a simple volume rendering example that uses a vtkFixedPointVolumeRayCastMapper.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue)
    parser.add_argument('--filename', help='bonsai.vti')
    args = parser.parse_args()
    return "bonsai.vti"


if __name__ == '__main__':
    main()

