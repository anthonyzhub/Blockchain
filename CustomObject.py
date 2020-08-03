import struct
import os
import subprocess

class CustomObject:
    
    # OBJECTIVE: Created an empty class that represents a struct object similar in C++
    
    def __init__(self):
        pass

    def string_to_struct(self, new_string):
        # OBJECTIVE: Convert string to bytes

        # Check if parameter is string
        if not isinstance(new_string, str):
            
            print("{} is {}".format(new_string, type(new_string)))
            return None

        # Convert everything to bytes
        # For packing, the function needs to know the length of the variable to be packed and the data itself
        return struct.pack('{}s'.format(len(new_string)), bytes(new_string, 'UTF-8'))

    def int_to_struct(self, new_int):
        # OBJECTIVE: Convert int to bytes

        # Check if parameter is int
        if not isinstance(new_int, int):
            
            print("{} is {}".format(new_int, type(new_int)))
            return None

        # Convert string to bytes
        return struct.pack('i', new_int)

    def float_to_struct(self, new_float):
        # OBJECTIVE: Convert float to bytes

        # Check if parameter is int
        if not isinstance(new_float, float):
            
            print("{} is {}".format(new_float, type(new_float)))
            return None

        # Convert string to bytes
        return struct.pack('f', new_float)

    def import_textfile(self):
        # OBJECTIVE: To add a text file to the blockchain
        
        # Execute shell script and accept script's output as input
        # FYI: subprocess will return data as bytes
        output = subprocess.run(["bash", "FindFile.sh"], stdout=subprocess.PIPE)

        # Return output as decoded string
        return output.stdout.decode('UTF-8')
        