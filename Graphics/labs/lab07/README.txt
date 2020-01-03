Part 1
------
Case 1 - since you translate 10 in the x direction first you are just going to the right 10 steps and then rotating by 45 degrees

Case 2 - you are going to rotate 45 degrees first, then move 10 steps along your x axis so instead of going straight right you
will be going up and to the right

Case 3 - you rotate your world by 45 degrees then scale your y of the universe by 3

Case 4 - First you grow your universe by 3 in the y axis then rotate it by 45 degrees

------
Part 2
------
10
1
1
1


it actually rotates by 45 degrees, scales it, then translates it so
glTranslatef(0.0, 0.0, -15.0)
glScalef(1.0, 3.0, 1.0)
glRotatef(45.0, 0.0, 0.0, 1.0)

------
Part 3
------
glTranslatef(7.5,7.5,0)
glRotatef(45.0, 0.0, 0.0, 1.0)
glTranslatef(-7.5,-7.5, -15.0)
glRectf(5.0, 5.0, 10.0, 10.0)

------
Part 4
------
