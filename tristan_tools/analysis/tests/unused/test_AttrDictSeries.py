import tristan_tools.analysis as analysis 


# this demonstrates how to use the RecursiveSeries together with the AttrDict
# this setup is useful in its own right, but is also the superclass of the
# TristanDataContainer, so it's important to understand how it works in order
# to use this API .

series = [ analysis.AttrDict( { 'a' : i, 'b' : 3 } ) for i in range(10) ]

recursive_series = analysis.AttrDictSeries( series )

print( '\nThe whole recursive series:' ) 
print( recursive_series ) 
print( len( recursive_series ) ) 

print( '\nAccessing index 5:' )
print( recursive_series[5] ) 


print( '\nNote that AttrDict is a subclass of dict' )
print( type( recursive_series[5] ) ) 
print( isinstance( recursive_series[5], dict ) ) 
print( recursive_series[5].keys() ) 

print( '\nConstructing new recursive series from attributes a and b:' )
print( recursive_series['a'] ) 
print( recursive_series['b'] ) 


print( '\nAlternatively, access the attributes as if it is an instance of the class:' )
print( recursive_series.a ) 
print( recursive_series.b ) 

print( '\nNote that if there is no recursive series that can be constructed (i.e. recursive_series.a is not a series of dicts or AttrDicts), then a list will automatically be returned rather than another AttrDictSeries:' )
print( type( recursive_series.a ) ) 


# print( '\nHere is how to pull the data out a recursive series, which is useful once you have completely un-nested the data and are left with an array:' )
# print( recursive_series.a ) 
# print( type( recursive_series.a ) ) 
# print( recursive_series.a.data ) 
# print( type( recursive_series.a.data ) ) 
