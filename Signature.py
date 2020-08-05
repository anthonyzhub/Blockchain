from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

# Documentation: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

class Signature:

    # OBJECTIVE: To digital sign a block's data as proof of verification

    def __init__(self):
        
        self.private_key = None
        self.public_key = None
        self.user_name = self.user_name = os.environ['USER'] # <- Cannot find 'WHOAMI'
        self.ENC_ALGO_TYPE = hashes.SHA256()
        self.PRIVATE_FILE_NAME = "{}-Private_Key.pem".format(self.user_name)
        self.PUBLIC_FILE_NAME = "{}-Public_Key.pem".format(self.user_name)

    def generate_keys(self):

        # OBJECTIVE: To generate a public-private key using RSA

        """
        1. public_exponent - The public exponent of the new key. Default is 65537.
        2. key_size - How big the key is in bits.
        3. backend - Generates a new RSA private from default_backend(). This implements RSABackend.
        """
        # Generate a pair of keys
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

        # From the private key derived the public key
        self.public_key = self.private_key.public_key()

    def get_keys(self):

        # OBJECTIVE: Collect user's keys if they were already created

        # NOTE: If keys were created, check project's working directory

        # Create boolean variable for further use
        does_private_key_exist = False
        does_public_key_exist = False
        
        # Open private key PEM file
        with open(self.PRIVATE_FILE_NAME, "rb") as private_file:

            # Save private_file's content to private_key
            self.private_key = serialization.load_pem_private_key(
                private_file.read(),
                password=None, # <- Password wasn't given upon creation
                backend=default_backend()
            )

            # Set boolean to True
            does_private_key_exist = True

        # Open public key PEM file
        with open(self.PUBLIC_FILE_NAME, "rb") as public_file:

            # Save public_file's content to public_key
            self.public_key = serialization.load_pem_public_key(
                public_file.read(),
                backend=default_backend()
            )

            # Set boolean to True
            does_public_key_exist = True

        # Return true if both conditions are true
        if does_private_key_exist == True and does_public_key_exist == True:

            return True

        else:
            
            return False

    def write_keys(self):

        # OBJECTIVE: To write the keys in a PEM file

        # Create a PEM file for the private key. The command below will serialize it.
        private_pem_file = self.private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())

        # Write the file in binary format to the file
        with open(self.PRIVATE_FILE_NAME, "wb") as private_file:

            # Write private key to file
            private_file.write(private_pem_file)

        # Create a file for the public key. The command below will serialize it
        public_pem_file = self.public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        
        # Write the file in binary format to the file
        with open(self.PUBLIC_FILE_NAME, "wb") as public_file:

            # Write public key to file
            public_file.write(public_pem_file)

    def create_signature(self, block_data):

        # OBJECTIVE: To sign binary data with user's private key

        """
        A signature requires a specific hash function and padding to use
        PSS is recommended for protocols or applications. 
        PKCS1v15 supports legacy protocols
        """

        # Digitally sign a block's data
        signature = self.private_key.sign(
            block_data,
            padding.PSS(
                mgf=padding.MGF1(self.ENC_ALGO_TYPE),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            self.ENC_ALGO_TYPE
        )

        # Return signature
        return signature

    def verify_signature(self, signature, block_data):

        # OBJECTIVE: To verify user's signature on their uploaded data

        is_signature_valid = False

        # Attempt to verify signature on block's data
        try:

            # Verify signature by decrypting signed data with signature
            self.public_key.verify(
                signature,
                block_data,
                padding.PSS(
                    mgf=padding.MGF1(self.ENC_ALGO_TYPE),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                self.ENC_ALGO_TYPE
            )

            # Change verification status
            is_signature_valid = True

        except:

            print("*** Invalid signature! ***")

        # Return status
        return is_signature_valid

    def encrypt_data(self, unencrypted_data):

        # OBJECTIVE: To encrypt data before adding it to blockchain

        """
        Valid paddings for encryption are OAEP and PKCS1v15.
        OAEP is recommended for protocols or applications.
        PKCS1v15 should be used to support legacy protocols.
        """
        # Encrypt data with user's public key using SHA256
        cipher = self.public_key.encrypt(
            unencrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=self.ENC_ALGO_TYPE),
                algorithm=self.ENC_ALGO_TYPE,
                label=None
            )
        )

        # Return cipher text
        return cipher

    def decrypt_data(self, cipher):

        # OBJECTIVE: To decrypt data from a block if user has correct private key

        # Decrypt cipher
        plain = self.private_key.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=self.ENC_ALGO_TYPE),
                algorithm=self.ENC_ALGO_TYPE,
                label=None
            )
        )

        # Return decrypted data
        return plain
