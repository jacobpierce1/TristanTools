# to see how these classes work together (quite nicely),
# check out ./analysis/tests/test_AttrDictSeries.py


class AttrDictSeries( object ) :

    def __init__( self, data = None )  :
        self.data = data
        self.len = len( data )
        self.keys = data[0].keys() 

    def keys( self ) :
        return self.keys

    # here is how it works: if item is one of the keys, then call it as if you
    # requested series[ item ]
    # otherwise just give the normal attribute
    # this way you don't lose access to normal attributes such as len, keys, __dict__, etc.
    def __getattr__( self, item ) :
        if item in self.keys :
            return self[ item ]
        else :
            return self.item

    def __getitem__( self, item ) :
        if isinstance( item, str ) :
            if item in self.keys :
                if isinstance( self.data[0][item], dict ) : 
                    return AttrDictSeries( [ x[item] for x in self.data ] )
                else :
                    return [ x[item] for x in self.data ]
            else :
                return self.item
        else :
            return self.data[ item ] 

    # print output 
    def __str__( self ) :
        return str( self.data ) 
        
    def __repr__( self ) :
        return str( self ) 
            




        
        
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

    # # print output 
    # def __str__( self ) :
    #     print( self.__dict__ )
        
    # def __repr__( self ) :
    #     return str( self ) 



