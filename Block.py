import json

from hashlib import sha256

class Block:

    # OBJECTIVE: To create components needed to make a block

    def __init__(self, index, data, timestamp, previous_block_hash, nonce=0):
        
        # Block's position and plain data
        self.index = index
        self.data = data

        # Block'stime of creation
        self.timestamp = timestamp

        # Save hashes
        self.previous_block_hash = previous_block_hash # <= Copied from previous block
        self.current_block_hash = None # <= Yet to be computed

        # Create pointers for network
        self.previous_block = None
        self.next_block = None

        self.nonce = nonce

    def compute_hash(self):

        # OBJECTIVE: Compute hash value of block's contents
        # NOTE: Function will return the same hash value, if given the same input. It doesn't matter how many times!
        
        # Create a dictionary in JSON format and sort keys
        json_string = json.dumps(self.__dict__, sort_keys=True)

        # print(json_string)

        # Return hash value of block's content
        return sha256(json_string.encode()).hexdigest()