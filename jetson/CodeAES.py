import numpy as np
from Crypto import Random
from Crypto.Cipher import AES


class Encryptor():

    def __init__(self, key=None):
        if key is None:
            self.key = Random.new().read(AES.block_size)  # Creates key

    def encrypt(self, coordinates, image):
        IV = Random.new().read(AES.block_size)  # Initialization vector
        mode = AES.MODE_CFB  # Sets encryption mode to CFB mode; CFB is great in avoiding the hassle of padding
        encryptor = AES.new(self.key, mode, IV)  # Encryptor

        ROI_number = 0
        for c in coordinates:
            x1, y1, x2, y2 = c
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            ROI = image[y1:y2, x1:x2]
            img_bytes = np.ascontiguousarray(ROI, dtype=None)

            encData = encryptor.encrypt(img_bytes)  # Encrypted data
            data = np.frombuffer(encData, dtype=np.uint8)
            data = np.reshape(data, (y2 - y1, x2 - x1, 3))
            image[y1:y2, x1:x2] = data
        return image, IV

    def decrypt(self, coordinates, image, IV):
        # IV = Random.new().read(AES.block_size) #Initialization vector
        mode = AES.MODE_CFB  # Sets encryption mode to CFB mode; CFB is great in avoiding the hassle of padding
        decryptor = AES.new(self.key, mode, IV)  # Decryptor

        for c in coordinates:
            x1, y1, x2, y2 = c
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            ROI = image[y1:y2, x1:x2]
            img_bytes = np.ascontiguousarray(ROI, dtype=None)

            decData = decryptor.decrypt(img_bytes)  # Encrypted data
            data = np.frombuffer(decData, dtype=np.uint8)
            data = np.reshape(data, (y2 - y1, x2 - x1, 3))
            image[y1:y2, x1:x2] = data

        return image
