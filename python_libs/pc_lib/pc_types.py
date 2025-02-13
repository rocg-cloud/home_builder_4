import bpy
import os, math
from . import pc_utils, pc_unit, pc_const
import xml.etree.ElementTree as ET

class HB_XML():
    
    tree = None
    
    def __init__(self):
        pass
    
    def create_tree(self):
        root = ET.Element('Root',{'Application':'Home Builder','ApplicationVersion':'7.0'})
        self.tree = ET.ElementTree(root)
        return root
    
    def add_element(self,root,elm_name,attrib_name=""):
        if attrib_name == "":
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name,{'Name':attrib_name})
        root.append(elm)
        return elm
    
    def add_element_with_text(self,root,elm_name,text):
        field = ET.Element(elm_name)
        field.text = text
        root.append(field)
    
    def format_xml_file(self,path):
        """ This makes the xml file readable as a txt doc.
            For some reason the xml.toprettyxml() function
            adds extra blank lines. This makes the xml file
            unreadable. This function just removes
            all of the blank lines.
            arg1: path to xml file
        """
        from xml.dom.minidom import parse
        
        xml = parse(path)
        pretty_xml = xml.toprettyxml()
        
        file = open(path,'w')
        file.write(pretty_xml)
        file.close()
        
        cleaned_lines = []
        with open(path,"r") as f:
            lines = f.readlines()
            for l in lines:
                l.strip()
                if "<" in l:
                    cleaned_lines.append(l)
            
        with open (path,"w") as f:
            f.writelines(cleaned_lines)
    
    def write(self,path):
        with open(path, 'w',encoding='utf-8') as file:
            self.tree.write(file,encoding='unicode')
            
        self.format_xml_file(path)

# class GeoPart:

#     coll = None
#     obj = None
#     node_group = None
#     modifier = None

#     def __init__(self,obj=None,filepath=""):
#         if obj:
#             self.obj = obj
#             for mod in self.obj.modifiers:
#                 if mod.type == 'NODES':
#                     self.mod = mod              

#         if filepath:
#             self.coll = bpy.context.view_layer.active_layer_collection.collection

#             self.obj = pc_utils.create_empty_mesh("Door")
#             self.coll.objects.link(self.obj)
            
#             # with bpy.data.libraries.load(filepath) as (data_from, data_to):
#             #     data_to.objects = data_from.objects
#             ngroup = None
#             if "Door" in bpy.data.node_groups:
#                 ngroup = bpy.data.node_groups["Door"]

#             else:
#                 with bpy.data.libraries.load(filepath) as (data_from, data_to):
#                     data_to.node_groups = ["Door"]
                    
#                 for node_group in data_to.node_groups:
#                     ngroup = node_group
#                     # if "geo_part" in obj and obj["geo_part"] == True:
#                     #     self.obj = obj
                    
#                     # self.coll.objects.link(obj)

#             mod = self.obj.modifiers.new("Door",'NODES')
#             mod.node_group = ngroup
#             self.node_group = mod.node_group
            
#     def get_prompt(self,name):
#         if name in self.obj.pyclone.prompts:
#             return self.obj.pyclone.prompts[name]
        
#         for calculator in self.obj.pyclone.calculators:
#             if name in calculator.prompts:
#                 return calculator.prompts[name]

#     def loc_x(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.location.x = value
#         else:
#             self.obj.pyclone.loc_x(expression,variables)

#     def loc_y(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.location.y = value
#         else:
#             self.obj.pyclone.loc_y(expression,variables)

#     def loc_z(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.location.z = value
#         else:
#             self.obj.pyclone.loc_z(expression,variables)           

#     def rot_x(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.rotation_euler.x = value
#         else:
#             self.obj.pyclone.rot_x(expression,variables)             

#     def rot_y(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.rotation_euler.y = value
#         else:
#             self.obj.pyclone.rot_y(expression,variables)      

#     def rot_z(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.obj.rotation_euler.z = value
#         else:
#             self.obj.pyclone.rot_z(expression,variables)      

#     def dim_x(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_2"] = value
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_2"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def dim_y(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_3"] = value
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_3"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def dim_z(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_4"] = bpy.utils.units.to_value('METRIC','LENGTH',str(value)+"m")
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_4"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def mirror_x(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_5"] = value
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_5"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def mirror_y(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_6"] = value
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_6"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def mirror_z(self,expression="",variables=[],value=0):
#         if expression == "":
#             self.mod["Input_7"] = value
#             return
#         driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["Input_7"]')
#         pc_utils.add_driver_variables(driver,variables)
#         driver.driver.expression = expression

#     def hide(self,expression="",variables=[],value=0):
#         hide = self.get_prompt("Hide")
#         if hide and expression == "":
#             hide.set_value(value)
#         else:
#             hide.set_formula(expression,variables)     

#     def prompt(self,prompt_name="",expression="",variables=[],value=0):
#         prompt = self.get_prompt(prompt_name)
#         if prompt and expression == "":
#             prompt.set_value(value)
#         else:
#             prompt.set_formula(expression,variables)   

class Room:

    scene = None

    def __init__(self,scene):
        pass

    def get_walls(self):
        wall_bps = []
        for obj in bpy.data.objects:
            if pc_const.IS_WALL_BP in obj and obj not in wall_bps:
                wall_bps.append(obj)
        walls = []
        for obj in wall_bps:
            walls.append(Assembly(obj))
        return walls

    def show_all_walls(self,context):
        walls = []
        for obj in context.scene.objects:
            if 'IS_WALL_BP' in obj:
                wall_is_hidden = False
                for child in obj.children:
                    if child.type == 'MESH' and child.hide_get():
                        wall_is_hidden = True
                if wall_is_hidden:
                    walls.append(obj)
        
        for wall in walls:
            bpy.ops.home_builder.show_hide_walls(wall_obj_bp=wall.name)

    def get_center_of_room(self):
        wall_assemblies = self.get_walls()

        first_wall = wall_assemblies[0]
        if first_wall:
            largest_x = first_wall.obj_bp.matrix_world[0][3]
            largest_y = first_wall.obj_bp.matrix_world[1][3]
            smallest_x = first_wall.obj_bp.matrix_world[0][3]
            smallest_y = first_wall.obj_bp.matrix_world[1][3]
            tallest_wall = first_wall.obj_z.location.z

        for assembly in wall_assemblies:
            start_point = (assembly.obj_bp.matrix_world[0][3],assembly.obj_bp.matrix_world[1][3],0)
            end_point = (assembly.obj_x.matrix_world[0][3],assembly.obj_x.matrix_world[1][3],0)
            if assembly.obj_z.location.z > tallest_wall:
                tallest_wall = assembly.obj_z.location.z
            
            if start_point[0] > largest_x:
                largest_x = start_point[0]
            if start_point[1] > largest_y:
                largest_y = start_point[1]
            if start_point[0] < smallest_x:
                smallest_x = start_point[0]
            if start_point[1] < smallest_y:
                smallest_y = start_point[1]
            if end_point[0] > largest_x:
                largest_x = end_point[0]
            if end_point[1] > largest_y:
                largest_y = end_point[1]
            if end_point[0] < smallest_x:
                smallest_x = end_point[0]
            if end_point[1] < smallest_y:
                smallest_y = end_point[1]

        if largest_x > smallest_x:
            x = (largest_x - smallest_x)/2 + smallest_x
        else:
            x = (smallest_x - largest_x)/2 + largest_x

        if largest_y > smallest_y:
            y = (largest_y - smallest_y)/2 + smallest_y
        else:
            y = (smallest_y - largest_y)/2 + largest_y

        z = tallest_wall - pc_unit.inch(.01)

        width = largest_x - smallest_x
        depth = largest_y - smallest_y
        if width > depth:
            size = width
        else:
            size = depth
        return x,y,z,size  


