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

1. create a new file with the name of the plotter and its actions in analysis/plotters, imitating the existing plotters. 

2. make the plotter usable by adding the corresponding line to __init__.py in the plotters directory

3. update TristanDataPlotter : 

   3.1. make the plotter available to the TristanDataPlotter class by adding the key for the new type of plot in the PLOTTERS_DICT of analysis/tristan_data_plotter, imitating the existing entries

   3.2 set what data keys will be available to this plotter by defining them in the tristan_data_plotter.py header (e.g. ALL_SCALARS if it's using 3D scalars), and add the entry to the AVAILABLE_DATA_DICT. if you are hoping to plot new computations that don't exist yet, then you will have to add those computations first (see the adding new computations section).

   3.3 add the new keys to the DATA_NAME_TO_KEYS_DICT. this maps the data name as displayed in the GUI (e.g. B) to a list of keys required by the tristan_data_container to construct it. for everything except the vectors, the current plots just use the same name (e.g. for the scalars: 'dens' is shown in the plot, and 'dens' is accessed in the TristanDataAnalyzer). this would probably be the case for most new plots.

4. imitate the entries in gui/plot_options_widgets.py to add a new options widget for the new plot type. these are the options that appear when you click on "options" in the gui.

6. make the new options widget available to the PlotControlWidget class by adding it to _plot_options_widgets in the top of gui/plot_control_widget.py

7. once the gui works and the plot gets generated, copy the current plots in gui/plot_options_widgets.py and analysis/plotters/*.py to add functionality to interactively change the plots.
