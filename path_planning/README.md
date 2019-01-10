# **Path Planner for Highway Autonomous Driving**

### Objective

Implement a simple real-time path planner in C++ to navigate a car around a simulated highway scenario, including 
other traffic, given waypoint, and sensor fusion data. 

The planned path should be safe and smooth, so that tha car 
avoids collisions with other vehicles, keeps within a lane (aside from short periods of time while changing lanes), and 
drive according to the speed limits (50mph). Besides, the car must not violate a set of motion constraints, e.g. maximum 
acceleration (10 m/s^2), and maximum jerk (50 m/s^3). As a results, the car is drive safely and the passengers feel 
comfortable.
 
#### 1.3 How to run the code

1. Clone this repo.
2. Make a build directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./path_planning`.
5. Open the simulator

### 2 Approaches

#### 2.1 Algorithm Steps

**(1) Utilize the sensor fusion data to check each lane's availability**

Go through all the detected vehicle's information and status, and check the availabilities of each lanes. 
See code from line 256-306 in `src/main.cpp`.

* Note: ["sensor_fusion"] is a 2d vector of cars and then that car's [car's unique 
ID, car's x position in map coordinates, car's y position in map coordinates, car's x velocity in m/s, car's y velocity 
in m/s, car's s position in frenet coordinates, car's d position in frenet coordinates. 

**(2) Based on the lanes' availability to plan the next state of the car**

Choose one of the following states for the car, based on the lane's availability which is obtained from 
the sensor fusion. See code from line 310-324 in `src/main.cpp`.

* Change to left lane
* Change to right lane
* Keep lane (speed up, slow down or keep speed)


**(3) Use anchor points to interpolate a spline curve** 

To create a smooth path, two last points from the previous planned path and another 3 predicted 
future points are used together for computing a smooth spline curve, which is visualized as planned
path. Then break the entire spline curve into
 50 points which is used to control the vehicle's speed (our car visits them sequentially every 0.02 
 seconds). See code from line 332-443 in `src/main.cpp`.
 
* Note: There will be some latency between the simulator running and the path planner returning a path, with optimized 
code usually its not very long maybe just 1-3 time steps. During this delay the simulator will continue using points 
that it was last given, because of this it's a good idea to store the last points we have used so we can have a smooth 
transition. 

#### 2.2 Frenet coordinates

Frenet coordinates make the math easy to describe the driving behaviors. 

* we use s=0 to represent the beginning of the segment of road. 
* We use d=0 to represent the center line of that road. To the left of the center line we have negative d and to the 
right d is positive.



### 3 Discussion

The autonomous car is able to complete loop around the 6946m highway without collisions with other vehicles and uncomfortable jerk, 
and its follows the road speed limits with gentle acceleration. Besides, the car is able to take over the slow vehicles 
when there are suitable opportunities, e.g. enough spacefs to both leading and following vehicles. 