class Assembly:

    coll = None
    obj_bp = None
    obj_x = None
    obj_y = None
    obj_z = None
    obj_prompts = None
    prompts = {}

    def __init__(self,obj_bp=None,filepath=""):
        if obj_bp:
            self.coll = bpy.context.view_layer.active_layer_collection.collection
            self.obj_bp = obj_bp
            for child in obj_bp.children:
                if "obj_x" in child:
                    self.obj_x = child
                if "obj_y" in child:
                    self.obj_y = child           
                if "obj_z" in child:
                    self.obj_z = child
                if "obj_prompts" in child:
                    self.obj_prompts = child    

        if filepath:
            self.coll = bpy.context.view_layer.active_layer_collection.collection

            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.objects = data_from.objects

            for obj in data_to.objects:
                if "obj_bp" in obj and obj["obj_bp"] == True:
                    self.obj_bp = obj
                if "obj_x" in obj and obj["obj_x"] == True:
                    self.obj_x = obj
                if "obj_y" in obj and obj["obj_y"] == True:
                    self.obj_y = obj
                if "obj_z" in obj and obj["obj_z"] == True:
                    self.obj_z = obj
                if "obj_prompts" in obj and obj["obj_prompts"] == True:
                    self.obj_prompts = obj
                
                self.coll.objects.link(obj)

    def update_vector_groups(self):
        """ 
        This is used to add all of the vector groups to 
        an assembly this should be called everytime a new object
        is added to an assembly.
        """
        vgroupslist = []
        objlist = []
        
        for child in self.obj_bp.children:
            if child.type == 'EMPTY' and 'obj_prompts' not in child:
                vgroupslist.append(child.name)
            if child.type == 'MESH':
                objlist.append(child)
        
        for obj in objlist:
            for vgroup in vgroupslist:
                if vgroup not in obj.vertex_groups:
                    obj.vertex_groups.new(name=vgroup)

    def create_assembly(self,assembly_name="New Assembly"):
        """ 
        This creates the basic structure for an assembly.
        This must be called first when creating an assembly from a script.
        """
        bpy.ops.object.select_all(action='DESELECT')

        self.coll = bpy.context.view_layer.active_layer_collection.collection

        self.obj_bp = bpy.data.objects.new(assembly_name,None)
        self.obj_bp.location = (0,0,0)
        self.obj_bp["obj_bp"] = True
        self.obj_bp.empty_display_type = 'ARROWS'
        self.obj_bp.empty_display_size = .1           
        self.coll.objects.link(self.obj_bp)
        self.obj_bp['IS_ASSEMBLY_BP'] = True

        self.obj_x = bpy.data.objects.new("OBJ_X",None)
        self.obj_x.location = (0,0,0)
        self.obj_x.parent = self.obj_bp
        self.obj_x["obj_x"] = True
        self.obj_x.empty_display_type = 'SPHERE'
        self.obj_x.empty_display_size = .1  
        self.obj_x.lock_location[0] = False       
        self.obj_x.lock_location[1] = True
        self.obj_x.lock_location[2] = True
        self.obj_x.lock_rotation[0] = True     
        self.obj_x.lock_rotation[1] = True   
        self.obj_x.lock_rotation[2] = True      
        self.coll.objects.link(self.obj_x)

        self.obj_y = bpy.data.objects.new("OBJ_Y",None)
        self.obj_y.location = (0,0,0)
        self.obj_y.parent = self.obj_bp
        self.obj_y["obj_y"] = True
        self.obj_y.empty_display_type = 'SPHERE'
        self.obj_y.empty_display_size = .1     
        self.obj_y.lock_location[0] = True       
        self.obj_y.lock_location[1] = False
        self.obj_y.lock_location[2] = True
        self.obj_y.lock_rotation[0] = True     
        self.obj_y.lock_rotation[1] = True   
        self.obj_y.lock_rotation[2] = True                    
        self.coll.objects.link(self.obj_y)      

        self.obj_z = bpy.data.objects.new("OBJ_Z",None)
        self.obj_z.location = (0,0,0)
        self.obj_z.parent = self.obj_bp
        self.obj_z["obj_z"] = True
        self.obj_z.empty_display_type = 'SINGLE_ARROW'
        self.obj_z.empty_display_size = .2     
        self.obj_z.lock_location[0] = True
        self.obj_z.lock_location[1] = True
        self.obj_z.lock_location[2] = False
        self.obj_z.lock_rotation[0] = True     
        self.obj_z.lock_rotation[1] = True   
        self.obj_z.lock_rotation[2] = True               
        self.coll.objects.link(self.obj_z)

        self.obj_prompts = bpy.data.objects.new("OBJ_PROMPTS",None)
        self.obj_prompts.location = (0,0,0)
        self.obj_prompts.parent = self.obj_bp
        self.obj_prompts.empty_display_size = 0      
        self.obj_prompts.lock_location[0] = True
        self.obj_prompts.lock_location[1] = True
        self.obj_prompts.lock_location[2] = True
        self.obj_prompts.lock_rotation[0] = True     
        self.obj_prompts.lock_rotation[1] = True   
        self.obj_prompts.lock_rotation[2] = True           
        self.obj_prompts["obj_prompts"] = True
        self.coll.objects.link(self.obj_prompts)

    def create_assembly_collection(self,name):
        bpy.ops.object.select_all(action='DESELECT')
        pc_utils.select_object_and_children(self.obj_bp)
        bpy.ops.collection.create(name=name)

        collection = bpy.data.collections[name]
        collection.pyclone.assembly_bp = self.obj_bp
        return collection

    def create_geo_part(self,name):
        if 'HBGeoNodePart' in bpy.data.node_groups:
            node = bpy.data.node_groups['HBGeoNodePart']
            mesh = bpy.data.meshes.new(name)
            obj = bpy.data.objects.new(name,mesh)
            mod = obj.modifiers.new('HBPart','NODES')
            mod.node_group = node
            self.coll.objects.link(obj)
            obj.parent = self.obj_bp
            obj['hb_geo_part'] = True
        else:
            obj = self.add_object_from_file(pc_utils.get_geo_node_path())
            obj.name = name
            obj['hb_geo_part'] = True
        return GeoNodeObject(obj)
    
    def add_geo_node_cutpart(self,name):
        cutpart = GeoNodeCutpart()
        cutpart.create(name)
        cutpart.obj.parent = self.obj_bp
        return cutpart

    def add_geo_node_cage(self,name):
        cage = GeoNodeCage()
        cage.create(name)
        cage.obj.parent = self.obj_bp
        return cage

    def create_cube(self,name="Cube",size=(0,0,0)):
        """ This will create a cube mesh and assign mesh hooks
        """
        # When assigning vertices to a hook 
        # the transformation is made so the size must be 0     
        obj_mesh = pc_utils.create_cube_mesh("Cube",size)
        self.add_object(obj_mesh)

        vgroup = obj_mesh.vertex_groups[self.obj_x.name]
        vgroup.add([2,3,6,7],1,'ADD')        

        vgroup = obj_mesh.vertex_groups[self.obj_y.name]
        vgroup.add([1,2,5,6],1,'ADD')

        vgroup = obj_mesh.vertex_groups[self.obj_z.name]
        vgroup.add([4,5,6,7],1,'ADD')        

        hook = obj_mesh.modifiers.new('XHOOK','HOOK')
        hook.object = self.obj_x
        hook.vertex_indices_set([2,3,6,7])

        hook = obj_mesh.modifiers.new('YHOOK','HOOK')
        hook.object = self.obj_y
        hook.vertex_indices_set([1,2,5,6])

        hook = obj_mesh.modifiers.new('ZHOOK','HOOK')
        hook.object = self.obj_z
        hook.vertex_indices_set([4,5,6,7])

        return obj_mesh

    def add_prompt(self,name,prompt_type,value,combobox_items=[]):
        prompt = self.obj_prompts.pyclone.add_prompt(prompt_type,name)
        prompt.set_value(value)
        if prompt_type == 'COMBOBOX':
            for item in combobox_items: 
                i = prompt.combobox_items.add()
                i.name = item
        return prompt

    def add_empty(self,obj_name):
        obj = bpy.data.objects.new(obj_name,None)
        self.add_object(obj)
        return obj

    def add_light(self,obj_name,light_type):
        light = bpy.data.lights.new(obj_name,light_type)
        obj = bpy.data.objects.new(obj_name,light)
        self.add_object(obj)
        return obj

    def add_object(self,obj):
        obj.location = (0,0,0)
        obj.parent = self.obj_bp
        self.coll.objects.link(obj)
        self.update_vector_groups()

    def add_assembly(self,assembly):
        if assembly.obj_bp is None:
            if hasattr(assembly,'draw'):
                assembly.draw()
        assembly.obj_bp.location = (0,0,0)
        assembly.obj_bp.parent = self.obj_bp
        return assembly

    def add_assembly_from_file(self,filepath):
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = data_from.objects

        obj_bp = None

        for obj in data_to.objects:
            if not obj.parent:
                obj_bp = obj
            self.coll.objects.link(obj)

        obj_bp.parent = self.obj_bp
        return Assembly(obj_bp)

    def add_object_from_file(self,filepath):
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            self.coll.objects.link(obj)
            obj.parent = self.obj_bp
            return obj

    def set_name(self,name):
        self.obj_bp.name = name

    def set_id_properties(self):
        if 'PROMPT_ID' in self.obj_bp:
            for child in self.obj_bp.children_recursive:
                child['PROMPT_ID'] = self.obj_bp['PROMPT_ID']
        if 'MENU_ID' in self.obj_bp:
            for child in self.obj_bp.children_recursive:
                child['MENU_ID'] = self.obj_bp['MENU_ID']

    def get_prompt(self,name):
        if name in self.obj_prompts.pyclone.prompts:
            return self.obj_prompts.pyclone.prompts[name]
        
        for calculator in self.obj_prompts.pyclone.calculators:
            if name in calculator.prompts:
                return calculator.prompts[name]

    def get_calculator(self,name):
        if name in self.obj_prompts.pyclone.calculators:
            return self.obj_prompts.pyclone.calculators[name]

    def update_calculators(self):
        for calculator in self.obj_prompts.pyclone.calculators:
            calculator.calculate()

    def set_prompts(self):
        for key in self.prompts:
            if key in self.obj_prompts.pyclone.prompts:
                if key in self.obj_prompts.pyclone.prompts:
                    prompt = self.obj_prompts.pyclone.prompts[key]
                    prompt.set_value(self.prompts[key])

    def get_prompt_dict(self):
        prompt_dict = {}
        for prompt in self.obj_prompts.pyclone.prompts:
            prompt_dict[prompt.name] = prompt.get_value()
        return prompt_dict

    def get_dim_x_var(self,var_name):
        return self.obj_x.pyclone.get_var('location.x',var_name)

    def get_dim_y_var(self,var_name):
        return self.obj_y.pyclone.get_var('location.y',var_name)

    def get_dim_z_var(self,var_name):
        return self.obj_z.pyclone.get_var('location.z',var_name)

    def get_hide_var(self,var_name):
        return self.get_prompt("Hide").get_var(var_name)

    def get_loc_x_var(self,var_name):
        return self.obj_bp.pyclone.get_var("location.x",var_name)

    def get_loc_y_var(self,var_name):
        return self.obj_bp.pyclone.get_var("location.y",var_name)

    def get_loc_z_var(self,var_name):
        return self.obj_bp.pyclone.get_var("location.z",var_name)

    def add_dummy_variable(self,parent):
        for driver in self.obj_x.animation_data.drivers:
            dummy_var = driver.driver.variables.new()
            dummy_var.name = 'DUMMY_VAR'
            dummy_var.type = 'TRANSFORMS'
            dummy_var.targets[0].id = parent

    def hide(self,expression="",variables=[],value=0):
        hide = self.get_prompt("Hide")
        if expression == "":
            hide.set_value(value = value)
        else:
            hide.set_formula(expression,variables)

    def loc_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.location.x = value
        else:
            self.obj_bp.pyclone.loc_x(expression,variables)

    def loc_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.location.y = value
        else:
            self.obj_bp.pyclone.loc_y(expression,variables)

    def loc_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.location.z = value
        else:
            self.obj_bp.pyclone.loc_z(expression,variables)           

    def rot_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.rotation_euler.x = value
        else:
            self.obj_bp.pyclone.rot_x(expression,variables)             

    def rot_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.rotation_euler.y = value
        else:
            self.obj_bp.pyclone.rot_y(expression,variables)      

    def rot_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_bp.rotation_euler.z = value
        else:
            self.obj_bp.pyclone.rot_z(expression,variables)      

    def dim_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_x.location.x = value
        else:
            self.obj_x.pyclone.loc_x(expression,variables)          

    def dim_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_y.location.y = value
        else:
            self.obj_y.pyclone.loc_y(expression,variables)    

    def dim_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj_z.location.z = value
        else:
            self.obj_z.pyclone.loc_z(expression,variables)                                                                      

