from animation import line, text, box, circle, color

F1 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [circle, [57, 85, 0, 5, 35], "left eye"],
      [line, [46, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 10, 60, 0], "right arm"],
      [line, [50, 50, 90, 60, 0], "left arm"],
      [line, [50, 20, 10, 0, 0], "right leg"],
      [line, [50, 20, 90, 0, 0], "left leg"]]

F2 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [circle, [57, 85, 0, 3.5, 35], "left eye"],
      [line, [46, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 10, 60, 0], "right arm"],
      [line, [50, 50, 90, 50, 0], "left arm"],
      [line, [50, 20, 30, 0, 0], "right leg"],
      [line, [50, 20, 90, 0, 0], "left leg"]]

F3 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [circle, [57, 85, 0, 2, 35], "left eye"],
      [line, [46, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 10, 40, 0], "right arm"],
      [line, [50, 50, 90, 40, 0], "left arm"],
      [line, [50, 20, 10, 0, 0], "right leg"],
      [line, [50, 20, 70, 0, 0], "left leg"]]

R1 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [57, 85, 0, 5, 35], "right eye"],
      [line, [46, 70, 60, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 80, 65, 0], "right arm"],
      [line, [50, 50, 80, 60, 0], "left arm"],
      [line, [50, 20, 30, 0, 0], "right leg"],
      [line, [50, 20, 60, 0, 0], "left leg"]]

R2 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [57, 85, 0, 5, 35], "right eye"],
      [line, [46, 70, 60, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 70, 45, 0], "right arm"],
      [line, [50, 50, 80, 60, 0], "left arm"],
      [line, [50, 20, 40, 0, 0], "right leg"],
      [line, [50, 20, 60, 0, 0], "left leg"]]

R3 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [57, 85, 0, 5, 35], "right eye"],
      [line, [46, 70, 60, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 80, 65, 0], "right arm"],
      [line, [50, 50, 80, 60, 0], "left arm"],
      [line, [50, 20, 40, 0, 0], "right leg"],
      [line, [50, 20, 70, 0, 0], "left leg"]]

L1 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [line, [40, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 20, 65, 0], "right arm"],
      [line, [50, 50, 20, 60, 0], "left arm"],
      [line, [50, 20, 30, 0, 0], "right leg"],
      [line, [50, 20, 60, 0, 0], "left leg"]]

L2 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [line, [40, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 30, 45, 0], "right arm"],
      [line, [50, 50, 20, 60, 0], "left arm"],
      [line, [50, 20, 40, 0, 0], "right leg"],
      [line, [50, 20, 60, 0, 0], "left leg"]]

L3 = [[circle, [50, 80, 0, 15, 35], "head"],
      [circle, [43, 85, 0, 5, 35], "right eye"],
      [line, [40, 70, 54, 70, 0], "mouth"],
      [line, [50, 20, 50, 65, 0], "body"],
      [line, [50, 50, 20, 65, 0], "right arm"],
      [line, [50, 50, 20, 60, 0], "left arm"],
      [line, [50, 20, 40, 0, 0], "right leg"],
      [line, [50, 20, 70, 0, 0], "left leg"]]

stickFigure = {'front':[F1,F2,F3], 'right':[R1,R2,R3], 'left':[L1,L2,L3]}
