from Block import Block
from collections import deque

import numpy as np
import pandas as pd
import zipfile
import os
import time

class Blockchain:

    # Declare static variable for add_block()
    # A static variable's value will always be remembered until program is terminated
    previous_hash_static = "0"

    # Difficulty of PoW algorithm
    difficulty = 2

    def __init__(self):
        
        # Create a head and tail node
        self.head = None
        self.tail = None

        # Set linked list size to 0
        self.list_size = 0

        # Create a queue of unconfirmed transactions
        self.unconfirmed_transactions = deque()

        # Create a data frame
        self.data_frame = pd.DataFrame()

    def is_empty(self):

        # OBJECTIVE: Check if list is empty
        return self.list_size == 0

    def proof_of_work(self, block):

        # OBJECTIVE: Before officially adding a block, increment block's nonce value until a proper hash value is computed

        """
        NOTE: A nonce is created to see how many times it will take for the computer to create a valid hash.
                A hash is valid, if it has a leading number of 0s. In this case, the number of zeros depends
                on the level of difficulty. Hence, the variable "difficulty" that is declared at the beginning
                of this class. 

                This approach is brute force because we are starting at 0. The variable will increment until
                a proper hash is calculated. So, nonce could eventually be 1_000_000_000!
        """

        # Start nonce value as 0
        block.nonce = 0

        # Compute block's hash
        hash = block.compute_hash()

        # Continue to compute a new hash until it starts with a N number of 0s.
        # Ex. 00xxxxx
        while not hash.startswith("0" * self.difficulty):

            # Increment block's nonce value and compute new hash
            block.nonce += 1
            hash = block.compute_hash()

        return hash

    def is_hash_valid(self, new_block, proposed_hash):

        # OBJECTIVE: Check if hash value meets the requirements AND hash value matches with a newly created hash value
        #
        #   1. Does proposed_hash start with N number of 0s?
        #   2. If hash is recomputed, would it return the same string?
        return (proposed_hash.startswith("0" * self.difficulty) and proposed_hash == new_block.compute_hash())

    def validate_entry(self, new_block):

        # OBJECTIVE: Verify block can be added to link list by:
        #
        #   1. Does new_block have the correct previous_block_hash?
        #   2. Does new_block's hash meet the requirements

        # Get hash from last block
        old_hash = self.tail.current_block_hash

        # Stop if hash values don't match
        if new_block.previous_block_hash != old_hash:
            return False

        """
        NOTE: IBM article is confusing. 
            create_hash() will create an infinite amount of potential hash values before assigning it to the block. Why? Because the hash needs to start with N number
            of 0s due to level of difficulty. compute_hash() only computes the hash value once. So, how is it fair to get matching hash values between a single-use
            function and a multi-use function? This is why I commented the if-statement.
        """
        # Stop if block's hash value isn't valid
        # if not self.is_hash_valid(new_block, proposed_hash):
            # return False

        # If hash value is valid, then add it to the new block
        # new_block.current_block_hash = proposed_hash

        return True

    def create_head(self, head_block):

        # OBJECTIVE: Create a head block with previous_hash as 0

        print("Creating a head block")

        # Add it to link list
        self.head = head_block
        self.tail = head_block

        # Update previous_hash_static variable
        self.previous_hash_static = head_block.current_block_hash

        # Increment counter for list size
        self.list_size += 1

    def add_block(self, new_block):

        # OBJECTIVE: Add a block to link list

        # If list is empty, go to a dedicated function to create a head block
        if self.is_empty():

            self.create_head(new_block)
            return None

        print("Creating a new block")

        # Get last block to update pointers
        old_block = self.tail

        old_block.next_block = new_block

        new_block.previous_block = old_block
        new_block.next_block = None

        # Update tail
        self.tail = new_block

        # Update old hash value
        self.previous_hash_static = new_block.current_block_hash

        # Update list's length
        self.list_size += 1

    def submit_new_transaction(self, data):

        # OBJECTIVE: Add data to a list of unconfirmed transactions
        self.unconfirmed_transactions.append(data)

    def request_to_mine(self):

        # OBJECTIVE: Check if transactions needs to be confirmed. If so, then starting mining

        # Check if unconfirmed_transactions is empty
        if not self.unconfirmed_transactions:
            return False

        # Pop data from list
        data = self.unconfirmed_transactions.popleft()

        # Create a new block and compute a hash value
        new_block = Block(self.list_size, data, time.time(), self.previous_hash_static)
        new_block.current_block_hash = self.proof_of_work(new_block)

        # If link list is empty, there's nothing to verify, so add new_block
        if not self.list_size:
            self.add_block(new_block)

        # Validate new block
        elif self.validate_entry(new_block):

            # Add block to link list
            self.add_block(new_block)

        else:
            
            # Print error message and add data back to queue
            print("ERROR: Unable to add block!")
            self.unconfirmed_transactions.append(data)

            return False

        return True

    def verify_chain(self):

        # OBJECTIVE: Verify blockchain has not been tampered with

        # Exit if link list only has <=1 block
        if self.is_empty() or self.list_size == 1:
            print("There's only <=1 blocks in the link list")
            return True

        # Get starting blocks
        tmp_block_a = self.head
        tmp_block_b = tmp_block_a.next_block

        counter = 0

        # Iterate link list
        while tmp_block_b is not None:

            # Compare hash values
            if tmp_block_b.previous_block_hash != tmp_block_a.current_block_hash:
                print("ERROR: Block #{} has a different hash value than Block #{}!".format(counter, counter - 1))
                return False

            # Update temporary blocks
            tmp_block_a = tmp_block_b
            tmp_block_b = tmp_block_b.next_block

            # Increment counter
            counter += 1

        return True

    def print_list(self):

        # OBJECTIVE: Print blockchain

        # Exit if link list is empty
        if self.is_empty():
            
            print("List is empty!")
            return None

        # Get head block
        old_block = self.head

        # Iterate link list
        while old_block is not None:

            print("Block:")
            print("\tIndex => {}".format(old_block.__dict__["index"]))
            print("\tData => {}".format(old_block.__dict__["data"]))
            print("\tHash => {}\n".format(old_block.__dict__["current_block_hash"]))

            # Move to next block
            old_block = old_block.next_block

    def download_blockchain_data(self):

        # OBJECTIVE: Write blockchain data to CSV file

        # Check if list is empty
        if self.is_empty() is True:

            print("List is empty!")
            return None

        # Get genesis block
        old_block = self.head
        dict_block = dict()
        block_num = 0

        while old_block is not None:

            # Write block's data to dictionary
            dict_block["Previous Block's Hash"] = old_block.previous_block_hash
            dict_block["Current Block's Hash"] = old_block.current_block_hash

            dict_block["Current Block's Data"] = old_block.current_block_data

            # Save dictionary to data frame
            self.data_frame = self.data_frame.append(dict_block, ignore_index=True)

            # Rename index names to Block <block_num>
            """
            1. Rename index with lambda function (nameless function)
            2. Parameter for lambda function is block_num, the variable I created as a counter
            3. The function will return a string "Block #" with # as the value of block_num
            """
            self.data_frame = self.data_frame.rename(index=lambda block_num: "Block {}".format(block_num))
            block_num+=1

            # Move to next block
            old_block = old_block.next_block_pointer

        # Write dataframe to CSV file
        csv_file_name = "Zamora-Blockchain_Data.csv"
        self.data_frame.to_csv(csv_file_name)

        # Compress CSV file
        zip_file = zipfile.ZipFile("Zamora-Blockchain.zip", mode='w') # <- Create a zip file archive for writing
        zip_file.write(csv_file_name, compress_type=zipfile.ZIP_STORED) # <- Write csv file to zip_file for compression
        zip_file.close() # <- Close file after writing to it

        # Delete uncompressed file
        os.remove(csv_file_name)
