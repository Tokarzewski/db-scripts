# convert idf file geometry from relative to world coordinate system 

from eppy.modeleditor import IDF

iddfile = "C:\\Users\\thinkpad\\Desktop\\GeometryConventionConverter\\Energy+.idd"
IDF.setiddname(iddfile)

# idf = "C:\\Users\\thinkpad\\Desktop\\GeometryConventionConverter\\detailed_geo_relative.idf"
idf = "C:\\Users\\thinkpad\\Desktop\\GeometryConventionConverter\\simple_geo_relative.idf"
idf = IDF(idf)

"""
TO DO improvement
Create dictionary. Zones have surfaces, surfaces have windows.
Loop through objects from dictionary once by looking at parent objects.
"""

def get_simple_surfaces():
    simple_surfaces = []
    simple_surface_types = [
        "Wall:Exterior",
        "Wall:Adiabatic",
        "Wall:Underground",
        "Wall:Interzone", #I
        "Roof",
        "Ceiling:Adiabatic",
        "Ceiling:Interzone", #I
        "Floor:GroundContact",
        "Floor:Adiabatic",
        "Floor:Interzone", #I
    ]
    for type in simple_surface_types:
        simple_surfaces += idf.idfobjects[type]

    return simple_surfaces

def update_simple_object_coordinates(zone, object):
    object.Starting_X_Coordinate += zone.X_Origin
    object.Starting_Y_Coordinate += zone.Y_Origin
    object.Starting_Z_Coordinate += zone.Z_Origin

def update_detailed_object_coordinates(zone, object):
    x_origin, y_origin, z_origin = zone.X_Origin, zone.Y_Origin, zone.Z_Origin
    number_of_vertices = int(object.Number_of_Vertices)

    for number in range(1, number_of_vertices + 1):
        x_coord_value = getattr(object, f"Vertex_{number}_Xcoordinate")
        y_coord_value = getattr(object, f"Vertex_{number}_Ycoordinate")
        z_coord_value = getattr(object, f"Vertex_{number}_Zcoordinate")
        setattr(object, f"Vertex_{number}_Xcoordinate", x_coord_value + x_origin)
        setattr(object, f"Vertex_{number}_Ycoordinate", y_coord_value + y_origin)
        setattr(object, f"Vertex_{number}_Zcoordinate", z_coord_value + z_origin)

def update_simple_geometry():
    for zone in list_of_zones:
        temp_zone_name = zone.Name
        for surface in simple_surfaces:
            if surface.Zone_Name == temp_zone_name:
                update_simple_object_coordinates(zone, surface)
                
                if "Interzone" in surface.key:
                    if surface.Outside_Boundary_Condition_Object in list_of_zone_names:
                        new_surface = idf.copyidfobject(surface)
                        new_surface.Name = surface.Name + "-Copy"
                        new_surface.Zone_Name = surface.Outside_Boundary_Condition_Object
                        new_surface.Outside_Boundary_Condition_Object = surface.Name
                        surface.Outside_Boundary_Condition_Object = new_surface.Name

def update_detailed_geometry():
    for zone in list_of_zones:
        temp_zone_name = zone.Name
        for surface in detailed_surfaces:
            if surface.Zone_Name == temp_zone_name:
                update_detailed_object_coordinates(zone, surface)

                temp_surface_name = surface.Name
                for opening in detailed_openings:
                    if opening.Building_Surface_Name == temp_surface_name:
                        update_detailed_object_coordinates(zone, opening)

global_geometry_rules = idf.idfobjects["GlobalGeometryRules"][0]
list_of_zones = idf.idfobjects["Zone"]
list_of_zone_names = [zone.Name for zone in list_of_zones]

simple_coordinate_system = global_geometry_rules.Rectangular_Surface_Coordinate_System
if simple_coordinate_system == "Relative":
    simple_surfaces = get_simple_surfaces()
    update_simple_geometry()
    global_geometry_rules.Rectangular_Surface_Coordinate_System = "World"

detailed_coordinate_system = global_geometry_rules.Coordinate_System
if detailed_coordinate_system == "Relative":
    detailed_surfaces = idf.idfobjects["BuildingSurface:Detailed"]
    detailed_openings = idf.idfobjects["FenestrationSurface:Detailed"]
    update_detailed_geometry()
    global_geometry_rules.Coordinate_System = "World"

for zone in list_of_zones:
    zone.X_Origin, zone.Y_Origin, zone.Z_Origin = 0, 0, 0

idf.saveas("converted.idf")
