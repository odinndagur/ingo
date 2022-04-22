import bpy
import math

wallheight = 2.510
wallthickness = 0.1

floors = []

def setcursor(position):
    x,y,z = position[0], position[1], position[2]
    bpy.context.scene.cursor.location = (x,y,z)

def process_walls(wall_list):
    walls = []
    for wall in wall_list:
        if len(wall) > 2:
            h = str(wall[2])
        else:
            h = '0'
        if wall[1] < 900:
            walls.append({'length':wall[0],'advanced':True,'angle':wall[1],'h':h})
        else:
            walls.append({'length':wall[0],'advanced':False})
    return walls

hidden = 3

basement = {
    'position': (0,0,0),
    'wallheight': 2.250,
    'wallthickness': 0.1,
    'floorindex': 0,
    'rooms': [
        {
            'position': (0,0,0),
            'walls': [(10.310,999),(2.360,90),(2.270,999),(2.940,999),(2.270,180.0),(1.040,90.0),(5.540,180.0),(3.10,90.0),(4.760,180.0)],
            'mergewalls': True,
            'addfloor': True,
            'baseboard': False
        }
    ]
}


floor1 = {
    'position': (0,0,2.250),
    'wallheight': 2.510,
    'wallthickness': 0.1,
    'floorindex': 1,
    'rooms': [
        {
            'position': (0,0,2.250),
            'walls': [(10.310,999),(2.360,90),(2.270,999),(2.940,999),(2.270,180.0),(1.040,90.0),(10.310,180.0)],
            'mergewalls': True,
            'addfloor': True,
            'baseboard': False
        },
        {
            'position': (0,3.15,2.250),
            'walls': [(3.14,999)],
            'mergewalls': False,
            'addfloor': False,
            'baseboard': False
        },
        {
            'position': (3.14,0,2.250),
            'walls': [(6.340,90.0)],
            'mergewalls': False,
            'addfloor': False,
            'baseboard': False
        },
        {
            'position': (0,6.34,2.250),
            'walls': [(3.110,90.0,hidden),(4.810,0.0,hidden),(3.110,-90.0,hidden)], #svalir
            'mergewalls': False,
            'addfloor': True,
            'baseboard': False
        },
    ],
}
floors.append(basement)
floors.append(floor1)


def makefloor(floor):
    position = floor['position']
    wallheight = floor['wallheight']
    wallthickness = floor['wallthickness']
    floorindex = floor['floorindex']

    for floor_room in floor['rooms']:
        setcursor(floor_room['position'])
        bpy.ops.mesh.archimesh_room() # create room - linked walls
        room = bpy.context.active_object # select newest object as room
        room.RoomGenerator[0].wall_num = len(floor_room['walls'])
        room.RoomGenerator[0].room_height = wallheight
        room.RoomGenerator[0].wall_width = wallthickness
        room.RoomGenerator[0].floor = floor_room['addfloor']
        room.RoomGenerator[0].merge = floor_room['mergewalls']
        room.RoomGenerator[0].baseboard = floor_room['baseboard']
        for index, wall in enumerate(process_walls(floor_room['walls'])):
            # print(index,wall['length'],wall['advanced'],wall['angle'])
            currentwall = room.RoomGenerator[0].walls[index]
            currentwall.w = wall['length']
            currentwall.a = True#wall['advanced']
            if 'h' in wall:
                currentwall.a = True
                currentwall.h = wall['h']
            if currentwall.a and 'angle' in wall:
                currentwall.r = wall['angle']




for floor in floors:
    makefloor(floor)

def makestairs(pos = (0,0,0),step_num=7,model = '1', curve=False, max_width=2.270, depth=0.3, shift=1, thickness=0.3, back=True, height=0, front_gap=0, side_gap=0, crt_mat=True):
    bpy.ops.mesh.archimesh_stairs(step_num=step_num,model=model,curve=curve,max_width=max_width,depth=depth,shift=shift,thickness=thickness,back=back,height=height,front_gap=front_gap,side_gap=side_gap,crt_mat=crt_mat)
    stairs = bpy.context.active_object
    stairs.location = pos
    return stairs

