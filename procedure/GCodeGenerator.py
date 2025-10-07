from config import GRBLConfig

def multi_dimensional_coordinates_from_axes(axes: GRBLConfig.Axes, command="G0"):
    """create a set of gcode instructions from multiples Axes
    to move around a multi dimensional figure
    currently only supports 1-2 axis"""
    gcode_commands = []
    relevant_axes= get_relevant_axes(axes) #get the axes that have changes in position
    number_relevant_axes = len(relevant_axes) #quantity of axes that need to be moved

    #Only one axis needs to be moved
    if (number_relevant_axes == 1):
        positions = generate_position_instructions(relevant_axes[0])
        for position in positions:
            gcode_commands.append(create_command(command, position))

    #Two axis need to be moved
    elif (number_relevant_axes == 2):
        axis_1 = relevant_axes[0]
        axis_2 = relevant_axes[1]
        #Get the two axis that need to be moved's positional changes
        primary_axis_positions = generate_position_instructions(relevant_axes[0])
        secondary_axis_positions = generate_position_instructions(relevant_axes[1])

        #Loops through and creates point sets (X,Y)
        #EX X0-X1, Y0-Y2, (example assumes resolution 1)
        
        #G0 X0 Y0 -> (0,0)
        #G0 Y1    -> (0,1)
        #G0 Y2    -> (0,2)
        #G0 X1 Y0 -> (1,0)
        #G0 Y1    -> (1,1)
        #G0 Y2    -> (1,2)
        
        #Handles the change in the first position ie point a to b: (Xa...Xb, Y0)
        for primary_position in primary_axis_positions: #Gets next Primary Position IE (X0, X1... X10): Xa
            start_position = f"{primary_position} {secondary_axis_positions[0]}" #Creates a start position: Xa Y0
            start_command = create_command(command, start_position) #prepends the movement command: G0 Xa Y0
            gcode_commands.append(start_command) #Adds to command list
            
            #Handles looping through all the changes in the secondary axis (X, Ya...Yb)
            #Assumes that prior step of for loop has relevant X position already, only adds a Y change
            for secondary_position in secondary_axis_positions[1:]: #Gets next secondary Position (Y0...Y10): Ya
                secondary_command = create_command(command, secondary_position) #Prepends movement command (assumes X position has already moved): G0 Ya
                gcode_commands.append(secondary_command) #adds to command list
        
                
    return gcode_commands

def single_dimensional_sweeps_from_axes(axes: GRBLConfig.Axes, command="G0"):
    """Sweeps through each given axes range
    Keeps all other axes at their start position for the sweep"""
    gcode_commands = []
    axes_positions = []
    relevant_axes = get_relevant_axes(axes)  # Get the axes that have changes in position

    # Generate position instructions for each relevant axis
    for axis in relevant_axes:
        axes_positions.append(generate_position_instructions(axis))

    # Generate G-code commands for each axis
    for i, current_axis_positions in enumerate(axes_positions):
        # First command string includes the first position of the current axis and first positions of other axes
        first_positions = []
        for j, other_axis_positions in enumerate(axes_positions):
            if i == j:  # Current axis
                first_positions.append(current_axis_positions[0])
            else:  # Use the first position of other axes
                first_positions.append(other_axis_positions[0])
        gcode_commands.append(create_command(command, " ".join(first_positions)))

        # Subsequent commands for the current axis
        for position in current_axis_positions[1:]:
            gcode_commands.append(create_command(command, position))

    return gcode_commands
        

#Helper Functions
def get_relevant_axes(axes: GRBLConfig.Axes):
    '''from a list of GRBLConfig Axes get the ones that have different start and stop values'''
    relevant_axes = []

    for axis in axes :
        print("------")
        print(axis)
        print("------")
        if axis.start != axis.stop: # axis has some degree of positional change associated with it
            relevant_axes.append(axis)
            # print()
            # print("found relevant axis")
            # print()
            # print(axis)

    return relevant_axes

def generate_position_instructions(axis: GRBLConfig.Axis_Components, command="G0"):
    position_instructions = []
    
    axis_name = axis.gCodeName  # get name of GCode [X, Y, Z, A, B, C]
    resolution = axis.resolution  # Size of a step
    
    # Calculate step size: Step size is inversely proportional to resolution
    if (resolution == 0):
        resolution = 1  # Avoid zero resolution, which would lead to division by zero.
        step_size = 1
    
    elif (resolution > 0):
        step_size = 1 / abs(resolution)
    
    elif (resolution < 0):
        step_size = abs(resolution)
    
    start = axis.start  # Starting position
    stop = axis.stop  # Ending Position
    position = start  # set the start position for internal iteration

    # if start > stop :
    #     step_size = (start - stop)/resolution
    
    # else :
    #     step_size = (stop-start)/resolution
    
    # Adjust step direction
    step_direction = step_size if start < stop else -step_size
    
    # Loop through positions from start to stop, incrementing by the step size
    while (step_direction > 0 and position <= stop) or (step_direction < 0 and position >= stop):
        # Generate the G-code command for the current position
        position_instructions.append(f"{axis_name}{position:.3f}")
        
        # Move to the next position
        position += step_direction
    
    return position_instructions

def create_command(command, instruction):
    return(f"{command} {instruction}\n")