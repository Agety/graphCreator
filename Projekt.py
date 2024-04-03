import bpy
import code
from locale import currency
import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/a?format=json%22")

if response.ok == True:
    data = response.json()[0]
    rates = data["rates"]
    
spacing = 1.5

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

color_column = bpy.data.materials.new(name='color_column')
color_column.diffuse_color = (0.446461, 0, 1,1)
color_text = bpy.data.materials.new(name='color_text')
color_text.diffuse_color = (1, 1, 1, 1)

green = bpy.data.materials.new(name='green')
yellow = bpy.data.materials.new(name='yellow')
red = bpy.data.materials.new(name='red')
green.diffuse_color = (0, 1, 0, 1)
yellow.diffuse_color = (1, 1, 0, 1)
red.diffuse_color = (1, 0, 0, 1)


for placemant, object in enumerate(rates):
    bpy.ops.mesh.primitive_plane_add(size=1)
    new_select = bpy.context.object
    new_select.active_material = color_column
    
    for vert in new_select.data.vertices:  #getting all vertices as list
        vert.co[1] += 0.5       #vert.co is a list of coordinates [x,y,z] 
        vert.co[0] += (placemant * spacing) + 0.5
        
    new_select.scale = (1, object['mid'] * 2, 1) #changing scale
    
    bpy.ops.object.text_add()
    bpy.context.object.data.align_x = 'RIGHT' 
    bpy.context.object.data.align_y = 'CENTER' 
    bpy.ops.transform.rotate(value = -1.5700)
    bpy.ops.transform.translate(value = ((placemant * spacing) + 0.5, -0.5, 0))
    bpy.context.object.data.body = str(object['code'])
    bpy.context.object.data.materials.append(color_text)
    
    bpy.ops.object.text_add()
    bpy.context.object.data.align_x = 'RIGHT' 
    bpy.context.object.data.align_y = 'CENTER'
    bpy.ops.transform.rotate(value = -1.5700)
    bpy.ops.transform.translate(value = ((placemant * spacing) + 0.5, object['mid'] * 2 + 5, 0))
    bpy.context.object.data.body = str(object['mid'])
    
    if object['mid'] < 1:
        bpy.context.object.data.materials.append(red)
    elif 3 > object['mid'] > 1:
        bpy.context.object.data.materials.append(yellow)
    else:
        bpy.context.object.data.materials.append(green)