make_the_stairs = True
if make_the_stairs:
    #front stairs
    frontstairs_front_gap = 1.4
    # frontstairs = makestairs(pos=(11.545,2.26,0),step_num=8,model = '1', curve=False, max_width=2.270, depth=0.3, shift=1, thickness=0.3, front_gap=frontstairs_front_gap)
    frontstairs = makestairs(pos=(11.545,-1.18325,0),step_num=8,model = '1', curve=False, max_width=2.270, depth=0.43, shift=0.64, thickness=0, front_gap=0)
    # frontstairs.location.y -= frontstairs.dimensions.y
    # frontstairs.location.y = 0

    #back stairs
    backstairs_front_gap = 1.2
    backstairs = makestairs(pos=(11.445,5.4,0),front_gap=backstairs_front_gap)
    backstairs.rotation_euler.z = math.radians(180)
    backstairs.location.y += backstairs.dimensions.y - backstairs_front_gap

    r6013stairs = makestairs(pos = (4.87,7.89,0))
    r6013stairs.rotation_euler.z = math.radians(-90)
    r6013stairs.location.z -= r6013stairs.dimensions.z


make_the_fences = True
if make_the_fences:
    #grindverk
    fenceCount = 8
    width = 4.80
    array_space = width/fenceCount
    bpy.ops.mesh.archimesh_column(
        model = '2',
        col_sx = 0.3,
        col_sy = 0.1,
        col_height=1.5,
        box_base=True,
        box_base_x=0.88,
        box_base_y=0.1,
        box_base_z=0.08,
        box_top=True,
        box_top_x=0.88,
        box_top_y=0.1,
        box_top_z=0.08,
        arc_top=False,
        array_num_x=8,
        array_space_x=0.64,
        array_space_z=0
        )
    fence = bpy.context.active_object
    fence.modifiers.new(type='ARRAY',name="Array")
    fence.modifiers["Array"].count = fenceCount
    fence.modifiers["Array"].use_constant_offset = True
    fence.modifiers["Array"].use_relative_offset = False
    fence.modifiers["Array"].constant_offset_displace.x = array_space
    fence.location.y = 9.45
    fence.location.x = 0.3


    #grindverk veggur 2
    fenceCount = 4
    width = 3.11
    array_space = width/fenceCount
    bpy.ops.mesh.archimesh_column(
        model = '2',
        col_sx = 0.3,
        col_sy = 0.1,
        col_height=1.5,
        box_base=True,
        box_base_x=0.88,
        box_base_y=0.1,
        box_base_z=0.08,
        box_top=True,
        box_top_x=0.88,
        box_top_y=0.1,
        box_top_z=0.08,
        arc_top=False,
        array_num_x=8,
        array_space_x=0.64,
        array_space_z=0
        )
    fence = bpy.context.active_object
    fence.modifiers.new(type='ARRAY',name="Array")
    fence.modifiers["Array"].count = fenceCount
    fence.modifiers["Array"].use_constant_offset = True
    fence.modifiers["Array"].use_relative_offset = False
    fence.modifiers["Array"].constant_offset_displace.x = array_space
    fence.location.y = 9.45 - 0.3
    fence.location.x = 0
    fence.rotation_euler.z = math.radians(-90)

    #grindverk veggur 2
    fenceCount = 4
    width = 3.11
    array_space = width/fenceCount
    bpy.ops.mesh.archimesh_column(
        model = '2',
        col_sx = 0.3,
        col_sy = 0.1,
        col_height=1.5,
        box_base=True,
        box_base_x=0.88,
        box_base_y=0.1,
        box_base_z=0.08,
        box_top=True,
        box_top_x=0.88,
        box_top_y=0.1,
        box_top_z=0.08,
        arc_top=False,
        array_num_x=8,
        array_space_x=0.64,
        array_space_z=0
        )
    fence = bpy.context.active_object
    fence.modifiers.new(type='ARRAY',name="Array")
    fence.modifiers["Array"].count = fenceCount
    fence.modifiers["Array"].use_constant_offset = True
    fence.modifiers["Array"].use_relative_offset = False
    fence.modifiers["Array"].constant_offset_displace.x = array_space
    fence.location.y = 9.45 - 0.3
    fence.location.x = 4.80
    fence.rotation_euler.z = math.radians(-90)

door_keys = {
    'model': '6'
}
bpy.ops.mesh.archimesh_door()
door = bpy.context.active_object
# for key in door_keys:
#     door.DoorObjectGenerator[0][key] = door_keys[key]
door.DoorObjectGenerator[0].model = '6'
door.location = (11.445,2.26,2.25)

bpy.ops.mesh.archimesh_door()
backdoor = bpy.context.active_object
backdoor.DoorObjectGenerator[0].model = '6'
backdoor.location = (11.075,5.4,2.25)
backdoor.rotation_euler.z = math.radians(180)

make_the_windows = True

def make_front_window(position):
    setcursor(position)
    bpy.ops.mesh.archimesh_winpanel()
    current_window = bpy.context.active_object
    window_generator = current_window.WindowPanelGenerator[0]

    total_window_width = 0.98 #98cm

    window_generator.kl1 = 10 #outer frame
    window_generator.fk = 1 #inner frame
    window_generator.gen = 2
    window_generator.yuk = 2
    window_generator.kl2 = 7 # risers
    window_generator.gnx0 = 26
    window_generator.gnx1 = 32
    window_generator.gny0 = 45
    window_generator.gny1 = 64
    return current_window

