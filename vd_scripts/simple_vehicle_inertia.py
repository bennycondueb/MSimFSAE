def calculate_box_inertia(mass, length_x, width_y, height_z):
    """Inertia for a box of given mass, length, width, height. E.g. Vehicle Chassis"""
    ixx = (1.0 / 12.0) * mass * (width_y**2 + height_z**2)
    iyy = (1.0 / 12.0) * mass * (length_x**2 + height_z**2)
    izz = (1.0 / 12.0) * mass * (length_x**2 + width_y**2)
    
    
    print(f"Mass: {mass} kg | Dimensions (x,y,z): {length_x}, {width_y}, {height_z} m")
    print(f'<inertia ixx="{ixx:.5f}" ixy="0.0" ixz="0.0" iyy="{iyy:.5f}" iyz="0.0" izz="{izz:.5f}" />')
    return ixx, iyy, izz

def calculate_wheel_inertia(mass, radius, width):
    """Inertia for a cylinder of given mass, radius, width. E.g. Wheels"""
    ixx = (1.0 / 12.0) * mass * (3 * radius**2 + width**2)
    iyy = (1.0 / 2.0) * mass * (radius**2)
    izz = (1.0 / 12.0) * mass * (3 * radius**2 + width**2) # Uguale a ixx per simmetria
    
    
    print(f"Mass: {mass} kg | Radius: {radius} m | Width: {width} m")
    print(f'<inertia ixx="{ixx:.5f}" ixy="0.0" ixz="0.0" iyy="{iyy:.5f}" iyz="0.0" izz="{izz:.5f}" />')
    return ixx, iyy, izz

if __name__ == "__main__":
    # Chassis Data
    CHASSIS_MASS = 190.0  # kg
    CHASSIS_X = 2.942       # m
    CHASSIS_Y = 1.575     # m
    CHASSIS_Z = 1.119      # m
    
    # Wheel Data
    WHEEL_MASS = 10.0     # kg 
    WHEEL_RADIUS = 0.23    # m
    WHEEL_WIDTH = 0.23     # m
    
    # Hinge Data
    # Assuming a hinge is a small cube
    HINGE_MASS = 2.0      # kg
    HINGE_SIZE = 0.1      # m 

    print("\n--- CHASSIS INERTIA ---")
    calculate_box_inertia(CHASSIS_MASS, CHASSIS_X, CHASSIS_Y, CHASSIS_Z)
    print("\n--- WHEEL INERTIA ---")
    calculate_wheel_inertia(WHEEL_MASS, WHEEL_RADIUS, WHEEL_WIDTH)
    print("\n--- HINGE INERTIA ---")
    calculate_box_inertia(HINGE_MASS, HINGE_SIZE, HINGE_SIZE, HINGE_SIZE)
    print("\n")