class Wall(Assembly):

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  
    
    def draw_wall(self,wall_length,wall_height,wall_thickness):
        self.create_assembly("Wall Mesh")

        #ASSIGN PROPERTY
        self.obj_bp["IS_WALL_BP"] = True
        self.obj_bp["PROMPT_ID"] = "home_builder.wall_prompts" 
        self.obj_bp["MENU_ID"] = "HOME_BUILDER_MT_wall_commands"

        #Set Default Dimensions
        self.obj_x.location.x = wall_length
        self.obj_y.location.y = wall_thickness
        self.obj_z.location.z = wall_height

        #Add Objects
        left_angle_empty = self.add_empty("Left Angle")
        right_angle_empty = self.add_empty("Right Angle")

        size = (0,0,0)
        obj_mesh = pc_utils.create_cube_mesh("Wall Mesh",size)
        obj_mesh.color = [0.252832, 0.500434, 0.735662, 1.000000]
        obj_mesh['IS_WALL_MESH'] = True
        self.add_object(obj_mesh)

        #Assign Mesh Hooks
        vgroup = obj_mesh.vertex_groups[left_angle_empty.name]
        vgroup.add([1,5],1,'ADD')  

        vgroup = obj_mesh.vertex_groups[right_angle_empty.name]
        vgroup.add([2,6],1,'ADD')

        vgroup = obj_mesh.vertex_groups[self.obj_x.name]
        vgroup.add([3,7],1,'ADD')        

        vgroup = obj_mesh.vertex_groups[self.obj_z.name]
        vgroup.add([4,5,6,7],1,'ADD')        

        hook = obj_mesh.modifiers.new('XHOOK','HOOK')
        hook.object = self.obj_x
        hook.vertex_indices_set([3,7])

        hook = obj_mesh.modifiers.new('LEFTANGLE','HOOK')
        hook.object = left_angle_empty
        hook.vertex_indices_set([1,5])

        hook = obj_mesh.modifiers.new('RIGHTANGLE','HOOK')
        hook.object = right_angle_empty
        hook.vertex_indices_set([2,6])        

        hook = obj_mesh.modifiers.new('ZHOOK','HOOK')
        hook.object = self.obj_z
        hook.vertex_indices_set([4,5,6,7])

        #Assign Drivers
        length = self.obj_x.pyclone.get_var('location.x','length')
        wall_thickness_var = self.obj_y.pyclone.get_var('location.y','wall_thickness_var')

        left_angle = self.add_prompt("Left Angle",'ANGLE',0)
        right_angle = self.add_prompt("Right Angle",'ANGLE',0)

        left_angle_var = left_angle.get_var('left_angle_var')
        right_angle_var = right_angle.get_var('right_angle_var')

        left_angle_empty.pyclone.loc_x('tan(left_angle_var)*wall_thickness_var',[left_angle_var,wall_thickness_var])
        left_angle_empty.pyclone.loc_y('wall_thickness_var',[wall_thickness_var])

        right_angle_empty.pyclone.loc_x('length+tan(right_angle_var)*wall_thickness_var',[length,right_angle_var,wall_thickness_var])
        right_angle_empty.pyclone.loc_y('wall_thickness_var',[wall_thickness_var])

        #Add Material Pointer
        bpy.context.view_layer.objects.active = obj_mesh
        bpy.ops.object.material_slot_add()
        pointer = obj_mesh.pyclone.pointers.add()
        pointer.name = "Wall"
        pointer.pointer_name = "Walls"

        # obj_mesh.lock_location = (True,True,True)
        # obj_mesh.lock_rotation = (True,True,True)
        pc_utils.assign_materials_to_object(obj_mesh)

    def get_wall_assembly_bps_by_tag(self,tag,loc_sort='X'):
        """ This returns a sorted list of all of the assemblies base points
            parented to the wall
        """
        list_obj_bp = []
        for child in self.obj_bp.children:
            cabinet_bp = pc_utils.get_bp_by_tag(child,tag)
            if cabinet_bp:
                list_obj_bp.append(child)
        if loc_sort == 'X':
            list_obj_bp.sort(key=lambda obj: obj.location.x, reverse=False)
        if loc_sort == 'Y':
            list_obj_bp.sort(key=lambda obj: obj.location.y, reverse=False)            
        if loc_sort == 'Z':
            list_obj_bp.sort(key=lambda obj: obj.location.z, reverse=False)
        return list_obj_bp