front_window_positions = [
    # (1.6517,-0.1,3),
    #aegir msea
    (0.71 + 0.98/2, -0.1, 3),
    (0.71 + 0.98 + 0.98/2,-0.1,3),
    #stofa
    (0.71 + 0.98/2, -0.1, 3),
    (0.71 + 0.98 + 0.98/2,-0.1,3)
]

wwidth = 0.98
#front windows:
w1 = (0.71 + wwidth/2)
w2 = (w1 + wwidth + 0.47)
w3 = (w2 + wwidth + 0.89)
w4 = (w3 + wwidth + 0.49)
w5 = (w4 + wwidth + 0.68)
w6 = (w5 + wwidth + 0.47)
front_window_x_positions = [w1,w2,w3,w4,w5,w6]
if make_the_windows:
    front_window_y = -0.1
    front_window_z = 3
    for x_pos in front_window_x_positions:
        window = make_front_window((x_pos,front_window_y,front_window_z))
        hole = [item for item in window.parent.children if 'CTRL' in item]
        
    # make_front_window((1.6517,-0.1,3))
    # bpy.ops.transform.resize(value=(0.437757, 0.437757, 0.437757), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    # current_window.location = (1.6517,-0.1,3.505)
    #gen = 5 # h count
    #yuk = 5 # v count
    #kl1 = 39 # outer frame
    #kl2 # risers
    #fk : inner frame
    #r : rotation
    #mr : sill (bool)
    #mr1 : sill height
    #mr2 : sill first depth
    #mr3 : sill second depth
    #mr4 : sill extrusion for jamb
    #gny0 - gny999 : first row height - 1000 row height
    #gnx0 - gnx999 : first col width - 1000 col width






# stairs = []
# frontstairs = {
#     'pos' : (11.445,2.26,0),
#     'step_num' : 7,
#     'model' : '1',
#     'curve' : False,
#     'max_width' : 2.270,
#     'depth' : 0.3,
#     'shift' : 1,
#     'thickness' : 0.3
#     }

# stairs.append(frontstairs)


# for stair in stairs:
#     makestairs({stair})
# floor1 = {
#     'position': (0,0,0),
#     'wallheight': 2.510,
#     'wallthickness': 0.1,
#     'walls': walls,
#     'floorindex': 1,
#     'mergewalls': True,
#     'addfloor': True,
#     'baseboard': False
# }

# wallheight = 2.510
# wallthickness = 0.1
# floorindex = 1
# position = (0,3.15,0)
# walls = [
#     {
#         'length': 3.14,
#         'advanced': False,
#     }
# ]

# floors.append({
#     'position': position,
#     'wallheight': wallheight,
#     'wallthickness': wallthickness,
#     'walls': walls,
#     'floorindex': floorindex,
#     'mergewalls': False,
#     'addfloor': False,
#     'baseboard': False
# })

# wallheight = 2.510
# wallthickness = 0.1
# floorindex = 1
# position = (3.14,0,0)
# walls = [
#     {
#         'length': 6.340,
#         'advanced': True,
#         'angle': 90.0
#     }
# ]

# floors.append({
#     'position': position,
#     'wallheight': wallheight,
#     'wallthickness': wallthickness,
#     'walls': walls,
#     'floorindex': floorindex,
#     'mergewalls': False,
#     'addfloor': False,
#     'baseboard': False
# })




# def makeroom(unit):
#     setcursor(unit['position'])
#     bpy.ops.mesh.archimesh_room() # create room - linked walls
#     room = bpy.context.active_object # select newest object as room

#     room.RoomGenerator[0].wall_num = len(unit['walls'])
#     room.RoomGenerator[0].room_height = unit['wallheight']
#     room.RoomGenerator[0].wall_width = unit['wallthickness']
#     room.RoomGenerator[0].floor = True
#     room.RoomGenerator[0].merge = True
#     room.RoomGenerator[0].baseboard = False

#     for index, wall in enumerate(unit['walls']):
#         # print(index,wall['length'],wall['advanced'],wall['angle'])
#         currentwall = room.RoomGenerator[0].walls[index]
#         currentwall.w = wall['length']
#         currentwall.a = wall['advanced']
#         if currentwall.a:
#             currentwall.r = wall['angle']

# for floor in floors:
#     makeroom(floor)


# for floor in floors:
#     floorindex = floor['floorindex']
#     for room in floor:
#         makeroom(room)