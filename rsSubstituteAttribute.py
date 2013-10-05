# rsSubstituteAttribute
# @author Roberto Rubio
# @date 2013-08-03
# @file rsSubstituteAttribute.py

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginCmdRsSubsAttUI = "rsSubsAttributeUI"


##
# rs Substitute Attribute UI launch class.
# launch UI for substitute Attributes.
class rsSubsAttributeUIClass(OpenMayaMPx.MPxCommand):

    ##
    # rsSubsAttributeUI Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    ##
    # Do it function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def doIt(self, argList):
        rsSubsAttrUI()


##
# Creating instance event.
# @param none.
# @return cmdCreatorRsSubsAttUI instance
def cmdCreatorRsSubsAttUI():
    return OpenMayaMPx.asMPxPtr(rsSubsAttributeUIClass())


kPluginCmdRsSubsAtt = "rsSubsAttributeCmd"

kDelFlag = "-d"
kDelLongFlag = "-delete"


##
# rs Substitute Attributes command class.
# Launch command for substitute Attributes.
class rsSubsAttributeCmdClass(OpenMayaMPx.MPxCommand):

    ##
    # rsSubsAttributeCmd Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    ##
    # Do it function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def doIt(self, argList):
        b_flag = False
        try:
            argData = OpenMaya.MArgDatabase(self.syntax(), argList)
            b_flag = True
        except:
            print("Invalid Arguments")
            pass
        if b_flag:
            sList = OpenMaya.MSelectionList()
            argData.getObjects(sList)
            if sList.length() != 0:
                l_selectionStrings = []
                sList.getSelectionStrings(l_selectionStrings)
            b_delSrcAttr = True
            if argData.isFlagSet(kDelFlag):
                b_delSrcAttr = argData.flagArgumentBool(kDelFlag, 0)
            if sList.length() == 2:
                rsSubsParam(l_selectionStrings[0], l_selectionStrings[1], b_delSrcAttr)
            else:
                raise RuntimeError("You need 2 objects")


##
# Creating instance event.
# @param none.
# @return rsSubsAttributeCmd instance
def cmdCreatorRsSubsAtt():
    return OpenMayaMPx.asMPxPtr(rsSubsAttributeCmdClass())


# Substitute arguments creator event.
# @param none.
# @return syntax instance
def syntaxCreatorRsSubsAtt():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kDelFlag, kDelLongFlag, OpenMaya.MSyntax.kBoolean)
    syntax.useSelectionAsDefault(True)
    syntax.setObjectType(OpenMaya.MSyntax.kSelectionList)
    return syntax


##
# Load Plugin event.
# @param obj.
# @return none
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, 'Rig Studio - Developer: Roberto Rubio', '1.0', 'Any')
    try:
        mplugin.registerCommand(kPluginCmdRsSubsAttUI, cmdCreatorRsSubsAttUI)
        mplugin.registerCommand(kPluginCmdRsSubsAtt, cmdCreatorRsSubsAtt, syntaxCreatorRsSubsAtt)
        mplugin.addMenuItem("rsSubs Attribute", "MayaWindow|mainModifyMenu", "rsSubsAttributeUI()", "")
    except:
        raise RuntimeError("Failed to register command: %s\ n" % kPluginCmdRsSubsAttUI)
        raise RuntimeError("Failed to register command: %s\ n" % kPluginCmdRsSubsAtt)


##
# Unload Plugin event.
# @param obj.
# @return none
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdRsSubsAttUI)
        mplugin.deregisterCommand(kPluginCmdRsSubsAtt)
        cmds.deleteUI("MayaWindow|mainModifyMenu|rsSubs_Attribute")
    except:
        raise RuntimeError("Failed to unregister command: %s\n" % kPluginCmdRsSubsAttUI)
        raise RuntimeError("Failed to unregister command: %s\n" % kPluginCmdRsSubsAtt)