class Assembly_Layout():

    VISIBLE_LINESET_NAME = "Visible Lines"
    HIDDEN_LINESET_NAME = "Hidden Lines"
    HIDDEN_LINE_DASH_PX = 10
    HIDDEN_LINE_GAP_PX = 10

    scene = None
    camera = None
    dimension_collection = None

    def __init__(self,scene=None):
        self.scene = scene
        self.camera = scene.camera
        for collection in self.scene.collection.children:
            if collection.pyclone.is_dimension_collection:
                self.dimension_collection = collection
                break

    def create_linestyles(self):
        linestyles = bpy.data.linestyles
        linestyles.new(self.VISIBLE_LINESET_NAME)
        
        hidden_linestyle = linestyles.new(self.HIDDEN_LINESET_NAME)
        hidden_linestyle.use_dashed_line = True
        hidden_linestyle.dash1 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.dash2 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.dash3 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.gap1 = self.HIDDEN_LINE_GAP_PX
        hidden_linestyle.gap2 = self.HIDDEN_LINE_GAP_PX
        hidden_linestyle.gap3 = self.HIDDEN_LINE_GAP_PX

    def create_linesets(self):
        f_settings = self.scene.view_layers[0].freestyle_settings
        linestyles = bpy.data.linestyles
        
        visible_lineset = f_settings.linesets.new(self.VISIBLE_LINESET_NAME)
        visible_lineset.linestyle = linestyles[self.VISIBLE_LINESET_NAME]
        visible_lineset.select_by_collection = True
        visible_lineset.collection_negation = 'EXCLUSIVE'
        visible_lineset.collection = self.dimension_collection

        hidden_lineset = f_settings.linesets.new(self.HIDDEN_LINESET_NAME)
        hidden_lineset.linestyle = linestyles[self.HIDDEN_LINESET_NAME]
        
        hidden_lineset.select_by_visibility = True
        hidden_lineset.visibility = 'HIDDEN'
        hidden_lineset.select_by_edge_types = True
        hidden_lineset.select_by_face_marks = False
        hidden_lineset.select_by_collection = True
        hidden_lineset.select_by_image_border = False
        
        hidden_lineset.select_silhouette = True
        hidden_lineset.select_border = False
        hidden_lineset.select_contour = False
        hidden_lineset.select_suggestive_contour = False
        hidden_lineset.select_ridge_valley = False
        hidden_lineset.select_crease = False
        hidden_lineset.select_edge_mark = True
        hidden_lineset.select_external_contour = False
        hidden_lineset.select_material_boundary = False
        hidden_lineset.collection_negation = 'EXCLUSIVE'
        hidden_lineset.collection = self.dimension_collection

    def clear_unused_linestyles(self):
        for linestyle in bpy.data.linestyles:
            if linestyle.users == 0:
                bpy.data.linestyles.remove(linestyle)

    def setup_assembly_layout(self):
        self.create_linestyles()

        self.dimension_collection = bpy.data.collections.new(self.scene.name + ' DIM')
        self.dimension_collection.pyclone.is_dimension_collection = True
        bpy.context.view_layer.active_layer_collection.collection.children.link(self.dimension_collection)

        props = self.scene.pyclone
        props.is_view_scene = True
        self.scene.render.use_freestyle = True
        view_settings = self.scene.view_settings
        view_settings.view_transform = 'Standard'
        view_settings.look = 'High Contrast'

        self.create_linesets()

    def add_assembly_view(self,collection):
        obj = bpy.data.objects.new(collection.name,None)
        obj.instance_type = 'COLLECTION'
        obj.instance_collection = collection
        obj.empty_display_size = .01
        obj.location = (0,0,0)
        obj.rotation_euler = (0,0,0)
        self.scene.view_layers[0].active_layer_collection.collection.objects.link(obj)  
        obj.select_set(True)
        obj.pyclone.is_view_object = True
        return obj

    def add_layout_camera(self):
        cam = bpy.data.cameras.new('Camera ' + self.scene.name)
        cam.type = 'ORTHO'
        cam.ortho_scale = 1
        self.camera = bpy.data.objects.new('Camera ' + self.scene.name,cam)
        self.scene.view_layers[0].active_layer_collection.collection.objects.link(self.camera)  
        #SET RESOLUTION TO PAGE SIZE RATIO DEFAULT PAGE SIZE IS 8.5 x 11
        self.scene.render.resolution_x = int(11 * 140)
        self.scene.render.resolution_y = int(8.5 * 140)
        self.scene.camera = self.camera

        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.data:                      
                            with bpy.context.temp_override(window=window, area=area, region=region):
                                bpy.ops.view3d.view_camera()
                                bpy.ops.view3d.view_center_camera()   
                            break          

    def add_3d_layout_camera(self):
        spd = bpy.context.space_data
        bpy.ops.object.camera_add(align='VIEW')
        camera = bpy.context.active_object
        self.camera = camera
        camera["PROMPT_ID"] = "camera_presets.camera_properties"   
        bpy.ops.view3d.camera_to_view()
        camera.data.clip_start = spd.clip_start
        camera.data.clip_end = spd.clip_end
        camera.data.ortho_scale = 200.0
        camera.data.sensor_width = 72  
        camera.data.lens = spd.lens
        spd.region_3d.view_camera_offset = [0,0]
        spd.region_3d.view_camera_zoom = 29.0746         

        self.scene.render.resolution_x = int(11 * 140)
        self.scene.render.resolution_y = int(8.5 * 140)
  

