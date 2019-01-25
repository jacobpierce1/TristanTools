import tristan_tools.analysis as analysis 


# this demonstrates how to use the RecursiveSeries together with the AttrDict
# this setup is useful in its own right, but is also the superclass of the
# TristanDataContainer, so it's important to understand how it works in order
# to use this API .

data = { 'a' : [ i for i in range(10) ],
         'b' : [ 0  for i in range(10) ]   } 

recursive_attr_dict = analysis.RecursiveAttrDict( data )

print( '\nThe whole recursive series:' ) 
print( recursive_attr_dict ) 
print( len( recursive_attr_dict ) ) 

print( '\nAccessing index 5:' )
print( recursive_attr_dict[5] ) 


print( '\nNote that AttrDict is a subclass of dict' )
print( type( recursive_attr_dict[5] ) ) 
print( isinstance( recursive_attr_dict[5], dict ) ) 
print( recursive_attr_dict[5].keys() ) 

print( '\nConstructing new recursive series from attributes a and b:' )
print( recursive_attr_dict['a'] ) 
print( recursive_attr_dict['b'] ) 


print( '\nAlternatively, access the attributes as if it is an instance of the class:' )
print( recursive_attr_dict.a ) 
print( recursive_attr_dict.b ) 

print( '\nNote that if there is no recursive series that can be constructed (i.e. recursive_attr_dict.a is not a series of dicts or AttrDicts), then a list will automatically be returned rather than another AttrDictSeries:' )
print( type( recursive_attr_dict.a ) ) 


