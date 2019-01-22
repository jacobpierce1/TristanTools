
class RecursiveSeries( object ) :

    def __init__( self, data = None )  :
        self.data = data 

    def __getitem__( self, item ) :
        if isinstance( item, str ) :
            return RecursiveSeries( [ x[item] for x in self.data ] )
        else :
            return self.data[ item ] 


            
# data container for all tristan data.
# i didn't test the efficiency of this vs. a named tuple, but this should be at least as fast
# with slightly worse memory usage. the point is that you can do:
# x = AttrDict()
# x.a = 2
# x['a'] --> returns 2
# x.a --> returns 2 
# see https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
class AttrDict( dict ):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        