##
# rs Substitute Attribute UI class.
# Create UI for substitute Attributes.
class rsSubsAttrUI():

    ##
    # UI Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        self.name = "rsSubstituteAttribute"
        self.title = "rs Substitute Attribute"
        i_windowSize = (300, 110)
        if (cmds.window(self.name, q=1, exists=1)):
            cmds.deleteUI(self.name)
        self.window = cmds.window(self.name, title=self.title)
        s_winColPro2 = cmds.columnLayout(adjustableColumn=True, parent=self.window)
        i_colum3 = (i_windowSize[0] / 6, i_windowSize[0] * 4 / 6, i_windowSize[0] / 6)
        s_winRowField1 = cmds.rowLayout(numberOfColumns=3, adjustableColumn3=2, columnWidth3=(i_colum3), columnAlign=(1, 'center'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=s_winColPro2)
        cmds.text(label='Source', align='center', parent=s_winRowField1)
        self.sourceText = cmds.textField(cmds.textField(), edit=True, parent=s_winRowField1)
        cmds.button(label='Pick up', c=self.rsPickUpSource, parent=s_winRowField1)
        s_winRowField2 = cmds.rowLayout(numberOfColumns=3, adjustableColumn3=2, columnWidth3=(i_colum3), columnAlign=(1, 'center'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=s_winColPro2)
        cmds.text(label='Target', align='center', parent=s_winRowField2)
        self.targetText = cmds.textField(cmds.textField(), edit=True, parent=s_winRowField2)
        cmds.button(label='Pick up', c=self.rsPickUpTarget, parent=s_winRowField2)
        cmds.separator(height=5, style="none", hr=True, parent=s_winColPro2)
        i_colum = i_windowSize[0] / 3
        s_winRow1 = cmds.rowLayout(numberOfColumns=3, adjustableColumn3=2, columnWidth3=(5, i_colum, i_colum), columnAlign=(1, 'center'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=s_winColPro2)
        cmds.separator(height=5, style="none", hr=True, parent=s_winRow1)
        self.delAttr = cmds.checkBox("rsDelSourceAttr", label='Delete Source Attribute', align='right', v=True, parent=s_winRow1)
        cmds.separator(height=5, style="none", hr=True, parent=s_winColPro2)
        self.rsSubs = cmds.button(label='Substitute or Clone', w=100, c=self.rsSubs, parent=s_winColPro2)
        cmds.window(self.window, e=1, w=430, h=103)
        cmds.showWindow(self.window)
        cmds.window(self.window, edit=True, widthHeight=(i_windowSize))

    ##
    # rsPickUpSource function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def rsPickUpSource(self, *args):
        sel = cmds.ls(sl=True, o=False)
        l_channelSelect = cmds.channelBox("mainChannelBox", q=True, sma=True)
        if l_channelSelect != None:
            cmds.textField(self.sourceText, e=True, text="%s.%s" % (sel[0], l_channelSelect[0]))
        else:
            if len(sel) > 0:
                cmds.textField(self.sourceText, e=True, text=sel[0])
                cmds.warning("This tool neeed a source attribute")
            else:
                cmds.warning("Select an attribute, please")

    ##
    # rsPickUpTarget function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def rsPickUpTarget(self, *args):
        sel = cmds.ls(sl=True, o=False)
        l_channelSelect = cmds.channelBox("mainChannelBox", q=True, sma=True)
        if l_channelSelect != None:
            cmds.textField(self.targetText, e=True, text="%s.%s" % (sel[0], l_channelSelect[0]))
        else:
            if len(sel) > 0:
                cmds.textField(self.targetText, e=True, text=sel[0])
                cmds.warning("This tool will clone the source attribute If you do not specify an attribute")
            else:
                cmds.warning("Select an attribute, please")

    ##
    # rsSubs function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def rsSubs(self, *args):
        sourceText = cmds.textField(self.sourceText, q=True, tx=True)
        targetText = cmds.textField(self.targetText, q=True, tx=True)
        b_delSrcAttr = cmds.checkBox(self.delAttr, q=True, v=True)
        rsSubsParam(sourceText, targetText, b_delSrcAttr)


##
# Substitute attribute launch function.
# @param s_source - Name of the source attribute.
# @param s_target - Name of the target attribute.
# @param b_delSrcAttr - Boolean value, it indicates if source parameter will be deleted.
# @return boolean.
def rsSubsParam(s_source, s_target, b_delSrcAttr=0):
    s_parent = s_source.split(".")
    s_parentTarget = s_target.split(".")
    try:
        cmds.attributeName(s_source, l=True)
    except:
        raise RuntimeError("%s - It is not an attribute" % (s_source))
    b_att = True
    try:
        cmds.attributeName(s_target, l=True)
    except:
        b_att = False
    if b_att:
        l_attributeData = rsAttributeData(s_source)
        if l_attributeData[0][0] == "double3":
            l_attributeDataTarget = rsAttributeData(s_target)
            if l_attributeDataTarget[0][0] == "double3":
                s_sourceVec = "%s.%s" % (s_parent[0], l_attributeData[0][2])
                i_sourceLock = cmds.getAttr(s_sourceVec, lock=True)
                for i in range(len(l_attributeData)):
                    s_sourceObj = "%s.%s" % (s_parent[0], l_attributeData[i][2])
                    s_targetObj = "%s.%s" % (s_parentTarget[0], l_attributeDataTarget[i][2])
                    rsSubsParamExecute(s_sourceObj, s_targetObj, 0)
                if b_delSrcAttr == True:
                    if i_sourceLock:
                        cmds.setAttr(s_sourceVec, lock=0)
                    cmds.deleteAttr(s_sourceVec)
            else:
                cmds.warning("Source and Target types are not similar")
        else:
            rsSubsParamExecute(s_source, s_target, b_delSrcAttr)
    else:
        if cmds.objExists(s_target):
            l_attributeData = rsAttributeData(s_source)
            rsCloneAttribute(l_attributeData, s_target)
            if l_attributeData[0][0] == "double3":
                s_sourceVec = "%s.%s" % (s_parent[0], l_attributeData[0][2])
                i_sourceLock = cmds.getAttr(s_sourceVec, lock=True)
                for i in range(len(l_attributeData)):
                    s_sourceObj = "%s.%s" % (s_parent[0], l_attributeData[i][2])
                    s_targetObj = "%s.%s" % (s_target, l_attributeData[i][2])
                    rsSubsParamExecute(s_sourceObj, s_targetObj, 0)
                if b_delSrcAttr == True:
                    if i_sourceLock:
                        cmds.setAttr(s_sourceVec, lock=0)
                    cmds.deleteAttr(s_sourceVec)
            else:
                s_target = "%s.%s" % (s_target, l_attributeData[0][2])
                rsSubsParamExecute(s_source, s_target, b_delSrcAttr)
        else:
            raise RuntimeError("%s - Object do not exists" % (s_target))
    return True


##
# Substitute attribute function.
# @param s_source - Name of the source attribute.
# @param s_target - Name of the target attribute.
# @param b_delSource - Boolean value, it indicates if source parameter will be deleted.
# @return boolean.
def rsSubsParamExecute(s_source, s_target, b_delSource):
    b_argExist = True
    if not cmds.objExists(s_source) or not cmds.objExists(s_target):
        b_argExist = False
    if b_argExist:
        i_targetLock = cmds.getAttr(s_target, lock=True)
        if i_targetLock:
            cmds.setAttr(s_target, lock=0)
        l_IncomingConnections = cmds.listConnections(s_source, plugs=True, destination=False, source=True)
        l_OutcomingConnections = cmds.listConnections(s_source, plugs=True, destination=True, source=False)
        if l_IncomingConnections:
            for s_InConn in l_IncomingConnections:
                try:
                    cmds.connectAttr(s_InConn, s_target, force=True)
                    print("%s - Connected to - %s" % (s_InConn, s_target))
                except:
                    pass
        else:
            print("%s - Do not have incoming connections" % (s_source))
        if l_OutcomingConnections:
            for s_OutConn in l_OutcomingConnections:
                try:
                    cmds.connectAttr(s_target, s_OutConn, force=True)
                    print("%s - Connected to - %s" % (s_target, s_OutConn))
                except:
                    pass
        else:
            print("%s - Do not have outgoing connections" % (s_source))
        i_sourceLock = cmds.getAttr(s_source, lock=True)
        if i_sourceLock:
            cmds.setAttr(s_target, lock=1)
        if b_delSource == True:
            if i_sourceLock:
                cmds.setAttr(s_source, lock=0)
            cmds.deleteAttr(s_source)
        return True
    else:
        return False


##
# Attribute data collection function..
# @param s_oAttribute - Name of the source attribute.
# @return l_attributeData - Attribute data list.
def rsAttributeData(s_oAttribute):
    l_attributeData = []
    l_attributes = []
    try:
        s_atName = cmds.attributeName(s_oAttribute, l=True)
    except:
        raise RuntimeError("It is not an attribute")
    s_parent = s_oAttribute.split(".")[0]
    l_Siblings = ""
    l_SiblingsPa = cmds.attributeQuery(s_atName, node=s_parent, listParent=True)
    if l_SiblingsPa != None:
        s_oAttribute = "%s.%s" % (s_parent, l_SiblingsPa[0])
        s_atName = cmds.attributeName(s_oAttribute, l=True)
    l_attributes.append(s_atName)
    s_atType = cmds.getAttr(s_oAttribute, type=True)
    if s_atType == "double3":
        l_Siblings = cmds.attributeQuery(s_atName, node=s_parent, listChildren=True)
        for o_sib in l_Siblings:
            l_attributes.append(o_sib)
    for s_atName in l_attributes:
        s_oAttribute = "%s.%s" % (s_parent, s_atName)
        s_atType = cmds.getAttr(s_oAttribute, type=True)
        s_atNiceName = cmds.attributeQuery(s_atName, node=s_parent, niceName=True)
        i_atLock = cmds.getAttr(s_oAttribute, lock=True)
        l_attributeDataTemp = [s_atType, s_parent, s_atName, s_oAttribute, s_atNiceName, i_atLock]
        if s_atType == "string":
            s_stringValue = cmds.getAttr(s_oAttribute)
            l_attributeDataTemp.append(s_stringValue)
            return (l_attributeDataTemp, None)
        i_atKey = cmds.getAttr(s_oAttribute, keyable=True)
        i_atHidden = cmds.getAttr(s_oAttribute, channelBox=True)
        l_attributeDataTemp.append(i_atKey)
        l_attributeDataTemp.append(i_atHidden)
        if s_atType == "enum":
            s_enum = (cmds.attributeQuery(s_atName, node=s_parent, listEnum=True))[0]
            l_enum = s_enum.split(':')
            l_attributeDataTemp.append(l_enum)
            return (l_attributeDataTemp, None)
        if s_atType != "double3":
            s_hasMin = cmds.addAttr(s_oAttribute, query=True, hasMinValue=True)
            f_atMinValue = 0
            if s_hasMin:
                f_atMinValue = (cmds.attributeQuery(s_atName, node=s_parent, minimum=True))[0]
            s_hasMax = cmds.addAttr(s_oAttribute, query=True, hasMaxValue=True)
            f_atMaxValue = 0
            if s_hasMax:
                f_atMaxValue = (cmds.attributeQuery(s_atName, node=s_parent, maximum=True))[0]
            f_atDefValue = (cmds.attributeQuery(s_atName, node=s_parent, listDefault=True))[0]
            l_rest = [s_hasMin, f_atMinValue, s_hasMax, f_atMaxValue, f_atDefValue]
            l_attributeDataTemp.extend(l_rest)
        l_attributeData.append(l_attributeDataTemp)
    return (l_attributeData)


##
# Clone attribute function..
# @param l_attributeData - Attribute data list.
# @param s_target - Object target to clone data.
# @return boolean.
def rsCloneAttribute(l_attributeData, s_target):
    s_oAtt = "%s.%s" % (s_target, l_attributeData[0][2])
    if cmds.objExists(s_oAtt):
        s_sepName = ""
        b_inAndOut = False
        l_IncomingConnections = cmds.listConnections(s_oAtt, plugs=True, destination=False, source=True)
        l_OutcomingConnections = cmds.listConnections(s_oAtt, plugs=True, destination=True, source=False)
        if l_IncomingConnections or l_OutcomingConnections:
            b_inAndOut = True
        if not b_inAndOut:
            cmds.deleteAttr(s_oAtt)
        else:
            s_sepName = l_attributeData[0][2]
            s_sepNameBase = s_sepName
            o_objParam = "%s.%s" % (s_target, s_sepName)
            i = 1
            while cmds.objExists(o_objParam):
                s_sepName = s_sepNameBase + str(i)
                o_objParam = "%s.%s" % (s_target, s_sepName)
                i = i + 1
            cmds.warning("You have one attribute with some connections and same name - This plugin will create another attribute named - %s" % (s_sepName))
        if s_sepName != "":
            l_attributeData[0][2] = s_sepName
    l_sel = cmds.ls(sl=True, o=False)
    cmds.select(s_target, r=True)
    f_NewValue = ""
    if l_attributeData[0][0] != 'enum' and l_attributeData[0][0] != "double3" and l_attributeData[0][0] != "string":
        f_NewValue = l_attributeData[0][12]
    if f_NewValue != "":
        cmds.addAttr(longName=l_attributeData[0][2], niceName=l_attributeData[0][4], attributeType=l_attributeData[0][0], hasMinValue=l_attributeData[0][8], hasMaxValue=l_attributeData[0][10], defaultValue=f_NewValue)
    else:
        if l_attributeData[0][0] == 'enum':
            s_enumList = ""
            for s_string in l_attributeData[0][8]:
                s_enumList = s_enumList + s_string + ":"
            cmds.addAttr(longName=l_attributeData[0][2], niceName=l_attributeData[0][4], attributeType=l_attributeData[0][0], en=s_enumList)
        if l_attributeData[0][0] == "string":
            cmds.addAttr(longName=l_attributeData[0][2], niceName=l_attributeData[0][4], dt=l_attributeData[0][0])
            cmds.setAttr("%s.%s" % (s_target, l_attributeData[0][2]), l_attributeData[0][6], type=l_attributeData[0][0])
        if l_attributeData[0][0] == 'double3':
            cmds.addAttr(longName=l_attributeData[0][2], niceName=l_attributeData[0][4], attributeType=l_attributeData[0][0])
            for i in range(1, len(l_attributeData)):
                cmds.addAttr(longName=l_attributeData[i][2], niceName=l_attributeData[i][4], attributeType="double", p=l_attributeData[0][2], hasMinValue=l_attributeData[i][8], hasMaxValue=l_attributeData[i][10])
            for i in range(1, len(l_attributeData)):
                s_NewAt = s_target + "." + l_attributeData[i][2]
                if l_attributeData[i][6]:
                    cmds.setAttr(s_NewAt, keyable=True, channelBox=False)
                if not l_attributeData[i][6] and l_attributeData[i][7]:
                    cmds.setAttr(s_NewAt, keyable=False, channelBox=True)
                if not l_attributeData[i][6] and not l_attributeData[i][7]:
                    cmds.setAttr(s_NewAt, keyable=False, channelBox=False)
    s_NewAt = s_target + "." + l_attributeData[0][2]
    if l_attributeData[0][0] != 'enum' and l_attributeData[0][0] != "double3" and l_attributeData[0][0] != "string":
        if l_attributeData[0][10]:
                cmds.addAttr(s_NewAt, edit=True, maxValue=l_attributeData[0][11])
        if l_attributeData[0][8]:
            cmds.addAttr(s_NewAt, edit=True, minValue=l_attributeData[0][9])
    if l_attributeData[0][6]:
        cmds.setAttr(s_NewAt, keyable=True, channelBox=False)
    if not l_attributeData[0][6] and l_attributeData[0][7]:
        cmds.setAttr(s_NewAt, keyable=False, channelBox=True)
    if not l_attributeData[0][6] and not l_attributeData[0][7]:
        cmds.setAttr(s_NewAt, keyable=False, channelBox=False)
    cmds.setAttr(l_attributeData[0][3], lock=l_attributeData[0][5])
    cmds.select(l_sel, r=True)
    return True
