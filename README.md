## Graph_algorithms
Link to Report on TSP Approximation: [link](https://www.overleaf.com/read/kxcbxmmbpnkx).

This program allows for visualization and approximation of four TSP approximation algorithms (Greedy, Nearest-neighbor, Christofides, and conv-hull insertion heuristic). It provides the cost of each algorithm on a user-provided TSP dataset. Keep in mind the algorithms **only** work for a symmetric complete graph. This program ALSO provides two lower bounds on the optimal cost: 1-Tree Lower Bound and the HK Lower Bound. You can then compare these approximations to the optimal solution (which is usually provided on http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html along with TSP datasets.) Feel free to let me know of any bugs!

Packages Needed 
------------
**Networkx**: https://pypi.python.org/pypi/networkx/ Make sure to download the networkx-1.11.tar.gz (md5) file and extract the folder networkx-1.11. Navigate to that folder and then use the command

```
python setup.py install
```

**Numpy & SciPy**: https://www.continuum.io/downloads Download and run the installer. If you're using Windows make sure to check the 'Add Anaconda to my PATH environment variable'. 

Dataset Setup
------------
To use this program, please place the appropriate datafiles in the datasetTSP directory. 3 sample directories have been included in this repo. In the datasetTSP directory, make a folder with the name **datasetName**. Make sure to follow the nomenclature and include **datasetName**_xy.txt (x and y coordinates), **datasetName**_s.txt(solution), and **datasetName**_d.txt(adjacency matrix, this one is **optional**) in that directory. 

For the _s.txt, make sure to append the _s.txt file with the first node number if you are selecting a TSPdata instance from the link above. Keep in mind it is **not** required for you to have an adjacency matrix file or a solution file. You must, however, have a _xy.txt file in the directory for this program to work. 

If you use a solution file for a particular instance from the TSPLib, you might want to also use the adjacency matrix that corresponds to the same instance. It's not required but sometimes the edge lengths in the problem might not be determined by the euclidean distance between the two nodes connected by that edge (EX: pa561.tsp). Also, some of these adjacency matrices may be provided as symmetric matrices that omit the upper triangular portions. If you fill in the upper triangular portion, you can still use it with this TSP Solver. This Solver requires for the adjacency matrix to be square and symmetric. It must not omit any portion of the matrix. 

For the **datasetName**xy.txt file, each row of the .txt file corresponds to a single node's x- & y-coordinates. To use the data from the TSPLIB, get the xy coordinates from the **datasetName**.tsp link (att48.tsp if you want the xy coordinates). You can also find the optimal tour under the tour_section in the **datasetName**.opt.tour link in the TSPLIB link above. 

Usage
-----
On your terminal, navigate to the graph_algorithms directory. 
Proceed to run:
```
python implementations.py
```
You will then see:
```
Enter the TSP directory you would like to approximate:
```
Type in your **datasetName**. This will be the same as the name of your newly created directory in the datasetTSP directory.
You will then see:
```
Do you have an adjacency matrix .txt file for your instance?(Y/N):
```
If you have not included a _d.txt file in your directory, type in 'N'. If you have, type in 'Y'.

You will then see:

```
Do you have a solution .txt file for your instance?(Y/N): 
```
If you have not included a _s.txt file in your directory, type in 'N'. If you have, type in 'Y'. If you answer 'Y', the cost of your optimal tour in the _s.txt file will be calculated and displayed.

You will then be prompted about whether or not you would like the HKLB to be included in the display. The HKLB uses the iterative approach and may take awhile depending on the number of nodes your TSP instance has. 
```
Would you like the Held-Karp Lower Bound to be included? The computation for this may take awhile and will increase the waiting time.(Y/N): 
```
To find the best HKLB, one can only find the strictest lower bound through experimentation of different U (Target Values) in bounds.py line 22. Currently, it is set to 115% of the One-Tree Lower Bound. By changing the U, you may get tighter lower bounds. 

You will then be prompted to whether or not you would like visualizations.
```
Would you like visualizations for the algorithms? (Y/N): 
```
The costs will then show up for the four algorithms along with the optimal cost (calculated from _s.txt). The lower Bounds (HKLB and OTLB) will also show up on your terminal.

The visualizations, if you typed in 'Y', will be saved in a directory with the name **datasetName** in the graph_algorithms directory. Check in 
```
\graph_algorithms\datasetName
```
and you should see distinct images in multiple folders. These images have not been stitched yet to form a movie. You can use imageJ to convert these images into a video. Enjoy! 

Example visualization [link](https://chriski777.github.io/TSP_Solver_Website/).
