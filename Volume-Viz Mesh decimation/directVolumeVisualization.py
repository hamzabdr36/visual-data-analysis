# ################################################################
# Import Packages
# ################################################################

import sys
import getopt
import math
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingCore import vtkColorTransferFunction
from vtkmodules.vtkRenderingCore import vtkVolumeProperty
from vtkmodules.vtkRenderingCore import vtkVolume
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper
from vtkmodules.vtkRenderingCore import vtkActor
import vtkmodules.vtkRenderingVolumeOpenGL2
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.vtkRenderingCore import vtkRenderWindow
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkCommonCore import vtkInformation
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.util import numpy_support
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from pylab import *
import os.path


def ReadInputFile(InputFilename):
    reader=None
    if InputFilename.endswith('.mhd'):
        reader=vtkMetaImageReader()
    if InputFilename.endswith('.vti'):
        reader=vtkXMLImageDataReader()
        
    reader.SetFileName(InputFilename)
    reader.Update()
    return reader.GetOutput();

def visualizeHistogram(data,gradMagnitude, bins):
    #get the arrays from the data
    x_vtkArray=data.GetPointData().GetScalars()
    y_vtkArray=gradMagnitude.GetPointData().GetScalars()

    #getting the values as np  arrays
    x= numpy_support.vtk_to_numpy(x_vtkArray)
    y= numpy_support.vtk_to_numpy(y_vtkArray)
    
    # Visualize the 2D histogram based on the number of bins
    #<Insert Code >

    #hint : matplotlib provides visualization techniques
    
    #</Insert Code>

def volumeVisualization(imageData):
    volumeMapper = vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputData(imageData)
    
# -----------------------------------------------------------------
#  Defining a Cropping Plane 
# -----------------------------------------------------------------
        
    
    volumeMapper.CroppingOn(); #enable volume Cropping
    #volumeMapper.CroppingOff(); #disable volume Cropping
    
    # compute Cropping Value
    xDim=imageData.GetDimensions()[0];
    yDim=imageData.GetDimensions()[1];
    zDim=imageData.GetDimensions()[2];
    valueX=xDim/2;
    valueY=yDim/2;
    valueZ=zDim/2;
    # Set the Cropping Values for the Mapper    
    
    #cropping along X-Axis
    volumeMapper.SetCroppingRegionPlanes(0,valueX,0,yDim,0,zDim); 
    
    #cropping along Y-Axis
    #volumeMapper.SetCroppingRegionPlanes(0,xDim,0,valueY,0,zDim);
    
    #cropping along Z-Axis
    #volumeMapper.SetCroppingRegionPlanes(0,xDim,0,yDim,0,valueZ);
    

# -----------------------------------------------------------------
# <Make changes to the transferfunction>
# -----------------------------------------------------------------
    minmax=imageData.GetScalarRange();
    # Designing the Transfer function
    volumeScalarOpacity = vtkPiecewiseFunction()

    #default <MODIFY>
    # hint : you can add as many points are necessary
    volumeScalarOpacity.AddPoint(minmax[0],    0.00)
    volumeScalarOpacity.AddPoint(minmax[1],    1.00)

    #default <MODIFY>
    # hint : you can add as many points are necessary
    volumeGradientOpacity = vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(minmax[0], 0.00)
    volumeGradientOpacity.AddPoint(minmax[1], 1.00)
    
    #Note: 
    # muliplies the scalarOpacity value with corresponding gradientOpacity value...

    # set the Colors for correspondig Regions
    #default <MODIFY>
    # hint : you can add as many points are necessary
    color = vtkColorTransferFunction();
    color.AddRGBPoint(minmax[0]     ,0.00,0.00,0.00);
    color.AddRGBPoint(minmax[1]     ,1.00,1.00,1.00);
    
    
    
    
#--------------------------------------------------------
# Rendering Pipeline 
#--------------------------------------------------------
    #create volume property 
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetColor(color)
    volumeProperty.SetInterpolationTypeToLinear()
    
    #create the volume 
    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    #create the outline
    outlineFilter=vtkOutlineFilter()
    outlineFilter.SetInputData(imageData)
    outlineFilter.Update();
    outlineMapper=vtkPolyDataMapper();
    outlineMapper.SetInputData(outlineFilter.GetOutput())
    outlineActor=vtkActor();
    outlineActor.SetMapper(outlineMapper)

    #rendering 
    render=vtkRenderer()
    render.AddVolume(volume)
    render.AddActor(outlineActor)
    window=vtkRenderWindow()
    window.AddRenderer(render)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
    interactor.Initialize()
    interactor.Start()
    
def computeGradientMagnitude(data):
    print ("Computing Gradient Magnitude...")
    
    #<Insert Code>
    #compute the gradientfield 
    
    #Hint : vtk provides a Sobel Filter 
    
    #</Insert Code>
    
    # create a vtkImage Data so we can return the gradient magnitude as vtkImageData
    sizeX=data.GetDimensions()[0];
    sizeY=data.GetDimensions()[1];
    sizeZ=data.GetDimensions()[2];
    
    tmpInfo=vtkInformation()
    image=vtkImageData()
    image.SetDimensions(data.GetDimensions())
    image.SetExtent(data.GetExtent())
    image.SetSpacing(data.GetSpacing())            
    image.SetOrigin(data.GetOrigin())    
    image.SetNumberOfScalarComponents(1,tmpInfo)
    image.AllocateScalars(tmpInfo)
    
    #iterate over each voxel and compute the gradient magnitude
    for z in range(0,sizeZ):
        for y in range(0,sizeY):
            for x in range(0,sizeX):
                magnitude=0;
                #<Insert Code>
                #compute the gradient magnitude 

                #Hint get the gradient vector and at each voxel and compute its length 
                
                #</Insert Code>
                gradMagnitude.SetScalarComponentFromDouble(x,y,z,0,magnitude)
    print ("...Done")
    return gradMagnitude

    
#Defining the Main Function 
def main(argv):    
    # define input variables
    helpstr="""directVolumeVisualization.py -i <InputFilename> """
    # parse command line
    InputFilename=None
  
    try:
        opts, args = getopt.getopt(argv,"i:")
    except getopt.GetoptError:
        print (helpstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (helpstr)
            sys.exit()
        elif opt == "-i":
            InputFilename = arg

    if InputFilename==None:
        InputFilename='headsq.vti'
        if not os.path.exists(InputFilename):
            print (helpstr)
            sys.exit(2)
# ########## Finished Parsing Agruments ##################
    
    # reading the file 
    data=ReadInputFile(InputFilename)
    print ("Data Scalar Range", data.GetScalarRange() )
    
    #computing gradient magnitude
    gradMagnitude=computeGradientMagnitude(data);
    print ("Grad Scalar Range", gradMagnitude.GetScalarRange() )
    
    #visualization
    visualizeHistogram(data,gradMagnitude,100);
    volumeVisualization(data)

    
    
#Entry point
if __name__ == "__main__":
    main(sys.argv[1:])