from interface.GRBLController import GRBL
from interface.PNAController import PNA
from procedure.ScanData import ScanData
from config.PNAConfig import PNAConfig

import time

def run(instruction_set, GRBL: GRBL, PNA: PNA, scan_data: ScanData, pnaConfig: PNAConfig):
    
    #Configure PNA
    PNA.configure_analyzer(pnaConfig)
    
    for instruction in instruction_set:
        instruction_type = instruction.split()[0] #Get the kind of instructions
        PNA.fetch_data()
        
        if instruction_type == "G0":
            GRBL.send_instruction(instruction)
            status = GRBL.get_status()
            while status == "Run":
                status = GRBL.get_status()
                time.sleep(0.05)
        
        elif instruction_type == "SCAN":
            data = PNA.fetch_data()
            grbl_response = GRBL.get_response()
            scan_data.parse_position_from_response(grbl_response)
            scan_data.update_dataframe(data, grbl_response)
            scan_data.save_dataframe()
        
        elif instruction_type == "DONE":
            pass


#Might deprecate
def compile_gcode_with_scan(gcode_commands):
    scan_call = "SCAN"
    finish_code = "DONE"
    instructions = []
    
    if len(gcode_commands) == 0:
        instructions.append(scan_call)
    
    else :
        #Loop through each Gcode position, add a scan call after
        for gcode in gcode_commands:
            instructions.append(gcode)
            instructions.append(scan_call)
    
        #Once all Gcode positions are complete, reset position with initial gcode position
        instructions.append(gcode_commands[0])
    
    #Append the finish code
    instructions.append(finish_code)

    return instructions