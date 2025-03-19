# Code structure
The source code contain mainly in ```uav4res``` folder, python file outside ```path_planning_visualizer``` folder contain codes to initialize interface of the application. We use pygame to draw interface. The main algorithm is put inside ```path_planning_visualizer``` folder:
+ ```path_planning_visualizer/main.py```: This file visulize the finding process
+ ```path_planning_visualizer/helper.py```: This file contain the algorithm to find the path for each rescue team and other helper function.

# Setup use Poetry 
Make sure you have installed Poetry 

```
pip install poetry
```
Then, run the following commands:
```
git clone https://github.com/UAV4Res/uav4res-visualizer
cd uav4res-visualizer
poetry install
```
# Run
```
python uav4res/main.py
```

# Reference
Theta*: https://arxiv.org/pdf/1401.3843 

A*: https://vi.wikipedia.org/wiki/Gi%E1%BA%A3i_thu%E1%BA%ADt_t%C3%ACm_ki%E1%BA%BFm_A*

BFS: https://wiki.vnoi.info/algo/graph-theory/breadth-first-search.md

Path planning system: https://ieeexplore.ieee.org/document/8955663