class Title_Block(Assembly):

    obj_drawing_title = None
    obj_description = None
    obj_scale = None
    obj_drawn_by = None
    obj_drawing_number = None
    obj_revision_number = None
    obj_original_date = None
    obj_revision_date = None

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  
        if self.obj_bp:
            for child in obj_bp.children:
                if "IS_DRAWING_TITLE" in child:
                    self.obj_drawing_title = child
                if "IS_DESCRIPTION" in child:
                    self.obj_description = child         
                if "IS_SCALE" in child:
                    self.obj_scale = child         
                if "IS_DRAWN_BY" in child:
                    self.obj_drawn_by = child         
                if "IS_DRAWING_NUMBER" in child:
                    self.obj_drawing_number = child        
                if "IS_REVISION_NUMBER" in child:
                    self.obj_revision_number = child          
                if "IS_ORIGINAL_DATE" in child:
                    self.obj_original_date = child             
                if "IS_REVISION_DATE" in child:
                    self.obj_revision_date = child                  
                if child.type == 'FONT':
                    self.obj_text = child   

    def create_title_block(self,layout_view,title_block_name="Title Block"):
        collection = layout_view.dimension_collection
        mat = pc_utils.get_dimension_material()

        PATH = os.path.join(os.path.dirname(__file__),'assets','Title Blocks',title_block_name + ".blend")

        with bpy.data.libraries.load(PATH) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            if "obj_bp" in obj:
                self.obj_bp = obj            
            if "obj_x" in obj:
                self.obj_x = obj
            if "obj_y" in obj:
                self.obj_y = obj           
            if "obj_z" in obj:
                self.obj_z = obj
            if "obj_prompts" in obj:
                self.obj_prompts = obj       
            if "IS_DRAWING_TITLE" in obj:
                self.obj_drawing_title = obj
            if "IS_DESCRIPTION" in obj:
                self.obj_description = obj         
            if "IS_SCALE" in obj:
                self.obj_scale = obj         
            if "IS_DRAWN_BY" in obj:
                self.obj_drawn_by = obj         
            if "IS_DRAWING_NUMBER" in obj:
                self.obj_drawing_number = obj        
            if "IS_REVISION_NUMBER" in obj:
                self.obj_revision_number = obj          
            if "IS_ORIGINAL_DATE" in obj:
                self.obj_original_date = obj             
            if "IS_REVISION_DATE" in obj:
                self.obj_revision_date = obj  
            obj["PROMPT_ID"] = 'pc_assembly.show_title_block_properties'                           
            collection.objects.link(obj)

        self.obj_bp.parent = layout_view.camera

        self.obj_bp.location.x = -0.5
        self.obj_bp.location.y = -0.386363 
        self.obj_bp.location.z = -0.694355

        for child in self.obj_bp.children:
            for slot in child.material_slots:
                if slot.material == None:
                    slot.material = mat
            if child.type == 'EMPTY':
                child.hide_viewport = True

    def draw_ui(self,context,layout):
        row = layout.row()
        row.label(text="Drawing Title:")
        row.prop(self.obj_drawing_title.data,'body',text="")

        row = layout.row()
        row.label(text="Description:")
        row.prop(self.obj_description.data,'body',text="")

        row = layout.row()
        row.label(text="Scale:")
        row.prop(self.obj_scale.data,'body',text="")

        row = layout.row()
        row.label(text="Drawn By:")
        row.prop(self.obj_drawn_by.data,'body',text="")

        row = layout.row()
        row.label(text="Drawing Number:")
        row.prop(self.obj_drawing_number.data,'body',text="")

        row = layout.row()
        row.label(text="Revision Number:")
        row.prop(self.obj_revision_number.data,'body',text="")

        row = layout.row()
        row.label(text="Original Date:")
        row.prop(self.obj_original_date.data,'body',text="")                                                

        row = layout.row()
        row.label(text="Revision Date:")
        row.prop(self.obj_revision_date.data,'body',text="")  

