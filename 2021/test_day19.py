from day19 import *


# def test_possible_rotations():

#     test_points = [(1,0,0), (0,1,0), (0,0,1)]

#     expected_results = [
#                                      # #+x with four orientations
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('x',0,degrees=True))
#         [(1,0,0), (0,0,1), (0,-1,0)], # rotations.append(Rotation.from_euler('x',90,degrees=True))
#         [(1,0,0), (0,-1,0), (0,0,-1)], # rotations.append(Rotation.from_euler('x',180,degrees=True))
#         [(1,0,0), (0,0,-1), (0,1,0)], # rotations.append(Rotation.from_euler('x',270,degrees=True))
#                                      # #-x with four orientations
#         [(-1,0,0), (0,-1,0), (0,0,1)], # rotations.append(Rotation.from_euler('zx',[180, 0],degrees=True))
#         [(-1,0,0), (0,0,-1), (0,-1,0)], # rotations.append(Rotation.from_euler('zx',[180, 90],degrees=True))
#         [(-1,0,0), (0,1,0), (0,0,-1)], # rotations.append(Rotation.from_euler('zx',[180, 180],degrees=True))
#         [(-1,0,0), (0,0,1), (0,1,0)], # rotations.append(Rotation.from_euler('zx',[180, 270],degrees=True))
#                                      # #+y with four orientations
#         [(0,1,0), (-1,0,0), (0,0,1)], # rotations.append(Rotation.from_euler('zy',[90, 0],degrees=True))
#         [(0,1,0), (0,0,1), (1,0,0)], # rotations.append(Rotation.from_euler('zy',[90, 90],degrees=True))
#         [(0,1,0), (1,0,0), (0,0,-1)], # rotations.append(Rotation.from_euler('zy',[90, 180],degrees=True))
#         [(0,1,0), (0,0,-1), (-1,0,0)], # rotations.append(Rotation.from_euler('zy',[90, 270],degrees=True))
#                                      # #-y with four orientations
#         #NOTE - test not completed, start here

#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('zy',[270, 0],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('zy',[270, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('zy',[270, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('zy',[270, 270],degrees=True))
#                                      # #+z with four orientations
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[90, 0],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[90, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[90, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[90, 270],degrees=True))
#                                      # #-z with four orientations
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[270, 0],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[270, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[270, 90],degrees=True))
#         [(1,0,0), (0,1,0), (0,0,1)], # rotations.append(Rotation.from_euler('yz',[270, 270],degrees=True))
#     ]

#     def test_rotation(rotation, points):
#         points_out = []
#         rmat = rotation.as_matrix()
#         for point in points:
#             pout = np.dot(rmat, np.array(point))
#             points_out.append(tuple([round(v) for v in pout.tolist()]))
#         return points_out

#     for index, rotation in enumerate(possible_rotations()):

#         print(index+1, expected_results[index])
#         transformed_points = test_rotation(rotation, test_points)
#         assert transformed_points == expected_results[index]
        

