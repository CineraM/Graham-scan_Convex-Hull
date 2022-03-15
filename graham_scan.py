import matplotlib.pyplot as plt
import random
import numpy as np
import math

# global variables
GLOBAL_DELAY = 0.3
NUM_OF_POINTS = 18
VALUES_RANGE = 10.0 # values in range from 1 to n

def draw_line(point1, point2, color = "black", line_style = "-", delay = GLOBAL_DELAY, delaybool = True):
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    line = plt.plot(x_values, y_values, c = color, linestyle = line_style, zorder=0)
    if(delaybool):
        plt.pause(delay)
    return line

# https://iq.opengenus.org/graham-scan-convex-hull/
# used in the while loop of the algo, based from here^^
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
    if val == 0:
        return 0
    
    if val > 0:
        return 1 #cw
    else:
        return 2 #ccw
    
# from stack overflow
def angle_between_points(p1, p2):
	xDiff = p2[0] - p1[0]
	yDiff = p2[1] - p1[1]
	angle = math.degrees(math.atan2(yDiff, xDiff))
	return (angle)

def proposed_hull(sorted_points, size, color = "black", delay=GLOBAL_DELAY):
    sorted_lines = []	# return the sorted lines
    angle_lines = []	# Delete the angled lines at the end
    labels = []			# Delete the lables at the end
    
    min_x = sorted_points[0]   
    for i in range(size):
        if i == 0: # label for the 1st point
            label = plt.text(sorted_points[i][0]-0.5, sorted_points[i][1]+1, 
			"Leftmost", horizontalalignment='left',
			verticalalignment='top', rotation='vertical',
			color="red", fontweight='heavy')
            labels.append(label)
            plt.pause(delay)
            continue
        # sketch the lines from the leftmost to all points
        line = draw_line(min_x, sorted_points[i], color, "--", delay)
        angle_lines.append(line)
        # label for the points
        label = plt.text(sorted_points[i][0], sorted_points[i][1], f'{i}', 
		color="blue", horizontalalignment='left', fontweight='heavy')
        labels.append(label)
        # proposed hull lines
        line = draw_line(sorted_points[i], sorted_points[i-1], color, "-", delay)
        sorted_lines.append(line)
    plt.pause(delay)
 
    line = draw_line(sorted_points[0], sorted_points[-1], color, "-", delay)
    sorted_lines.append(line)
    
    for line in angle_lines:
        l = line.pop(0)
        l.remove()
    plt.pause(GLOBAL_DELAY)
    
    return sorted_lines, labels
    

plt.xlim(0, VALUES_RANGE+1)
plt.ylim(0, VALUES_RANGE+1)
plt.axis('off')

angles = []
randomx = []
randomy = []
random_points = []
# generate random points
for i in range(NUM_OF_POINTS):   
    x = round(random.uniform(1.0, VALUES_RANGE), 2)
    y = round(random.uniform(1.0, VALUES_RANGE), 2)
    point = [x, y]
    random_points.append(point)
    randomx.append(x)
    randomy.append(y)
    
######################## Hard Coded Points ############################
# random_points = [[6.9, 9.22], [3.04, 3.72], [7.01, 3.19], [3.83, 8.58], 
#                  [2.61, 8.56], [6.67, 2.89], [8.57, 7.77], [5.93, 5.47], 
#                  [9.19, 2.56], [4.83, 7.58], [9.76, 2.55], [3.19, 6.49]]
# randomx = []
# randomy = []
# for point in random_points:
#     randomx.append(point[0])
#     randomy.append(point[1])
######################## Hard Coded Points ############################

randomx = np.array(randomx)
randomy = np.array(randomy) # waste of memory fix later 
# plot the points
plt.scatter(randomx, randomy, s=10, c="black", zorder=0)
plt.pause(GLOBAL_DELAY)
# selecting min x for the algo
min_x = random_points[0]
for i in random_points:
    if(i[0] < min_x[0]):
        min_x = i;


