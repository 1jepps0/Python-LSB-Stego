from PIL import Image 

valid_modes = ["encode", "decode"]
args = sys.argv
mode = args[1].lower()
image_path = args[2]

def help_info():
    print("Invalid Usage")
    print("Usage: python3 stego.py [encode/decode] [image path]")
    exit()

# check for valid usage
if len(args) > 3:
    help_info()

if mode not in valid_modes:
    help_info()

# check if given valid image

def is_valid_image_path(path):
    # Check if the file exists
    if not os.path.exists(path):
        return False
    
    # try opening as image
    try:
        with Image.open(path) as img:
            img.verify()  
        return True
    except (IOError, SyntaxError):
        return False

if not is_valid_image_path(image_path):
    print("Invalid Image Path")
    help_info()

i = 0

def encode_lsb(num, bin):
    global i

    if i < len(bin): 
        # make the least signifigant bit the current bit in the message
        new_number = (num & 0xFE) | int(bin[i])

        i += 1
        return new_number

    return num

def encode_image(path, message):


    with Image.open(path) as image:
        pixels = image.load()
        width, height = image.size

        encoded_image = Image.new("RGB", (width, height), color="white")

        bin = ''.join(format(ord(i), '08b') for i in message)
        i = 0 # reset iterator


        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r, g, b = (encode_lsb(r, bin), encode_lsb(g, bin), encode_lsb(b, bin))

                encoded_image.putpixel((x, y), (r, g, b))

        encoded_image.save("encoded_" + path)



def decode_lsb(num):
    return str(num & 1)


def decode_image(path, message_length):

    with Image.open(path) as image:
        pixels = image.load()
        width, height = image.size

        binary_message = ""

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_message += decode_lsb(r) + decode_lsb(g) + decode_lsb(b)

        decoded_message = ""
        for i in range(0, message_length * 8, 8):
            byte = binary_message[i:i+8]
            decoded_message += chr(int(byte, 2))

        print(decoded_message)
                

secret_message = "I like hotdogs"

encode_image(file_path, secret_message)
decode_image("encoded_" + file_path, len(secret_message))

