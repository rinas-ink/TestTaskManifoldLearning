## Some assumptions

- Obstacles can't cover each other (partially or not).
- Rectangle's square must be > 0.
- For current obstacles' position various robot's positions can be given

## Algorithm Description

Keep obstacles in 3 data structures in Map object:
1. As hashmap `self.rectangles` from obstacle id to its coordinates. It consumes 
O(number of obstacles) memory.
2. As array `self.rectangleYtoX` of hashsets, where `self.rectangleYtoX[35]`, for example,
is hashset of all X-es of cells, that are occupied by some obstacle. It consumes
O(sum of obstacles' squares + n) memory as it is array of size n, but there are no more than
sum of obstacles' squares elements in it. In the worst case sum of obstacles' squares
is around n^2, and it consumes O(n^2).
3. Similar to above `self.rectangleXtoY`, but indices of array are X-es and in sets are Y-s. 
Memory consumption same as above.

As sum of squares of obstacles is definitely >= then the number of them 
(as they have non-zero square) we can tell that memory consumption overall is
O(sum of obstacles' squares + n) with constant around 4 = (1 for first hashmap) + 1.5 * (2 for arrays of hashsets). 
That wasn't checked empirically.

When we want to add an obstacle we add it to hashmap and then add all it's cells to 
corresponding positions in `self.rectangleYtoX` and `self.rectangleXtoY`. So adding of obstacle
works in O(k*l), where k and l are dimensions of an obstacle.
We add borders of a map to these arrays as well to avoid extra checks.

Suppose we have robot with coordinates `(Xr, Yr)`.
When we want to check where are the obstacles relative to robot on 0 (up) and 180 (down) 
degrees we get upper-bound and lower-bound cells from `self.rectangleXtoY[Xr]`. 
From their coordinates in a grid we deduce their relative position to robot.

Checking obstacles on 90 and 270 is similar, except that we check for upper and lower bounds
in `self.rectangleYtoX`.

As hashset works in amortized O(1), we answer in O(1) to each new position
of robot.



