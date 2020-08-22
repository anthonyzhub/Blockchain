import struct
import os
import subprocess
import zipfile

class CustomObject:
    
    # OBJECTIVE: Import files from host computer and put it in the blockchain
    
    def __init__(self):
        
        # Hold file's path
        self.file_path = os.environ['PWD']

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

    def import_text_file(self):
        
        # OBJECTIVE: Locate text file before importing to Python program
        
        # Ask for directory
        file_directory = input("Enter file's directory: ")

        # Search and replace text
        # os.environ lets me to use shell variables on the host computer
        if file_directory == "~":
            file_directory = os.environ['HOME']
        elif file_directory == ".":
            file_directory = os.environ['PWD']

        # Only print files inside directory
        for pos, f in enumerate(os.listdir(file_directory)):
            
            if not os.path.isdir(file_directory + "/" + f):
                print("{} - {}".format(pos, f))

        # Ask for filename
        file_name = input("Enter filename: ")

        # Check if file exists
        if not os.path.exists(file_directory + "/" + file_name):

            print("Invalid directory!")
            return None

        # Save file's path
        self.file_path = file_directory + "/" + file_name

        print("Compression is starting")

        # Compress file
        zf = zipfile.ZipFile("{}.zip".format(file_name), mode='w') # <- Create zip's filename
        zf.write(self.file_path, compress_type=zipfile.ZIP_STORED) # <- Enter file to compress
        zf.close() # <- Close the zip file

        print("Compression is done")

        # Open file in read binary mode
        with open("{}.zip".format(file_name), "rb") as f:

            f_message = f.readlines() # <- Read message and return list
            f_message = b' '.join(word for word in f_message) # <- Turn list to string
            
            return f_message