class Annotation(Assembly):

    obj_text = None

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  
        if self.obj_bp:
            for child in obj_bp.children:
                if child.type == 'FONT':
                    self.obj_text = child   

    def create_annotation(self,layout_view=None):
        PATH = os.path.join(os.path.dirname(__file__),'assets',"Annotation_Arrow.blend")

        with bpy.data.libraries.load(PATH) as (data_from, data_to):
            data_to.objects = data_from.objects

        if layout_view:
            collection = layout_view.dimension_collection
        else:
            collection = bpy.context.view_layer.active_layer_collection.collection

        for obj in data_to.objects:
            if "obj_bp" in obj:
                self.obj_bp = obj     
                self.obj_bp['IS_ANNOTATION'] = True         
            if "obj_x" in obj:
                self.obj_x = obj
            if "obj_y" in obj:
                self.obj_y = obj           
            if "obj_z" in obj:
                self.obj_z = obj
            if "obj_prompts" in obj:
                self.obj_prompts = obj         
            if obj.type == 'FONT':
                self.obj_text = obj     
            obj["PROMPT_ID"] = 'pc_assembly.show_annotation_properties'                       
            collection.objects.link(obj)

    def draw_ui(self,context,layout):
        arrow_height = self.get_prompt("Arrow Height")
        arrow_length = self.get_prompt("Arrow Length")
        line_thickness = self.get_prompt("Line Thickness")

        row = layout.row()
        row.label(text="Annotation Text:")
        row.prop(self.obj_text.data,'body',text="")

        row = layout.row() 
        row.label(text="Arrow Size:")
        row.prop(arrow_height,'distance_value',text="Height")     
        row.prop(arrow_length,'distance_value',text="Length")  

        row = layout.row()
        row.label(text="Line Thickness:")
        row.prop(line_thickness,'distance_value',text="")   

        row = layout.row()
        row.label(text="Flip Text:")
        row.prop(self.obj_text.pyclone,'flip_x',text="X")            
        row.prop(self.obj_text.pyclone,'flip_y',text="Y")     
        

class GeoNodeObject():

    obj = None
    mod = None
    coll = None

    def __init__(self,obj=None,layout_view = None):
        if obj:
            self.obj = obj
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break            
        if layout_view:
            self.coll = layout_view.dimension_collection
        else:
            self.coll = bpy.context.view_layer.active_layer_collection.collection

    def get_geo_node(self,path,geo_node_name):
        if geo_node_name in bpy.data.node_groups:
            node = bpy.data.node_groups[geo_node_name]
            cage = bpy.data.meshes.new(geo_node_name)
            self.obj = bpy.data.objects.new(geo_node_name,cage)
            self.mod = self.obj.modifiers.new('GeometryNodes','NODES')
            self.mod.node_group = node
        else:
            with bpy.data.libraries.load(path) as (data_from, data_to):
                data_to.objects = data_from.objects
            for obj in data_to.objects:
                self.obj = obj
            self.obj.name = geo_node_name
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break        

    def add_assembly(self,assembly):
        if assembly.obj_bp is None:
            if hasattr(assembly,'draw'):
                assembly.draw()
        assembly.obj_bp.location = (0,0,0)
        assembly.obj_bp.parent = self.obj
        return assembly

    def add_dummy_variable(self,parent):
        for driver in self.obj.animation_data.drivers:
            dummy_var = driver.driver.variables.new()
            dummy_var.name = 'DUMMY_VAR'
            dummy_var.type = 'TRANSFORMS'
            dummy_var.targets[0].id = parent

    def add_assembly_from_file(self,filepath):
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = data_from.objects

        obj_bp = None

        for obj in data_to.objects:
            if not obj.parent:
                obj_bp = obj
            self.coll.objects.link(obj)

        obj_bp.parent = self.obj
        return Assembly(obj_bp)

    def add_object_from_file(self,filepath):
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            self.coll.objects.link(obj)
            obj.parent = self.obj
            return obj
        
    def add_empty(self,obj_name):
        obj = bpy.data.objects.new(obj_name,None)
        self.add_object(obj)
        return obj

    def add_light(self,obj_name,light_type):
        light = bpy.data.lights.new(obj_name,light_type)
        obj = bpy.data.objects.new(obj_name,light)
        self.add_object(obj)
        return obj

    def add_object(self,obj):
        obj.location = (0,0,0)
        obj.parent = self.obj
        self.coll.objects.link(obj)

    def add_geo_node_cage(self,name):
        part = GeoNodeCage()
        part.create(name)
        part.obj.parent = self.obj
        return part

    def add_geo_node_cutpart(self,name):
        part = GeoNodeCutpart()
        part.create(name)
        part.obj.parent = self.obj
        return part
    
    def set_id_properties(self):
        if 'PROMPT_ID' in self.obj:
            for child in self.obj.children_recursive:
                child['PROMPT_ID'] = self.obj['PROMPT_ID']
        if 'MENU_ID' in self.obj:
            for child in self.obj.children_recursive:
                child['MENU_ID'] = self.obj['MENU_ID']

    def assign_booleans(self):
        for child in self.obj.children_recursive:
            for boolean in child.pyclone.boolean_objects:
                mod = boolean.obj.modifiers.new(child.name,'BOOLEAN')
                mod.object = child
                mod.operation = 'DIFFERENCE'
                child.hide_viewport = True

    def get_var(self,input_name,name):
        node = self.mod.node_group      
        input_identifier = "" 
        for input in node.interface.items_tree:
            if input.name == input_name:
                input_identifier = input.identifier
                break        
        data_path = 'modifiers["' + self.mod.name + '"]["' + input_identifier + '"]'
        return self.obj.pyclone.get_var(data_path,name)

    def get_prompt_var(self,input_name,name):
        node = self.mod.node_group      
        input_identifier = "" 
        for input in node.interface.items_tree:
            if input.name == input_name:
                input_identifier = input.identifier
                break        
        data_path = 'modifiers["' + self.mod.name + '"]["' + input_identifier + '"]'
        return self.obj.pyclone.get_var(data_path,name)

    def get_loc_x_var(self,var_name):
        return self.obj.pyclone.get_var("location.x",var_name)

    def get_loc_y_var(self,var_name):
        return self.obj.pyclone.get_var("location.y",var_name)

    def get_loc_z_var(self,var_name):
        return self.obj.pyclone.get_var("location.z",var_name)
    
    def hide(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.hide_viewport = value
            self.obj.hide_render = value
        else:
            self.obj.pyclone.hide(expression,variables)

    def loc_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.location.x = value
        else:
            self.obj.pyclone.loc_x(expression,variables)

    def loc_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.location.y = value
        else:
            self.obj.pyclone.loc_y(expression,variables)

    def loc_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.location.z = value
        else:
            self.obj.pyclone.loc_z(expression,variables)           

    def rot_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.rotation_euler.x = value
        else:
            self.obj.pyclone.rot_x(expression,variables)             

    def rot_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.rotation_euler.y = value
        else:
            self.obj.pyclone.rot_y(expression,variables)      

    def rot_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.obj.rotation_euler.z = value
        else:
            self.obj.pyclone.rot_z(expression,variables)   

    def driver(self,name,expression="",variables=[]):
        input_identifier = ""
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]  
            input_identifier = node_input.identifier
        driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
        pc_utils.add_driver_variables(driver,variables)
        driver.driver.expression = expression
    
    def add_prompt(self,name,prompt_type,value,combobox_items=[]):
        prompt = self.obj.pyclone.add_prompt(prompt_type,name)
        prompt.set_value(value)
        if prompt_type == 'COMBOBOX':
            for item in combobox_items: 
                i = prompt.combobox_items.add()
                i.name = item
        return prompt

    def get_prompt(self,name):
        if name in self.obj.pyclone.prompts:
            return self.obj.pyclone.prompts[name]
        
        for calculator in self.obj.pyclone.calculators:
            if name in calculator.prompts:
                return calculator.prompts[name]
            
    def set_input(self,name,value=None):
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]    
            self.mod.node_group.interface_update(bpy.context)
            if hasattr(node_input,'subtype'):
                node_input.subtype = node_input.subtype            
            exec('self.mod["' + node_input.identifier + '"] = value')    

    def get_input(self,name):
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]
            return eval('self.mod["' + node_input.identifier + '"]')
            
    def get_hide_var(self,var_name):
        return self.obj.pyclone.get_var('hide_viewport',var_name)

    def draw_input(self,layout,name,text,icon=''):
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]
            if icon == '':
                layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text)
            else:
                layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text,icon=icon)

    def get_calculator(self,name):  
        if name in self.obj.pyclone.calculators:
            return self.obj.pyclone.calculators[name]
        


