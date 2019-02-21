OVERVIEW 

This is a library for plotting and analyzing TRISTAN-MP simulation data. The plan is to include offline tools for complete customization of data analysis in specific cases, as well as a GUI for rapid visualization of the most important quantities such as fields and density.

Included are the following groups of software:

* tristan_tools.analysis: importable library for analysis and plotting of tristan data, independently of a GUI. 
* tristan_tools.gui: a GUI built on TristanAnalysis used for rapid data-visualization
* tristan_tools.launcher: importable library with some barebones functions for dispatching simulations that explore a user-specified parameter space, as well as a system to automate creation of the input files (which dependent on user-implemented tristan user file). 



INSTALLATION

run `pip install -e .` in the directory containing this README. For Midway users, you may need to run `pip install --user -e .`. 




CITATION

Feel free to use the software freely without citation. 




ABOUT

Originally developed by Jacob Pierce at UChicago under Prof. Damiano Caprioli in Jan 2019. Inspired by previously existing software Iseult for 2D tristan analysis. Current email is jacobpierce@uchicago.edu, feel free to contact for details.
 



STEPS FOR ADDING A NEW PLOTTER

One major advantage of this code is that new plots can be added easily. Here are the steps for doing so:

0. for efficiency, test the features of the plot that you want to create (including changing mayavi attributes that will be able to be changed in real time via the gui, e.g. the glyph mask_points, or scale_factor for vectors ) in a barebones script. some previous prototypes are in the examples section.

1. create a new file with the name of the plotter and its actions in analysis/plotters, imitating the existing plotters. the functions other than __init__, startup, reset, and set_data are not required, but those are what are called by the gui (in the current implementation) for changes to the plot

2. make the plotter usable by adding the corresponding line to __init__.py in the plotters directory

3. update TristanDataPlotter : 

   3.1. make the plotter available to the TristanDataPlotter class by adding the key for the new type of plot in the PLOTTERS_DICT of analysis/tristan_data_plotter, imitating the existing entries

   3.2 set what plot names will be available to this plotter by defining them in the tristan_data_plotter.py header (e.g. ALL_SCALARS if it's using 3D scalars), and add the entry to the AVAILABLE_DATA_DICT. if you are hoping to plot new computations that don't exist yet, then you will have to add those computations first (see the adding new computations section). this dicitonary contains the available plots (called the plot_names) that can be constructed for each plot_type (e.g. volume_slice).

   3.3 if you defined a new plot name, then add the new keys required for the new plot_name to the PLOT_NAME_TO_KEYS_DICT. this maps the data name as displayed in the GUI (e.g. B) to a list of keys required by the tristan_data_container to construct it. for everything except the vectors, the current plots just use the same name (e.g. for the scalars: 'dens' is shown in the plot, and 'dens' is accessed in the TristanDataAnalyzer). this would probably be the case for most new plots. the simplest example is a plot of the vector field of B. as implemented, 'B' is chosen as the plot name, and the keys required to make that plot are 'bx', 'by', and 'bz' (as output in tristan data). as a more complicated example, for the plot 'PP', we get a histogram of the momentum squared. the plot can show hists for both electrons and positrons, so PP_e_spec and PP_i_spec (computed in computations) are both required. note that they are not necessarily used for every plot that is made, but for the most general plot they would both be required. 

4. imitate the entries in gui/plot_options_widgets.py to add a new options widget for the new plot type. these are the options that appear when you click on "options" in the gui. just define the functions __init__ and set_current_values, which can do nothing (see commented out stub at bottom)

5. make the new options widget available to the PlotControlWidget class, which creates the dialogs for selecting a new plot when you click on the 'options' button, by adding it to the dictionary  _plot_options_widgets in the top of gui/plot_control_widget.py 


6. if you wrote stubs before, in the plot_options_widget, then go back and write them. for adding new features, i would once again suggest going to step 0 to debug first. 






ADDING A NEW COMPUTATION

0. First, consider whether the computation you are adding is generic (useable in a wide variety of circumstances, e.g. plasma beta) or very specific to your situation (e.g. methods for detecting a shock front). if the latter, i would recommend subclassing the current tristandataanalyzer and adding new methods for your specific case. that way, you are not going to get stuck with a massive class if you later on want to add more functions for a different specific analysis.

1. In either case, open the class for the analyzer (either the original TristanDataAnalyzer in analysis/tristan_data_analyzer.py or your subclass). Add the computation name to the instance variable self.computation_callbacks in the __init__ function. This is the name as it will be displayed in the gui and referenced elsewhere

2. define the new callback function in the class, just imitate the existing ones  that are defined in self.computation_callbacks. it should take an index at which you are performing the computation, from which you have full flexibility over the data array( i.e. can access all timesteps for the computation) to perform the quantity. the computation will not be stored in self.data elsewhere, so you have to do it here.

3. if you already have plots that can plot the new computation, then add it to the corresponding dictionaries at the top of tristan_data_plotter.py. for example if the quantity you computed is a scalar, defined at every grid point, then you could plot it using volume slice or any other scalar plotter. in this case, adding it to ALL_SCALARS will make it accessible to these plotters.

That is all that is necessary, unless the computation requires a new type of plot. In that case you need to define a plotter to make the plot, see the section on adding a new plotter. 
