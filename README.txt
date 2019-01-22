OVERVIEW 

This is a library for plotting and analyzing TRISTAN-MP simulation data. The plan is to include offline tools for complete customization of data analysis in specific cases, as well as a GUI for rapid visualization of the most important quantities such as fields and density.

Included are the following groups of software:

* TristanAnalysis: importable library for analysis and plotting of tristan data, independently of a GUI. 
* TristanGUI: a GUI built on TristanAnalysis used for rapid data-visualization
* TristanLauncher: contains some barebones functions for dispatching simulations that explore a user-specified parameter space, as well as a system to automate creation of the input files (which dependent on user-implemented tristan user file). 



INSTALLATION

run `pip install -e .` in the directory containing this README. For Midway users, you may need to run `pip install --user -e .`. 



CITATION

Feel free to use the software freely without citation. 
