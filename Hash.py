from hashlib import blake2b # <- Slightly faster than SHA-3 and just as secure

class Hash:

    # OBJECTIVE: To encrypt data before adding it to a block

    def __init__(self):
        
        # Initialize blake2b()
        self.blake_encrypt = blake2b()

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

    def is_prev_block_hashes_none(self, data):
        # OBJECTIVE: Check if data is None

        if data is None:
            return True

        return False

    def error_message(self, message):
        # OBJECTIVE: To print an error message

        raise Exception(message)

    def encode_string(self, incoming_str):
        # OBJECTIVE: To encode a string

        return bytes(incoming_str, 'UTF-8')

    def encode_prev_block_hashes(self, prev_block_hashes):
        # OBJECTIVE: To encrypt string of prev_block_hashes before being encrypted again with new data

        if self.is_prev_block_hashes_none(prev_block_hashes):

            # This condition should be executed only for genesis_block
            # so, return False to skip encryption of prev_block_hashes
            return False

        else:

            # Return prev_block_hashes as bytes
            return self.encode_string(prev_block_hashes)

    def encrypt_individual_data(self, incoming_data):
        # OBJECTIVE: Encrypt incoming data and return its hash value

        # If incoming_data is a String, then it needs to be encoded to be able to convert to bytes
        if self.is_data_string(incoming_data):
            
            try:
                # Attempt to encode string in UTF-8
                new_bytes_data = self.encode_string(incoming_data)

            except TypeError as err:
                # Print error message
                self.error_message(err)

        else:

            # Convert incoming_data to bytes
            new_bytes_data = bytes(incoming_data)

        # Encrypt data with blake2b()
        self.blake_encrypt.update(new_bytes_data)

        # Return hexa-decimal of encryption
        return self.blake_encrypt.hexdigest()


    def encrypt_pair_data(self, incoming_list):
        # OBJECTIVE: To encrypt a list and return its hash value

        # Specify encoding if it's a string list
        if self.is_data_string(incoming_list[0]):
            
            for i in incoming_list:
                # Encode string, then encrypt it
                self.blake_encrypt.update(self.encode_string(i))

        else:
            
            for i in incoming_list:
                # Change all elements inside array to bytes
                self.blake_encrypt.update(bytes(i))

        # Return hexadecimal digest
        return self.blake_encrypt.hexdigest()

    def encrypt_data(self, incoming_data):
        # OBJECTIVE: To decide if incoming_data is either an individual (single variable) or a pair data type (list)

        # Encrypt lists, tuples, or dicts
        if isinstance(incoming_data, list) or isinstance(incoming_data, tuple) or isinstance(incoming_data, dict):
            return self.encrypt_pair_data(incoming_data)

        else:
            return self.encrypt_individual_data(incoming_data)