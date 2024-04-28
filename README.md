# TODO
- [ ] setup and installation
- [ ] deliverables
    1. write what is required acc. to the assignment
    2. counterwrite what we have delivered according to each of those points in the readme itself.
    3. ~make a dedicated DELIVERABLES.md file.~
- [ ] SCENARIOS
    1. how are we going to model the faculty? using MDP or what?
    2. 
---

# autonomous-systems-pa3
Programming assignment for autonomous systems programming assignment 3 - (Phase II) by Jaisidh Singh, Ishaan Shrivastava.

# setup and installation
1. make sure `ros-noetic-desktop-full` as well as all of the `turtlebot3` packages are installed.
2. clone the repository and cd into `./autonomous-systems-pa3`.
3. create the workspace directory using `mkdir -p catkin_ws_local/src`
4. cd into `catkin_ws_local` and execute the command `catkin_make`
5. execute the command `source devel/setup.bash`
6. use a GUI file manager to copy the `catkin_ws/src/custom_worlds_testing` and `catkin_ws/src/maze_solver` folders to inside of `catkin_ws_local/src/`
7. navigate back to `catkin_ws_local` and execute the command `catkin_make`
8. set the turtlebot model environment variable using `export TURTLEBOT3_MODEL=burger`
9. launch the world simulation using `roslaunch maze_solver world.launch`

# 