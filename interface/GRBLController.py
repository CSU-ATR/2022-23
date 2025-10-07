import serial
import serial.tools.list_ports
import time

from misc.Logger import Logger

class GRBL:
    """A class to connect to an Arduino with custom GRBL MEGA-5x software"""
    
    def __init__(self, debug=False, ui_output=True):
        self.debug = debug
        self.ui_output = ui_output
        self.vid = 0x2A03
        self.pid = 0x0042
        self.baud_rate = 115200
        self.port = None
        self.connection = None
        self.source = "Arduino"
    
    def output_message(self, message, level="info"):
        """Output Messages to cmdline and UI Terminal"""
        if(self.debug):
            Logger.console(message, source=self.source, level=level) 
                       
        if(self.ui_output):
            Logger.ui(message, source=self.source, level=level)
        
    def find_port(self):
        """Find a port with an Arduino Mega connected"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == self.vid and port.pid == self.pid:
                self.port = port.device
        
        if (self.port):
            self.output_message(f"Port found on: {self.port}")
            
        else:
            self.output_message("No Port found", level="error")
            
            
    def setup_connection(self):
        """Establish connection to the GRBL Arduino device."""
        try:
            grbl = serial.Serial(self.port, self.baud_rate)
            self.connection = grbl
            self.output_message(f"Connected")
            
        except serial.SerialException as e:
            self.output_message(f"Unable to connect: {e}", level="error")
            self.connection = None
            
    def close_connection(self):
        """Close connection the the Arduino"""
        if self.connection:
            self.connection.close()
            print("GRBL connection closed")
    
    def update_settings(self, settings):
        """Send custom settings to GRBL"""
        self.output_message(f"Updating GRBL Settings")
        for setting in settings :
            self.send_instruction(setting)
    
    def wake_GRBL(self):
        """Wake up GRBL so it is ready to recieve commands"""
        self.output_message(f"Waking GRBL")
        self.connection.write(b"\r\n\r\n")
        time.sleep(1)
        self.connection.flushInput()
        
    #Needs to output whats happening to terminal
    def send_instruction(self, instruction, print_instruction=False):
        """Send a single instruction to GRBL"""
        if self.connection:
            waiting = True
            response = ""
            self.connection.write(instruction.encode())
            self.connection.flush()
            time.sleep(0.05) #Test Removing this
            
            while waiting :
                if self.connection.in_waiting > 0:
                    response += self.connection.readline().decode()
                else :
                    break
            if(print_instruction):
                self.output_message(f"Sent: '{instruction.strip()}'\nRecieved:\n{response}")
            
            status = self.parse_response_for_status(response)
            return response, status

    def get_status(self):
        """Get the status of GRBL"""
        _, status = self.send_instruction('?')
        return status

    def get_response(self):
        """Get the full response of GRBL's state"""
        response, _ = self.send_instruction('?')
        return response

    def parse_response_for_status(self, response):
        """parse GRBLS response to get its status code"""
        status = ""
        if "Idle" in response:
            status = "Idle"
        elif "ALARM" in response:
            status = "Alarm"
        elif "HOLD" in response:
            status = "Hold"
        elif "FAULT" in response:
            status = "Fault"
        elif "Run" in response:
            status = "Run"

        return status
    
    def initialize(self):
        """Initialize, connection to Arduino, and GRBL software to recieve instructions"""
        self.find_port() #Find Port
        
        if self.port: 
            self.setup_connection() #Connect to grbl
            
        if self.connection :
            #settings = (get settings)
            # self.updateSettings(settings) #
            self.wake_GRBL() #Wake up GRBL
            self.send_instruction("?\n") #clear output buffer
            self.output_message("GRBL is ready")

        
    
    