# rotating all by 90 ccw to properly# https://iq.opengenus.org/graham-scan-convex-hull/
	# while loop implementation based from here ^ find the angle        
points_90ccw = []
for point in random_points: 
    if min_x == point:
        continue
    ccw_90 = [-point[1], point[0]]
    points_90ccw.append(ccw_90)   
min_x = [-min_x[1], min_x[0]]

# finding the angle with respect to our leftmost point
for point in points_90ccw:        
    new_angle = angle_between_points(point, min_x)
    new_point = point
    new_point.append(new_angle)
    angles.append(new_point)

new_point = min_x
new_point.append(-400.0) # make the most leftmost the 1st in the list.
angles.append(new_point)

# sort the angles based on the angle
angles = sorted(angles, key=lambda x:x[2]) # sort bse on the angle column

# revert the 90ccw rotation
sorted_ang_points = []
for point in angles: 
    point = [point[1], -point[0]]
    sorted_ang_points.append(point)

# animates the proposed hull
hull_lines, labels = proposed_hull(sorted_ang_points, NUM_OF_POINTS, "black")
plt.pause(2)
for i in range(NUM_OF_POINTS):
    if i == 0 or i == NUM_OF_POINTS-1:
        continue
    l = hull_lines[i].pop(0)
    l.remove()    
plt.pause(GLOBAL_DELAY) # need delay to delete
    
# hull lines, sorted points

stack = []

# push the 1st 3 vertices
stack.append(sorted_ang_points[0])
stack.append(sorted_ang_points[1])
stack.append(sorted_ang_points[2])

lines = []
new_line = draw_line(stack[1], stack[2], "blue" ,delay=GLOBAL_DELAY)
lines.append(new_line)
for i in range(3, NUM_OF_POINTS):
    # draw lines and append them to a list
    new_line = draw_line(stack[len(stack)-1], sorted_ang_points[i], "blue" ,delay=GLOBAL_DELAY)
    lines.append(new_line)
    # https://iq.opengenus.org/graham-scan-convex-hull/
	# while loop implementation based from here ^
    while(orientation(stack[len(stack)-2], stack[len(stack)-1], sorted_ang_points[i]) != 2):
        # stack will be popped --> delete two lines
        length = len(lines)
        # copy the top two lines --> plot them as red to represend the lines that will be deleted
        topl = lines[length-1]
        x1 = topl[0].get_xdata()
        y1 = topl[0].get_ydata()
        err1_line = plt.plot(x1, y1, c = "red", linestyle = "-", zorder=0)
        
        nextTopl = lines[length-2]
        x2 = nextTopl[0].get_xdata()
        y2 = nextTopl[0].get_ydata()
        err2_line = plt.plot(x2, y2, c = "red", linestyle = "-", zorder=0)
        
        l = lines.pop().pop(0)
        l.remove()
        l = lines.pop().pop(0)
        l.remove()
        
        plt.pause(GLOBAL_DELAY)
        l = err1_line.pop(0)
        l.remove()
        l = err2_line.pop(0)
        l.remove()
        # delete the algorithm/error lines
            
        a = stack.pop() 

        new_line = draw_line(stack[len(stack)-1], sorted_ang_points[i], "blue" ,delay=GLOBAL_DELAY)
        lines.append(new_line)
    #append the next point to the stack
    stack.append(sorted_ang_points[i])


for i in range(len(stack)):
	draw_line(stack[i], stack[i-1], "black", "-", 0.1, delaybool=False)
 
for text in labels:
    text.set_visible(False)
    
plt.pause(0.00001) # need delay to delete

for i in range(len(lines)):
    l = lines[i].pop(0)
    l.remove()  
plt.pause(0.00001) # need delay to delete

plt.show()

""" plt line format notes:
	colors = ["red", "blue", "green", "orange"]
	[‘solid’ | ‘dashed’, ‘dashdot’, ‘dotted’ | (offset, on-off-dash-seq) | '-' | '--' | '-.' | ':' | 'None' | ' ' | '']
"""