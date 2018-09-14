from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

# Generate a pair
key = RSA.generate(1024)

# Get the key strings
privKey = key.exportKey()
pubKey = key.publickey().exportKey()

# Message

message = """
    key = RSA.generate(2048)

    binPrivKey = key.exportKey('DER')
    binPubKey =  key.publickey().exportKey('DER')

    privKeyObj = RSA.importKey(binPrivKey)
    pubKeyObj =  RSA.importKey(binPubKey)

    msg = "attack at dawn"
    emsg = pubKeyObj.encrypt(msg, 'x')[0]
    dmsg = privKeyObj.decrypt(emsg)

    assert(msg == dmsg)
"""

## Generate trusted data

binary_message = message.encode('utf8')
signature = key.encrypt(binary_message, 0)
data = (binary_message, signature, pubKey)

## Verify the trust

b, s, pk = data

key = RSA.importKey(pk)


