import rsa

publicKey, privateKey = rsa.newkeys(512)

message = "seb is hot"

print("Encrypting " + message)

print(privateKey)

encMessage = rsa.encrypt(message.encode(),publicKey)

print(encMessage)

decMessage = rsa.decrypt(encMessage, privateKey).decode()

print("Message after decryption: " + str(decMessage))

