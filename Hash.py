from hashlib import blake2b # <- Slightly faster than SHA-3 and just as secure

class Hash:

    # OBJECTIVE: To encrypt data before adding it to a block

    def __init__(self):
        pass

    def is_data_string(self, data):
        # OBJECTIVE: Check if data is type string

        if isinstance(data, str):
            return True
        
        return False

    def is_data_list(self, data):
        # OBJECTIVE: Check if data is type array
 
        if isinstance(data, list):
            return True

        return False

    def error_message(self, message):
        # OBJECTIVE: To print an error message

        raise Exception(message)

    def encode_string(self, incoming_str):
        # OBJECTIVE: To encode a string

        return bytes(incoming_str, 'UTF-8')

    def encrypt_data(self, incoming_data):
        # OBJECTIVE: Encrypt incoming data and return its hash value

        # If incoming_data is a String, then it needs to be encoded to be able to convert to bytes
        if self.is_data_string(incoming_data):
            
            try:
                # Attempt to encode string in UTF-8
                b_data = self.encode_string(incoming_data)

            except TypeError as err:
                # Print error message
                self.error_message(err)

        else:
            # Convert incoming_data to bytes
            b_data = bytes(incoming_data)

        # Encrypt data with blake2b()
        blake_encrypt = blake2b()
        blake_encrypt.update(b_data)

        # Return hexa-decimal of encryption
        return blake_encrypt.hexdigest()


    def encrypt_list(self, incoming_list):
        # OBJECTIVE: To encrypt a list and return its hash value
        
        # Create instance of blake2b() for further use
        blake_encrypt = blake2b()

        # Specify encoding if it's a string list
        if self.is_data_string(incoming_list[0]):
            
            for i in incoming_list:
                # Encode string, then encrypt it
                blake_encrypt.update(self.encode_string(i))

        else:
            
            for i in incoming_list:
                # Change all elements inside array to bytes
                blake_encrypt.update(bytes(i))

        # Return hexadecimal digest
        return blake_encrypt.hexdigest()