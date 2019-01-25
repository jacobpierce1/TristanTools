# to see how these classes work together (quite nicely),
# check out ./analysis/tests/test_AttrDictSeries.py

import sys 


class RecursiveAttrDict( dict ) : 

    # pythonic style: give user the option of creating a recursive dict if they
    # already had the appropriate data structure stored.
    # also allows you to create an object with no keys. compare to empty,
    # which does the same thing but also allows you to populate with a list of key names
    def __init__( self, data = None, size = 0 ) :

        if data is None :
            data = {} 

        self.data = data 
        # self.__keys = list( data.keys() )
        if self.data : 
            self.size = len( next( iter( data.values() ) ) )

        else : 
            self.size = size
            
        self.check_good() 


    # here is how it works: if item is one of the keys, then call it as if you
    # requested series[ item ]
    # otherwise just give the normal attribute
    # this way you don't lose access to normal attributes such as len, keys, __dict__, etc.
    def __getattr__( self, item ) :
        if item in self.data.keys() :
            return self[ item ]
        else :
            return self.item

            
    def __getitem__( self, item ) :
        if isinstance( item, str ) :
            # if item in self.data.keys() :
            #     if isinstance( self.data[item], dict ) : 
            #         return AttrDictSeries( [ x[item] for x in self.data ] )
            #     else :
            #         return [ x[item] for x in self.data ]

            # if item in self.data.keys() :
            #     return self.data[ item ] 
            
            # else :
            #     return self.item
            return self.data[ item ]  
            
        # otherwise assume it's an and apply the index
        else :
            return { key : val[ item ] for key, val in self.data.items() }

            
    # check if all the arrays have the same length and all the keys are strings
    # terminate program if not .       
    def check_good( self ) :
        for key in self.data.keys() :
            if not isinstance( key, str ) :
                # return 0
                print( 'ERROR: all data keys for RecursiveDict must be strings' )
                sys.exit(1)
                
            if len( self.data[ key ] ) != self.size :
                print( 'ERROR: arrays don\'t all have same len' )
                sys.exit( 1 )  


    # set a key equal to data. the key used can also be a new key not
    # already in self.data
    def set_key( self, key, data = None ) :
        if data is None :
            data = [ None for i in range( self.size ) ] 
        self.data[ key ] = data

        
    # create an empty RecursiveDict
    @classmethod
    def empty( cls, keys = None, size = 0 ) :         
        if keys is None :
            keys = [] 

        data = dict( keys )
        for key in keys :
            data[ key ] = [ None for i in range(size) ] 

        return cls( data, size = size ) 
            
            
    def keys( self ) :
        return self.data.keys()

    def __len__( self ) :
        return len( data )     

    def __str__( self ) :
        return str( self.data ) 
        
    def __repr__( self ) :
        return str( self ) 

    def __len__( self ) :
        return len( self.data ) 





        
        
# data container for the params. example usage: 
# x = AttrDict()
# x.a = 2
# x['a'] --> returns 2
# x.a --> returns 2 
# see https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
class AttrDict( dict ):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self







# # stores a sequence of dicts with the same keys in self.data
# # and the keys of these dicts (not checked to be the same, this is
# # the user's responsibility) in self.__keys. if 'x' is a key, then
# # self.x and self['x'] both return an array with self.data evaluated
# # at ['x']. 

# class AttrDictSeries( object ) :

#     def __init__( self, data = None )  :
#         self.data = data
#         # self.len = len( data )
#         if data : 
#             self.__keys = data[0].keys() 
#         else :
#             self.__keys = None

            
#     def keys( self ) :
#         return self.__keys

#     # here is how it works: if item is one of the keys, then call it as if you
#     # requested series[ item ]
#     # otherwise just give the normal attribute
#     # this way you don't lose access to normal attributes such as len, keys, __dict__, etc.
#     def __getattr__( self, item ) :
#         if item in self.__keys :
#             return self[ item ]
#         else :
#             return self.item

            
#     def __getitem__( self, item ) :
#         if isinstance( item, str ) :
#             if item in self.__keys :
#                 if isinstance( self.data[0][item], dict ) : 
#                     return AttrDictSeries( [ x[item] for x in self.data ] )
#                 else :
#                     return [ x[item] for x in self.data ]
#             else :
#                 return self.item
#         else :
#             return self.data[ item ] 

#     @classmethod
#     def empty( self, keys = None ) : 
        
        
#     # set the keys that are used for recursive indexing
#     def set_keys( self, keys ) :
#         self.__keys = keys 

#     # for usage with built in python functions 
#     def __str__( self ) :
#         return str( self.data ) 
        
#     def __repr__( self ) :
#         return str( self ) 

#     def __len__( self ) :
#         return len( self.data ) 

        



