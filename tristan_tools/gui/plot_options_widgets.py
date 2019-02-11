# here are the classes for custom settings for each plot, accessed by
# clicking the options button .


from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIntValidator


import time 



def int2checkstate( x ) :
    if x == 0 :
        return x
    else :
        return 2




class MPLPlotOptionsWidget( QWidget ) :

    def __init__( self, plotter, set_current_values = 1 ) :

        super().__init__()

        if set_current_values :
            self.set_current_values() 


    def set_current_values( self ) :
        pass 


            

class MayaviPlotOptionsWidget( QWidget ) :

    # plotter is a Plotter subclass, defined in tristan_data_plotter.
    def __init__( self, plotter, set_current_values = 1 ) :
        
        super().__init__()
        self.plotter = plotter 

        layout = QFormLayout()
        self.setLayout( layout )


        checkbox_functions = [ self.set_orientation_axes,
                               self.set_outline ]
        
        checkbox_descriptions = [ 'Toggle Orientation Axes',
                                  'Toggle Outline' ] 

        checkboxes = [ QCheckBox() for i in range( len( checkbox_functions ) ) ]

        ( self.orientation_axes_checkbox,
          self.outline_checkbox ) = checkboxes 
        
        for i in range( len( checkbox_functions ) ) :
            checkboxes[i].clicked.connect( checkbox_functions[i] ) 
            layout.addRow( checkbox_descriptions[i], checkboxes[i] ) 

        # must be set to 0 for subclasses 
        if set_current_values : 
            self.set_current_values() 
            
        
    def set_orientation_axes( self ) :
        state = self.orientation_axes_checkbox.checkState()
        self.plotter.set_orientation_axes( state ) 


    def set_outline( self ) :
        state = self.outline_checkbox.checkState()
        self.plotter.set_outline( state ) 
    
    
    def set_current_values( self ) :
        self.orientation_axes_checkbox.setCheckState( int2checkstate( self.plotter.orientation_axes_state ) )
        self.outline_checkbox.setCheckState( int2checkstate( self.plotter.outline_state ) )

        
    


    
        
class VolumeSliceOptionsWidget( MayaviPlotOptionsWidget ) :

    def __init__( self, plotter ) :
        super().__init__( plotter, 0 )

        layout = self.layout()

        self.slice_checkboxes = [ QCheckBox() for i in range(3) ]
        labels = [ s + ' Slice: ' for s in [ 'x', 'y', 'z' ] ]

        for i in range(3) :
            self.slice_checkboxes[i].clicked.connect( lambda state, a=i : self.set_slice( a ) )
            layout.addRow( labels[i], self.slice_checkboxes[i] ) 

        self.set_current_values() 

        
    def set_current_values( self ) :
        super().set_current_values() 

        # add slice states 
        for i in range(3) :

            # excuse my (elegant) abstruseness
            slice_active = not not self.plotter.mayavi_plots[i] 
            self.slice_checkboxes[i].setCheckState( int2checkstate( slice_active ) )
        
        
    def set_slice( self, i ) :
        state = self.slice_checkboxes[i].checkState()
        if state:
            self.plotter.add_slice( i )
        else :
            self.plotter.remove_slice( i ) 
        

    


# class Quiver3DOptionsWidget( PlotOptionsWidget ) :

#     def __init__( self, plotter ) :
#         super().__init__( plotter, 0 ) 


class VectorFieldOptionsWidget( MayaviPlotOptionsWidget ) :

    def __init__( self, plotter ) :
        super().__init__( plotter, 0 )

        layout = self.layout()
        self.mask_points_entry = QLineEdit()
        self.mask_points_entry.setValidator( QIntValidator() )
        self.mask_points_entry.returnPressed.connect( self.set_mask_points ) 

        layout.addRow( 'Mask Points', self.mask_points_entry ) 
        
        self.set_current_values() 


    def set_current_values( self ) :
        super().set_current_values()
        self.mask_points_entry.setText( str( self.plotter.get_mask_points() ) ) 


    def set_mask_points( self ) :
        mask_points = int( self.mask_points_entry.text() )
        self.plotter.set_mask_points( mask_points ) 



        


class VectorCutPlaneOptionsWidget( MayaviPlotOptionsWidget ) : 

    def __init__( self, plotter ) :
        super().__init__( plotter, 0 )
        layout = self.layout()

        self.slice_checkboxes = [ QCheckBox() for i in range(3) ]
        labels = [ s + ' Slice: ' for s in [ 'x', 'y', 'z' ] ]

        for i in range(3) :
            self.slice_checkboxes[i].clicked.connect( lambda state, a=i : self.set_slice( a ) )
            layout.addRow( labels[i], self.slice_checkboxes[i] ) 


        # text entries
        entries = []
        callbacks = [ self.set_mask_points, self.set_scale_factor ]
        descriptions = [ 'Mask points', 'Scale factor' ]
        for i in range(2) : 
            x = QLineEdit()
            x.setValidator( QIntValidator() )
            x.returnPressed.connect( callbacks[i] ) 
            layout.addRow( descriptions[i], x ) 
            entries.append(x) 
            
        self.mask_points_entry, self.scale_factor_entry = entries 

        self.set_current_values()


        
    def set_current_values( self ) :
        super().set_current_values()

        # add slice states 
        for i in range(3) :
            slice_active = not not self.plotter.mayavi_plots[i] 
            self.slice_checkboxes[i].setCheckState( int2checkstate( slice_active ) )

        self.mask_points_entry.setText( str( self.plotter.get_mask_points() ) ) 


        
    def set_mask_points( self ) :
        mask_points = int( self.mask_points_entry.text() )
        self.plotter.set_mask_points( mask_points ) 


    def set_scale_factor( self ) :
        scale_factor = int( self.scale_factor_entry.text() )
        self.plotter.set_scale_factor( scale_factor ) 

            
    def set_slice( self, i ) :
        state = self.slice_checkboxes[i].checkState()
        if state:
            self.plotter.add_slice( i )
        else :
            self.plotter.remove_slice( i ) 
        





class VolumeOptionsWidget( MayaviPlotOptionsWidget ) : 

    def __init__( self, plotter ) :
        super().__init__( plotter, 0 )

        layout = self.layout()

        labels = [ 'vmin', 'vmax' ]
        callbacks = [ self.set_vmin, self.set_vmax ] 
        entries = [] 

        for i in range(2) : 
            x = QLineEdit()
            x.setValidator( QIntValidator() )
            x.returnPressed.connect( callbacks[i] ) 
            layout.addRow( labels[i], x )
            entries.append(x) 

        self.vmin_entry, self.vmax_entry = entries 
            
        self.set_current_values() 


    def set_current_values( self ) :
        super().set_current_values()
        # self.mask_points_entry.setText( str( self.plotter.get_mask_points() ) ) 


    def set_vmin( self ) :
        vmin = int( self.vmin_entry.text() )
        self.plotter.set_vmin( vmin )

        
    def set_vmax( self ) :
        vmax = int( self.vmax_entry.text() )
        self.plotter.set_vmax( vmax ) 









        
class Hist1dOptionsWidget( MPLPlotOptionsWidget  ) : 

    def __init__( self, plotter ) :
        super().__init__( plotter, 0 )
        layout = self.layout() 

        self.set_current_values()


    def set_current_values( self ) :
        

        super().set_current_values()
        









        
# class VectorCutPlaneOptionsWidget( PlotOptionsWidget ) : 

#     def __init__( self ) :
#         super().__init__( plotter, 0 )
#         layout = self.layout() 

#         self.set_current_values()


#     def set_current_values( self ) :
        

#         super().set_current_values()
        
