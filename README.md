## How to run
1. Run `docker build --tag <your tag> .`
2. Run `docker run -it -v <path to folder where you want to see saved images>:/app/output <your tag>`. It's very important to run in interactive mode and with host folder mounted to docker container. Matplotlib image with map will be saved to that folder.

## Some assumptions

- Obstacles can cover each other.
- Rectangle's square must be > 0.
- Robot can't be on obstacle.
- For current obstacles' position various robot's positions can be given. It turned out that this wasn't required, but it was already implemented and I didn't want to remove it.


## Algorithm Description

I created 2 algorithms Map1 and Map2. Map2 might be effective for online version of a task (multiple robot positions for current obstacles). This turned out to be not needed, but I didn't want to throw it away.

### Map1
- Stores rectangles as array of their diagonal corners coordinates.
- Getting information about obstacles near robot works in `O(obstacle_amount)` as it just iterates over all obstacles each time and finds the closest ones.
- Initializing of map works in `O(obstacle_amount) < O(N^2)`.
- Map consumes `O(obstacle_amount) < O(N^2)` memory.
- That algorithm is used if version is offline or "not enough" (later about what is "enough")
robot's positions updates are planned.

### Map2
- Keep obstacles in 2 data structures in Map object:
1. As dictionary `self.obstructed_y_to_x` of lists, where `self.obstructed_y_to_x[35]`, for example,
is hashset of all X-es of cells, that are occupied by some obstacle and have Y = 35. 
2. Mirror to above `self.obstructed_x_to_y`. 
It consumes
These structures consume `O(sum of obstacles' squares) < O(N^2)`.

- Suppose we have robot with coordinates `(Xr, Yr)`.  When we want to check where are the obstacles relative to robot on 0 (up) and 180 (down) degrees we get upper-bound and lower-bound cells from `self.obstructed_x_to_y[Xr]`. From their coordinates in a grid we deduce their relative position to robot.  Checking obstacles on 90 and 270 is similar, except that we check for upper and lower bounds
in `self.obstructed_y_to_x`.

- As dictionary (hashset) works in `O(1)`, in found array we do binary search in `O(log N)`. We get answer for the query for `O(log N)` in total.

- That algorithm is used in online version, when amount of planned updates of robot positions `rp` is such that: `(sum of obstacles' squares) + rp * log2(N) < rp * len(obstacles)`.



