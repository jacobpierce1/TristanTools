
import numpy as np



# used for arbitrary position and momentum cuts 
class TristanCut() :


    # possibilities for cut :
    # None
    # [ [None, right], [left,right], [None,None] ]
    # etc
    
    def __init__( self, cuts = None, dim = 3 ) :

        if cuts is None :
            # cuts = [ [ None, None ] for i in range( dim ) ]
            cuts = np.zeros( ( dim, 2 ), dtype = object )
            cuts[:] = None
            
        self.cuts = cuts
        # self.mask = None

    def __len__( self ) :
        return len( self.cuts ) 
        
    def check_cut( self, cut ) :

        if cut is None :
            return

        if len( cut) != 2 :
            raise KeyError( 'ERROR: attempted to set a cut with length != 2' )

        if ( cut[0] is not None ) and ( cut[1] is not None ) and ( cut[0] > cut[1] ) : 
            print( 'WARNING: the specified cut will always fail: ' + str( cut ) )



    def check_cuts( self ) :
        for i in range( len (self ) ) :
            self.check_cut( self.cuts[i] )
                        
    def __getitem__( self, idx ) :
        return self.cut[ idx ]

    def __setitem__( self, idx, item ) :
        self.check_cut( item ) 
        self.cut[idx] = item 

    def encode( self ) :
        arr = np.array( self.cuts ) 

        for i in range( len( arr ) ) :
            if arr[i][0] == None :
                self.arr[i][0] = -np.inf
            if arr[i][1] == None :
                self.arr[i][1] = np.inf


                
    def set( self, cut_array ) :
        self.cuts[:] = cut_array
        self.check_cuts() 

        
    @classmethod
    def decode( cls, arr ) :
        for i in range( len( arr ) ) :
            if arr[i][0] == -np.inf :
                self.arr[i][0] = None
            if arr[i][1] == -np.inf :
                self.arr[i][1] = None

        return cls( arr ) 
        

    
    def apply( self, _array ) : 
        mask = np.ones( len( _array[0] ), dtype = bool )
        for i in range( len( self.cuts ) ) :
            if self.cuts[i][0] is not None :
                mask &= ( _array[i] >= self.cuts[i][0] )
            if self.cuts[i][1] is not None :
                mask &= ( _array[i] <= self.cuts[i][1] )

        return mask


    
    def __str__( self ) :
        return str( self.cuts )

                          