class GeoNodeCage(GeoNodeObject):

    geo_node_name = "GeoNodeCage"

    def get_dim_x_var(self,var_name):
        return self.get_var("Dim X",var_name)

    def get_dim_y_var(self,var_name):
        return self.get_var("Dim Y",var_name)

    def get_dim_z_var(self,var_name):
        return self.get_var("Dim Z",var_name)
        
    def dim_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Dim X",value)
        else:        
            node_input = self.mod.node_group.interface.items_tree["Dim X"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def dim_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Dim Y",value)
        else:        
            node_input = self.mod.node_group.interface.items_tree["Dim Y"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def dim_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Dim Z",value)
        else:
            node_input = self.mod.node_group.interface.items_tree["Dim Z"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def create(self,name=""):
        props = bpy.context.scene.pyclone
        path = os.path.join(os.path.dirname(__file__),'assets','GeoNodeObjects',self.geo_node_name + ".blend")
        self.get_geo_node(path,self.geo_node_name)                
        self.obj.name = name
        self.obj.hide_render = True
        self.obj["GeoNodeName"] = self.geo_node_name
        self.mod.node_group.interface_update(bpy.context)
        # self.mod.node_group.update()
        # self.obj['PROMPT_ID'] = 'pc_layout_view.show_dimension_properties'
        # self.obj['MENU_ID'] = 'CWP_MT_dimension_commands'
        if self.coll:
            self.coll.objects.link(self.obj)
        else:
            bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)
        self.obj.display.show_shadows = False
        self.obj.display_type = 'WIRE'
        self.obj.color = (0,0,0,1)


class GeoNodeCutpart(GeoNodeObject):

    geo_node_name = "GeoNodeCutpart"

    def get_dim_x_var(self,var_name):
        return self.get_var("Length",var_name)

    def get_dim_y_var(self,var_name):
        return self.get_var("Width",var_name)

    def get_dim_z_var(self,var_name):
        return self.get_var("Thickness",var_name)
    
    def dim_x(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Length",value)
        else:        
            node_input = self.mod.node_group.interface.items_tree["Length"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def dim_y(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Width",value)
        else:        
            node_input = self.mod.node_group.interface.items_tree["Width"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def dim_z(self,expression="",variables=[],value=0):
        if expression == "":
            self.set_input("Thickness",value)
        else:
            node_input = self.mod.node_group.interface.items_tree["Thickness"]  
            input_identifier = node_input.identifier
            driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
            pc_utils.add_driver_variables(driver,variables)
            driver.driver.expression = expression

    def create(self,name=""):
        props = bpy.context.scene.pyclone
        path = os.path.join(os.path.dirname(__file__),'assets','GeoNodeObjects',self.geo_node_name + ".blend")
        self.get_geo_node(path,self.geo_node_name)                        
        self.obj.name = name
        self.obj["GeoNodeName"] = self.geo_node_name
        # self.obj['PROMPT_ID'] = 'pc_layout_view.show_dimension_properties'
        # self.obj['MENU_ID'] = 'CWP_MT_dimension_commands'
        if self.coll:
            self.coll.objects.link(self.obj)
        else:
            bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)
        self.obj.display.show_shadows = False
        self.obj.color = (1,1,1,1)
    
    def draw_interface(self,layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        self.draw_input(row,"Length","Length")
        self.draw_input(row,"Mirror X","",icon='MOD_MIRROR')

        row = col.row(align=True)
        self.draw_input(row,"Width","Width")
        self.draw_input(row,"Mirror Y","",icon='MOD_MIRROR')

        row = col.row(align=True)
        self.draw_input(row,"Thickness","Thickness")
        self.draw_input(row,"Mirror Z","",icon='MOD_MIRROR')

class GeoNodeDimension(GeoNodeObject):

    geo_node_name = "GeoNodeDimension"

    def create(self,layout_view=None):
        mat = pc_utils.get_dimension_material()
        scene = bpy.context.scene
        props = scene.pyclone        
        if self.geo_node_name in bpy.data.node_groups:
            node = bpy.data.node_groups[self.geo_node_name]
            curve = bpy.data.curves.new('Dimension','CURVE')
            spline = curve.splines.new('BEZIER')
            spline.bezier_points.add(1)
            self.obj = bpy.data.objects.new('Dimension',curve)
            self.mod = self.obj.modifiers.new('HBDimension','NODES')
            self.mod.node_group = node
        else:
            PATH = os.path.join(os.path.dirname(__file__),'assets','GeoNodeObjects',self.geo_node_name + ".blend")
            with bpy.data.libraries.load(PATH) as (data_from, data_to):
                data_to.objects = data_from.objects
            for obj in data_to.objects:
                self.obj = obj
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break                  
        self.obj[self.geo_node_name] = True
        self.obj['PROMPT_ID'] = 'pc_layout_view.show_dimension_properties'
        self.obj['MENU_ID'] = 'HOME_BUILDER_MT_dimension_commands'
        self.obj["IS_2D_ANNOTATION"] = True
        if self.coll:
            self.coll.objects.link(self.obj)
        else:
            bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)
        self.obj.display.show_shadows = False
        self.obj.color = (0,0,0,1)

        self.set_input('Text Size',props.text_size)
        self.set_input('Arrow Height',props.arrow_height)
        self.set_input('Arrow Length',props.arrow_length)
        self.set_input('Line Thickness',props.line_thickness)
        self.set_input('Metric',True if scene.unit_settings.system == 'METRIC' else False)
        self.set_input('Material',mat)
        self.set_curve_to_vector(bpy.context)

    def set_curve_to_vector(self,context):
        self.obj.select_set(True)
        context.view_layer.objects.active = self.obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.mode_set(mode='OBJECT')

    def update(self):
        self.obj.hide_viewport = False
        p1 = self.obj.data.splines[0].bezier_points[0].co
        p2 = self.obj.data.splines[0].bezier_points[1].co   
        dist = pc_utils.calc_distance(p1,p2)        
        if dist == 0:
            self.obj.hide_viewport = True
        elif dist <= pc_unit.inch(7):
            self.set_input("Offset Text Amount",pc_unit.inch(3))
            self.set_input("Offset Text From Line",True)
        else:
            self.set_input("Offset Text From Line",False)

        text = str(round(pc_unit.meter_to_inch(math.fabs(dist)),3))
        inch_value, decimal_value = text.split(".")
        if decimal_value == "0":
            self.set_input("Decimals",0)
        else:
            self.set_input("Decimals",len(decimal_value))

    def set_dim_decimal(self):
        p1 = self.obj.data.splines[0].bezier_points[0].co
        p2 = self.obj.data.splines[0].bezier_points[1].co    

        dist = pc_utils.calc_distance(p1,p2) 

        text = str(round(pc_unit.meter_to_inch(math.fabs(dist)),3))
        inch_value, decimal_value = text.split(".")
        if decimal_value == "0":
            self.set_input("Decimals",0)
        else:
            self.set_input("Decimals",len(decimal_value))


class Dimension(Assembly):

    obj_text = None

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  
        if self.obj_bp:
            for child in obj_bp.children:
                if child.type == 'FONT':
                    self.obj_text = child     

    def flip_x(self):
        self.obj_text.scale.x = -1

    def flip_y(self):
        self.obj_text.scale.y = -1

    def create_dimension(self,layout_view=None):
        PATH = os.path.join(os.path.dirname(__file__),'assets',"Dimension_Arrow.blend")

        with bpy.data.libraries.load(PATH) as (data_from, data_to):
            data_to.objects = data_from.objects

        if layout_view:
            collection = layout_view.dimension_collection
        else:
            collection = bpy.context.view_layer.active_layer_collection.collection
        for obj in data_to.objects:
            if "obj_bp" in obj:
                self.obj_bp = obj          
                self.obj_bp['IS_DIMENSION'] = True  
            if "obj_x" in obj:
                self.obj_x = obj
            if "obj_y" in obj:
                self.obj_y = obj           
            if "obj_z" in obj:
                self.obj_z = obj
            if "obj_prompts" in obj:
                self.obj_prompts = obj    
            if obj.type == 'FONT':
                self.obj_text = obj   
            if obj.type in {'MESH','CURVE','FONT'}:
                pc_utils.assign_materials_to_object(obj)         
            obj["PROMPT_ID"] = "pc_assembly.show_dimension_properties"
            collection.objects.link(obj)

        self.get_prompt("Font Size").set_value(.07)
        self.get_prompt("Horizontal Line Location").set_value(.05)
        self.get_prompt("Line Thickness").set_value(.002)
        self.get_prompt("Arrow Height").set_value(.03)
        self.get_prompt("Arrow Length").set_value(.03)

    def update_dim_text(self):
        if bpy.context.scene.unit_settings.system == 'METRIC':
            if bpy.context.scene.unit_settings.length_unit == 'METERS':
                text = str(round(self.obj_x.location.x,2))
                self.obj_text.data.body = text + 'm'
            elif bpy.context.scene.unit_settings.length_unit == 'CENTIMETERS':
                text = str(round(pc_unit.meter_to_centimeter(self.obj_x.location.x),2))
                self.obj_text.data.body = text + 'cm'
            else:
                text = str(round(pc_unit.meter_to_millimeter(self.obj_x.location.x),2))
                self.obj_text.data.body = text + 'mm'
        else:
            if bpy.context.scene.unit_settings.length_unit == 'FEET':
                feet_decimal = round(pc_unit.meter_to_feet(self.obj_x.location.x),2)
                feet = int(feet_decimal)
                inches = round((feet_decimal - feet) * 12,2)
                text = str(round(pc_unit.meter_to_feet(self.obj_x.location.x),2))
                self.obj_text.data.body = str(feet) + "'" + " " + str(int(inches)) + '"'
            else:
                text = str(round(pc_unit.meter_to_inch(self.obj_x.location.x),2))
                self.obj_text.data.body = text + '"'
        bpy.context.view_layer.update()

        div_factor = 1
        if self.obj_bp.parent:
            div_factor = self.obj_bp.parent.scale.x

        text_width = self.get_prompt("Text Width")
        text_width.set_value((self.obj_text.dimensions.x/div_factor) + .05)
        for child in self.obj_bp.children:
            if child.type == 'EMPTY':
                child.empty_display_size = .00001
                # child.hide_viewport = True
        # if self.obj_y.location.y < 0:
        #     hll = self.get_prompt('Horizontal Line Location')
        #     hll.set_value(hll.get_value()*-1)

    def draw_ui(self,context,layout):
        font_size = self.get_prompt("Font Size")
        arrow_height = self.get_prompt("Arrow Height")
        arrow_length = self.get_prompt("Arrow Length")
        extend_first_line_amount = self.get_prompt("Extend First Line Amount")
        extend_second_line_amount = self.get_prompt("Extend Second Line Amount")
        line_thickness = self.get_prompt("Line Thickness")

        row = layout.row()
        row.label(text="Dimension Length:")
        row.prop(self.obj_x,'location',index=0,text="")

        row = layout.row()
        row.label(text="Leader Length:")
        row.prop(self.obj_y,'location',index=1,text="")   

        row = layout.row() 
        row.label(text="Arrow Size:")
        row.prop(arrow_height,'distance_value',text="Height")     
        row.prop(arrow_length,'distance_value',text="Length")      

        row = layout.row() 
        row.label(text="Extend Line:")
        row.prop(extend_first_line_amount,'distance_value',text="Line 1")     
        row.prop(extend_second_line_amount,'distance_value',text="Line 2")     

        row = layout.row()
        row.label(text="Line Thickness:")
        row.prop(line_thickness,'distance_value',text="")   

        row = layout.row()
        row.label(text="Font Size:")
        row.prop(font_size,'float_value',text="")  

        row = layout.row()
        row.label(text="Flip Text:")
        row.prop(self.obj_text.pyclone,'flip_x',text="X")            
        row.prop(self.obj_text.pyclone,'flip_y',text="Y")               