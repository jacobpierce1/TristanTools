# this is a class that pre-loads data before it is displayed for
# a better user experience.

# import mayavi
# print( mayavi.__file__ ) 

import numpy as np 
import threading 
from queue import Queue


from collections import OrderedDict

import gui_config



DEBUG_DATA_LOADER = 1




# see https://stackoverflow.com/questions/3262346/pausing-a-thread-using-threading-class
# to see how the thread event pausing works. 

class DataLoader( object ) :

    def __init__( self, tristan_data_analyzer ) :

        self.queue = Queue() 
        # self.pause_event = threading.Event()

        self.current_timestep = -1 
        self.current_timestep_finished_event = threading.Event() 
        
        self.lock = threading.Lock() 
        
        # self.timesteps_being_loaded = set() 
        self.timesteps_loaded = set()

        # timesteps that are currently being loaded
        self.timesteps_being_loaded = set() 
        
        # self.thread = None
        self.tristan_data_analyzer = tristan_data_analyzer 

        # store all active threads and the timestep that each thread is computing.
        self.threads = []
        # self.timesteps_being_loaded  = [] 

        for i in range( gui_config.DATA_LOADER_NUM_THREADS ) :
            t = threading.Thread( target = self.worker_target )
            t.setDaemon( 1 )
            t.start() 
            
            # self.timesteps_being_loaded.append( -1 )
                                


    # given the current timestep and the known data that could be switch in the gui,
    # load all relevant data that has not been loaded yet and unload unnecessary data.
    # note that it is not possible to kill a thread or restart a thread, so if a thread is
    # working on obsolete data at the time that the request for 
    def handle_timestep( self, timestep, stride, max_timestep ) : 

        if DEBUG_DATA_LOADER :
            print( 'INFO: handling new timestep in DataLoader.' ) 
        
        # # construct a new queue of timesteps to be loaded. 
        # queue = Queue()

        self.current_timestep = timestep

        # first handle the current timestep, which is required before we return anyway
        # if it has already been loaded / computed, then this will take barely any time.
        # this way, if all the threads have terminated, then there will be no GIL competition for
        # resources to compute the current timestep, which is the priority. if it's already in the
        # process of being computed, then we just wait for it to finish.
        # with self.lock :
        #     compute_current_timestep_in_main = self.current_timestep not in self.timesteps_being_loaded

        # if compute_current_timestep_in_main :
        #     if DEBUG_DATA_LOADER :
        #         print( 'INFO: computing current timestep in main' ) 
        #     self.load_timestep( self.current_timestep )

        #     if DEBUG_DATA_LOADER :
        #         print( 'INFO: finished.' )

        # else :
        #     if DEBUG_DATA_LOADER :
        #         print( 'INFO: current timestep is already being computed. ' ) 

        # compute in main thread, which gives it priority if the other threads have finished. 
        self.load_timestep( self.current_timestep ) 
        
        # now for the rest of the threads, load them into the queue and they will automatically
        # be picked up by the worker threads. we will return before they finish.
        
        with self.queue.mutex :
            self.queue.queue.clear() 
            
        timesteps = [] 
        
        for i in range( gui_config.DATA_LOADER_FORWARD_TIMESTEPS ) :
            forward = min( timestep + stride * i + 1, max_timestep ) 
            backward = max( timestep - stride * i, 0 )

            timesteps.append( forward )
            timesteps.append( backward ) 
            

        # remove duplicates
        timesteps = list( OrderedDict.fromkeys( timesteps ) )

        if DEBUG_DATA_LOADER : 
            print( 'timesteps: ' + str( timesteps ) ) 
        
        unused_indices = self.timesteps_loaded - set( timesteps )

        if DEBUG_DATA_LOADER :
            print( 'deleting old indices: ' + str( unused_indices ) )

        self.tristan_data_analyzer.unload_indices( unused_indices )

        with self.lock :
            self.timesteps_loaded -= unused_indices 


        if DEBUG_DATA_LOADER :
            print( 'timesteps loaded: ' + str( self.timesteps_loaded ) ) 


        # add these to the queue. processing starts immediately.
        for t in timesteps :
            self.queue.put( t ) 

        if DEBUG_DATA_LOADER :
            print( 'queue:' + str( list( self.queue.queue ) ) )  
            print( 'waiting for current timestep to finish.' )

        self.current_timestep_finished_event.wait() 
        self.current_timestep_finished_event.clear()
        
        if DEBUG_DATA_LOADER :
            print( 'INFO: current timestep finished, returning ' ) 



        
    def worker_target( self ) :

        while 1 :
            # print( 'waiting for event' ) 
            # self.pause_event.wait() 

            # print( 'getting data from queue. ' ) 
            timestep = self.queue.get()


            
            self.load_timestep( timestep ) 

            
            self.queue.task_done() 


            
    def load_timestep( self, timestep ) :
        # only load if the data is not yet loaded.
        with self.lock :
            load = ( timestep not in self.timesteps_loaded ) and ( timestep not in self.timesteps_being_loaded ) 

        if load :

            # track the fact that this data is being loaded, so that no other thread attempts to load it
            # if requested. 
            with self.lock :
                self.timesteps_being_loaded.add( timestep ) 


            if DEBUG_DATA_LOADER :
                print( 'loading timestep: ' + str( timestep ) ) 

            self.tristan_data_analyzer.load_indices( timestep ) 
            self.tristan_data_analyzer.compute_indices( timestep ) 

            # update the status. only one thread can update the variables at a time.  
            with self.lock :
                self.timesteps_loaded.add( timestep )
                self.timesteps_being_loaded.remove( timestep ) 
                # self.timesteps_being_loaded.remove( timestep ) 

        else :
            if DEBUG_DATA_LOADER :
                print( 'already loaded or being loaded: ' + str( timestep ) ) 

        # signal that handle_timestep can return, i.e. the plots are ready to be generated
        # and handle_timestep can return.
        if self.current_timestep == timestep :
            self.current_timestep_finished_event.set() 


                    
    def clear( self ) :
        with self.lock : 
            self.timesteps_loaded.clear()

        if DEBUG_DATA_LOADER:
            print( 'INFO: cleared data loader.' )
            print( 'self.timesteps_loaded: ', self.timesteps_loaded ) 
            
