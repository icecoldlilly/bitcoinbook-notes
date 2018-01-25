import ecdsa
import os

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
# Define secp256k1 Elliptic Curve Finite Prime Field
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
# Define secp256k1 Generator point
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
# Define Object identifier for secp256k1
oid_secp256k1 = (1, 3, 132, 0, 10)
# Define SECP256K1 Elliptic Curve, with variables define above
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1,
                               generator_secp256k1, oid_secp256k1)
# Define order of the Elliptic Curve
ec_order = _r

# Rename variables to easier conventions
curve = curve_secp256k1
generator = generator_secp256k1

# A method that creates a random secret by: 
# 1) drawing a random 32-byte array (32*8=256 bit) number,
# 2) passing to anon lambda function, 
# 3) anon function encodes to hex,
def random_secret():
    convert_to_int = lambda array: int("".join(array).encode("hex"), 16)

    # Collect 256 bits of random data from the OS's cryptographically secure
    # random generator
    byte_array = os.urandom(32)

    return convert_to_int(byte_array)

# A method that constructs pubkey of given point by: 
# 1) accepting hex point as input
# 2) concating '03' for positive 'y' value points and '02' otherwise,
# 3) concating result of mod '%064x' by 'x' value of point,
# 4) decode hex of the result
def get_point_pubkey(point):
    key = ('03' if point.y() & 1 else '02') + '%064x' % point.x()
    return key.decode('hex')

# A method that constructs uncompressed pubkey of given point by: 
# 1) accepting hex point as input
# 2) concating '03' prefix for positive 'y' value points, or '02' prefix otherwise,
# 3) taking result of mod '%064x' by 'x' value of point,
# 4) taking result of mod '%064x' by 'y' value of point,
# 5) concating sum result of 3) & 4)
# 6) decode hex of the result
def get_point_pubkey_uncompressed(point):
    key = ('04' +
           '%064x' % point.x() +
           '%064x' % point.y())
    return key.decode('hex')


# Generate a new private key.
secret = random_secret()
print("Secret: ", secret)

# Get the public key point.
point = secret * generator
print("EC point:", point)

print("BTC public key:", get_point_pubkey(point).encode("hex"))

# Given the point (x, y) we can create the object using:
point1 = ecdsa.ellipticcurve.Point(curve, point.x(), point.y(), ec_order)
assert(point1 == point)