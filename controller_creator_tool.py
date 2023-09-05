import maya.cmds as cmds

def addGeoSuffix():
    sel = cmds.ls(selection=True)
    
    for obj in sel:
        cmds.rename(obj, obj + '_geo')
        
def addSuffix():
    sel = cmds.ls(selection=True)
    
    for obj in sel:
        cmds.rename(obj, obj + '_jnt')

def createOffsetGroups():
    sel = cmds.ls(selection=True)

    for obj in sel:
        groupName = obj + "_off"
        cmds.createNode("transform", name=groupName)
        cmds.delete(cmds.parentConstraint(obj, groupName))
        cmds.parent(obj, groupName)

def createCurveControllers():
    sel = cmds.ls(selection=True)

    for obj in sel:
        ctrlName = obj.replace("jnt", "cc")
        curve = cmds.circle(n=ctrlName, ch=False)
        groupName = ctrlName + "_off"
        cmds.createNode("transform", name=groupName)
        cmds.parent(curve[0], groupName)
        cmds.delete(cmds.parentConstraint(obj, groupName))
        cmds.parentConstraint(curve[0], obj)
        
        # Get the selected color from the color picker
        rgb_values = cmds.colorSliderGrp(color_slider, query=True, rgbValue=True)
        color_index = getColorIndex(rgb_values)
        
        # Apply the color to the curve controller
        cmds.setAttr(curve[0] + ".overrideEnabled", 1)
        cmds.setAttr(curve[0] + ".overrideColor", color_index)
        
        # Get the selected scale value from the slider
        scale_value = cmds.floatSliderGrp(scale_slider, query=True, value=True)
        
        # Apply the scale to the curve controller
        cmds.scale(scale_value, scale_value, scale_value, curve[0])

def updateColorIndex(value):
    # Update the color index when the color picker is changed
    rgb_values = cmds.colorSliderGrp(color_slider, query=True, rgbValue=True)
    index = getColorIndex(rgb_values)
    cmds.colorSliderGrp(color_slider, edit=True, value=index)

def getColorIndex(rgb_values):
    # Get the color index from the RGB values
    color_index = 0
    if rgb_values[0] == 0.0 and rgb_values[1] == 0.0 and rgb_values[2] == 0.0:
        color_index = 1
    elif rgb_values[0] == 1.0 and rgb_values[1] == 1.0 and rgb_values[2] == 1.0:
        color_index = 0
    return color_index

# Make a new window
window = cmds.window(title="Control Creator", widthHeight=(500, 500))
cmds.columnLayout(adjustableColumn=True)
cmds.separator(height=10, style='none')
cmds.button(label='Add _geo suffix', command='addGeoSuffix()')
cmds.separator(height=10, style='none')
cmds.button(label='Add _jnt Suffix', command='addSuffix()')
cmds.separator(height=10, style='none')
cmds.button(label='Create Offset Groups', command='createOffsetGroups()')
cmds.separator(height=10, style='none')

cmds.text(label='Curve Controller Color:')
# Create a color picker for choosing the color
color_slider = cmds.colorSliderGrp(label="Color", rgb=(1, 1, 1), columnWidth=(1, 70),
                                   changeCommand='updateColorIndex')

cmds.separator(height=10, style='none')

cmds.text(label='Curve Controller Scale:')
# Create a slider for adjusting the scale
scale_slider = cmds.floatSliderGrp(label="Scale", field=True, minValue=0.1, maxValue=5.0, value=1.0, 
                                   columnWidth=(1, 70))
cmds.separator(height=10, style='none')
cmds.button(label='Create Curve Controllers', command='createCurveControllers()')
cmds.separator(height=10, style='none')

cmds.setParent('..')
cmds.showWindow(window)
