# -*- coding: utf-8 -*-
"""
/***************************************************************************
 zhengshiban
                                 A QGIS plugin
 zhengshiban
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by zhengshiban
        email                : zhengshiban
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QFileDialog

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .zhengshiban_dialog import zhengshibanDialog
import os.path
from qgis.core import QgsProject
from qgis.utils import iface

from osgeo import gdal_array as ga
import gdal, ogr, os, osr
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import QStringListModel 


import skimage
from skimage import io


class zhengshiban:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'zhengshiban_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&zhengshiban')



        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('zhengshiban', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/zhengshiban/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&zhengshiban'),
                action)
            self.iface.removeToolBarIcon(action)

    def fc1(self):
        print("removeAllMapLayers")

        QgsProject.instance().removeAllMapLayers()

    def fc2(self,layers):
        selectedLayerIndex = self.dlg.comboBox.currentIndex()
        print(layers[0],selectedLayerIndex)
        # selectedLayer = layers[selectedLayerIndex]
        # fields = selectedLayer.pendingFields()
        # fieldnames = [field.name() for field in fields]
        # print(fieldnames)

    def select_output_file(self):
        print("select_output_file")
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.tiff')
        # print(filename)
        self.dlg.lineEdit.setText(filename[0])


    def getfeature_select_input_filename(self):
        print("select_output_file")
        filename = QFileDialog.getOpenFileName(self.dlg, "Select input file ","", '*.tiff')
        # print(filename)
        self.dlg.lineEdit_getfeature_input.setText(filename[0])

    def getfeature_select_output_filename(self):
        print("select_output_file")
        filename = QFileDialog.getExistingDirectory(self.dlg, "Select output file ")
     
        self.dlg.lineEdit_getfeature_output.setText(filename)

    def clip_select_input_filename(self):
        print("select_output_file")
        filename = QFileDialog.getOpenFileName(self.dlg, "Select input file ","", '*.tiff')

        self.dlg.lineEdit_clip_input.setText(filename[0])

    def clip_select_output_filename(self):
        print("select_output_file")
        filename = QFileDialog.getExistingDirectory(self.dlg, "Select output file ")

        self.dlg.lineEdit_clip_output.setText(filename)
        
    def insert_my_layer(self, layers):
        """
        插入图层
        """
        selectedLayerIndex = self.dlg.comboBox.currentIndex()
        print(selectedLayerIndex)
        # selectedLayer = layers[selectedLayerIndex]

        self.dlg.listWidget.addItems(selectedLayerIndex)

    def fc2(self):
        # 坡度计算
        dem_name = self.dlg.comboBox.currentText()
        print(dem_name)
        # import qgis
        # qgis.analysis.QgsSlopeFilter("","")
        print("button 2")






    def Calculation_NDVI(self,in_filename,output_path,labeldict,Band1=1,Band2=2,save=True):

        # 文件名
        name = os.path.split(in_filename)[-1]

        
        gdal_data = gdal.Open(in_filename)

        img = gdal_data.ReadAsArray()

        save_dict={}
        for index,label in labeldict.items():
            save_dict[index] = output_path+'/'+index+'_'+name
        print(save_dict)

        if labeldict['NDVI'] == 1:
            Band1=2
            Band2=3
            output_filename = save_dict['NDVI']
            showname = os.path.split(output_filename)[-1]
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            ndvi=((arr1-arr)*1.0)/((arr1+arr)*1.0)
            ndvi1=ga.numpy.nan_to_num(ndvi)
            print("Calculation NDVI success")
            print("Calculation and save NDVI success")

         
            out=ga.SaveArray(ndvi1,save_dict['NDVI'],format = "GTiff",prototype =gdal_data)
            out=None
            iface.addRasterLayer(save_dict['NDVI'], showname)
        if labeldict['DVI'] == 1:
            output_filename = save_dict['DVI']
            showname = os.path.split(output_filename)[-1]

            Band1=2
            Band2=3
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            dvi=(arr1*1.0)/(arr*1.0)
            dvi1=ga.numpy.nan_to_num(dvi)
            
            out=ga.SaveArray(dvi1,save_dict['DVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation DVI success")
            iface.addRasterLayer(save_dict['DVI'], showname)
        if labeldict['RVI'] == 1: 
            output_filename = save_dict['RVI']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            rvi=(arr1*1.0)/(arr*1.0)
            rvi1=ga.numpy.nan_to_num(rvi)
            
            out=ga.SaveArray(rvi1,save_dict['RVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation RVI success")
            iface.addRasterLayer(save_dict['RVI'], showname)
        if labeldict['GNDVI'] == 1: 
            output_filename = save_dict['GNDVI']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            gndvi=((arr1-arr)*1.0)/((arr1+arr)*1.0)
            gndvi1=ga.numpy.nan_to_num(gndvi)
            
            out=ga.SaveArray(gndvi1,save_dict['GNDVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation GNDVI success")     
            iface.addRasterLayer(save_dict['GNDVI'], showname)
        if labeldict['NDWI'] == 1:
            output_filename = save_dict['NDWI']
            showname = os.path.split(output_filename)[-1]

            Band1=1
            Band2=3    
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            ndwi=((arr1-arr)*1.0)/((arr1+arr)*1.0)
            ndwi1=ga.numpy.nan_to_num(ndwi)
            
            out=ga.SaveArray(ndwi1,save_dict['NDWI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation NDWI success")  
            iface.addRasterLayer(save_dict['NDWI'], showname)
        if labeldict['SAVI'] == 1: 
            output_filename = save_dict['SAVI']
            showname = os.path.split(output_filename)[-1]

            Band1=2
            Band2=3
            L=0.5
            Band1=3
            Band2=1 
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            savi=((arr1-arr)*1.0)*((1+L)*1.0)/((arr1+arr+L)*1.0)
            savi1=ga.numpy.nan_to_num(savi)
            
            out=ga.SaveArray(savi1,save_dict['SAVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation SAVI success")    
            iface.addRasterLayer(save_dict['SAVI'], showname) 
        if labeldict['MSAVI'] == 1:   
            output_filename = save_dict['MSAVI']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3   
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")

            msavi=(2*arr1+1-np.sqrt((2*arr1+1)**2-8*(arr1-arr)))*0.5
            msavi1=ga.numpy.nan_to_num(msavi)
            
            out=ga.SaveArray(msavi1,save_dict['MSAVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation MSAVI success")
            iface.addRasterLayer(save_dict['MSAVI'], showname)
        if labeldict['EVI'] == 1: 
            output_filename = save_dict['EVI']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3
            Band3=0    
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            arr2=img[Band3,:,:]
            ga.numpy.seterr(all="ignore")

            evi=2.5*((arr1-arr)*1.0)/((arr1+arr*6-7.5*arr2+1)*1.0)
            evi1=ga.numpy.nan_to_num(evi)
            
            out=ga.SaveArray(evi1,save_dict['EVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation EVI success")
            iface.addRasterLayer(save_dict['EVI'], showname)
        if labeldict['ARVI'] == 1:  
            output_filename = save_dict['ARVI']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3
            Band3=0
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            arr2=img[Band3,:,:]

            ga.numpy.seterr(all="ignore")

            arvi=((arr1-(2*arr-arr2))*1.0) / ((arr1+2*arr-arr2)*1.0)

            arvi1=ga.numpy.nan_to_num(arvi)

            out=ga.SaveArray(arvi1,save_dict['ARVI'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Calculation ARVI success")   
            iface.addRasterLayer(save_dict['ARVI'], showname)

        if labeldict['Vegetation_removal'] == 1:  
            output_filename = save_dict['Vegetation_removal']
            showname = os.path.split(output_filename)[-1]
            Band1=2
            Band2=3
            img = gdal_data.ReadAsArray()
            arr=img[Band1,:,:]
            arr1=img[Band2,:,:]
            ga.numpy.seterr(all="ignore")
            ndvi=((arr1-arr)*1.0)/((arr1+arr)*1.0)
            NDVI=ga.numpy.nan_to_num(ndvi)

            NDVI_new =NDVI.copy()
            NDVI_new[NDVI_new > 0.4] = 0 
            out=ga.SaveArray(NDVI_new,save_dict['Vegetation_removal'],format = "GTiff",prototype =gdal_data)
            out=None
            print("Vegetation_removal success")   
            iface.addRasterLayer(save_dict['Vegetation_removal'], showname)                                                                      
        

    def cal_feature(self):

        print('计算特征')
        import sys


        
        #实例化列表模型，添加数据
   
        listView = self.dlg.listView
        slm = QStringListModel()
        qList = ['Item 1','Item 2','Item 3','Item 4' ]	
        slm.setStringList(qList) 
        listView.setModel(slm ) 
    
        # 
 
        label_list = ['NDVI','DVI','RVI','GNDVI','NDWI','SAVI','MSAVI','EVI','ARVI','Vegetation_removal']
        check_list = [self.dlg.checkBox_NDVI.isChecked(),
                    self.dlg.checkBox_DVI.isChecked(),
                    self.dlg.checkBox_RVI.isChecked(),
                    self.dlg.checkBox_GNDVI.isChecked(),
                    self.dlg.checkBox_NDWI.isChecked(),
                    self.dlg.checkBox_SAVI.isChecked(),
                    self.dlg.checkBox_MSAVI.isChecked(),
                    self.dlg.checkBox_EVI.isChecked(),
                    self.dlg.checkBox_ARVI.isChecked(),
                    self.dlg.checkBox_Vegetation_removal.isChecked()]
        labeldict ={}


        for i,j in zip(label_list,check_list):
            labeldict[i]=j
        
        

        in_filename = self.dlg.lineEdit_getfeature_input.text()
        output_path = self.dlg.lineEdit_getfeature_output.text()

        # todo:加警告框
        if (output_path is None) or (in_filename is None):
            print('请选择路径')
        else:
            self.Calculation_NDVI(in_filename,output_path,labeldict)




    def raster_clip(self):
        from PIL import Image
        
            
      
        in_filename = self.dlg.lineEdit_clip_input.text()
        output_path = self.dlg.lineEdit_clip_output.text()
        clip_width = self.dlg.lineEdit_clip_width.text()
        clip_height = self.dlg.lineEdit_clip_height.text()
        clip_step = self.dlg.lineEdit_clip_step.text()
        name = os.path.split(in_filename)[-1]


        imagepath = in_filename
        ds=gdal.Open(imagepath)
        wx=ds.RasterXSize
        wy=ds.RasterYSize
        
        imagepath=in_filename
        isnot_clip_label =False
        if 0:
            labelname='../data/huapo/origin/label5.tif'
            isnot_clip_label =True
        
            

    
        if isnot_clip_label: dslb=gdal.Open(labelname)
        
        stx=0
        sty=0
        step=int(clip_step)
        outsize=int(clip_width)
        nullthresh=outsize*outsize*0.7
        cx=0
        cy=0

        from PyQt5.QtWidgets import  QProgressBar
        from PyQt5.QtCore import QBasicTimer
        pbar = self.dlg.progressBar_clip

        
        bar_num = 0

        c =0
        while cy+outsize<wy:
            cx=0
            while cx+outsize<wx:
                c+=1
                cx+=step
            cy+=step

        cx=0
        cy=0
        # 秦磊修改15：26
        # 秦磊修改15：27
        while cy+outsize<wy:
            cx=0
            while cx+outsize<wx:
                pbar.setValue(bar_num)
                bar_num+=(100/c)
                img=ds.ReadAsArray(cx,cy,outsize,outsize)
                img2=img[0:3,:,:].transpose(1,2,0)
                if (img2[:,:,0]==0).sum()>nullthresh:
                    cx+=step
                    continue
   
                skimage.io.imsave(output_path+'/'+name+'_{}_{}.jpg'.format(cx,cy),img2.astype(int))
   
                #deal with label
                if isnot_clip_label:
                    img=dslb.ReadAsArray(cx,cy,outsize,outsize)
                    img=Image.fromarray(img).convert('L')
                    img.save(output_path+'/'+name+'_{}_{}.jpg'.format(cx,cy))
     
                print(cx,cy)
                cx+=step
            cy+=step
        pbar.setValue(100)

        
        

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = zhengshibanDialog()

        
        self.dlg = zhengshibanDialog()


        ###############################打开插件预处理阶段#############################################
        # 清除编辑框
        self.dlg.lineEdit.clear()
        # 绑定打开文件按钮
        self.dlg.pushButton_3.clicked.connect(self.select_output_file)
        self.dlg.pushButton.clicked.connect(self.fc1) 
        self.dlg.pushButton_2.clicked.connect(self.fc2)
        
        # 获取所有图层并存到列表里 layer_list
        layers = QgsProject.instance().mapLayers().values()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())

        # 把图层里的数据加到combox里
        self.dlg.comboBox.clear()
        self.dlg.comboBox.addItems(layer_list) 

        # 把图层显示到【文件目录】
        listView = self.dlg.listView
        slm = QStringListModel()
        qList = layer_list
        slm.setStringList(qList) 
        listView.setModel(slm ) 


        ##################################特征提取模块##########################################
        # 读取文件
        self.dlg.pushButton_getfeature_input.clicked.connect(self.getfeature_select_input_filename)
        self.dlg.pushButton_getfeature_output.clicked.connect(self.getfeature_select_output_filename)
       
        # 按钮
        self.dlg.pushButton_getfeature.clicked.connect(self.cal_feature)

        ############################################################################

        ##################################裁剪图片模块##########################################
        # 读取文件
        self.dlg.pushButton_clip_input.clicked.connect(self.clip_select_input_filename)
        self.dlg.pushButton_clip_output.clicked.connect(self.clip_select_output_filename)
       
        # 按钮
        self.dlg.pushButton_clip.clicked.connect(self.raster_clip)

        ############################################################################



        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        print(result)
        # See if OK was pressed
        if result:pass

 