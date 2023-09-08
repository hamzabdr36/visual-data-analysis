# ################################################################
# Import Packages
# ################################################################
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPlaneCollection
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkProperty,
    vtkRenderer,
)

import sys
import getopt

def ReadInputFile(InputFilename):
    reader = vtkXMLImageDataReader()
    reader.SetFileName(InputFilename)
    reader.Update()
    return reader.GetOutput()

def CreateVisualizationFromListOfActors(ListOfActors):
    #create a renderer
    render = vtkRenderer()
    #Add the Actors to Renderer
    for i in range(0,len(ListOfActors)):
        render.AddActor(ListOfActors[i]);
    #Create Render Window
    window = vtkRenderWindow()
    window.AddRenderer(render)
    #Create Interactor
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
    interactor.Initialize()
    interactor.Start()

def task1(InputData):
    # create a BoundingBox using 
    # vtkOutlineFilter 
    # vtkPolyDataMapper
    # vtkActor 
   
    # <Insert Code >

    outActor = vtkActor()
    # <Insert Code> 

    #return the actor
    return outActor
  
def task2(InputData):
    #create a contour using contourFilter
    # <Insert Code >
   
    bonesActor = vtkActor()
    # <Insert Code>

    #return the actor
    return bonesActor
    
def task3(InputData):
    #create a contour using contourFilter
    # <Insert Code>

    skinnActor = vtkActor()
    # <Insert Code>

    #return the actor
    return skinnActor



#Defining the Main Function 
def main(argv):
    # define input variables
    helpstr = """IntroVtkPython.py -i <InputFilename> [optional -b <ShowBoundingBox>]"""
    # parse command line
    InputFilename = None
    ShowBBoxInStr = None
    ShowBBox = 0
    try:
        opts, args = getopt.getopt(argv,"i:b:")
    except getopt.GetoptError:
        print (helpstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (helpstr)
            sys.exit()
        elif opt == "-i":
            InputFilename = arg
        elif opt == "-b":
            ShowBBoxInStr = arg

    if InputFilename==None:
        print (helpstr)
        sys.exit(2)
    if ShowBBoxInStr=="true":
        ShowBBox = 1

    # ######################################
    # Finished Parsing Agruments
    # ######################################

    # reading the file
    data = ReadInputFile(InputFilename)
    #adding the actors to A List Of Actors
    ListOfActors = []
    BboxActor    = task1(data)
    BonesActor   = task2(data)
    SkinActor    = task3(data)
    # disable the visibility of the BboxActor when
    # the boundingbox should not be shown
    # <Insert Code>

    #adding the actors to A List Of Actors
    ListOfActors = []
    ListOfActors.append(BboxActor)
    ListOfActors.append(BonesActor)
    ListOfActors.append(SkinActor)
   
    # create visualization and interaction 
    CreateVisualizationFromListOfActors(ListOfActors)
    
#Entry point
if __name__ == "__main__":
    main(sys.argv[1:])

    
