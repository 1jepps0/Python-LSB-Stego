import sys
import os
import argparse
from PIL import Image 

def encode_lsb(num, iterator):
    # Make the last bit in the given number equal to the next bit in our message
    encoded_num = (num & 0xFE) | int(next(iterator))
    return encoded_num 

def encode_image(path, message, output_path):
    with Image.open(path) as image:
        # convert the message into binary with null character, so we know where it ends 
        binary_message = ''.join(format(ord(c), '08b') for c in message) + '00000000' 
        iterator = iter(binary_message)

        pixels = image.getdata()
        encoded_pixels = []
        pixel_count = 0

        # encode each channel of the pixel
        for pixel in pixels:
            pixel_count += 1
            
            if pixel_count <= len(binary_message) / 3:
                encoded_channel = (
                    encode_lsb(pixel[0], iterator),
                    encode_lsb(pixel[1], iterator),
                    encode_lsb(pixel[2], iterator)
                )
            else:
                encoded_channel = pixel

            encoded_pixels.append(encoded_channel)

        # add the encoded pixels to a new image
        encoded_image = Image.new(image.mode, image.size)
        encoded_image.putdata(encoded_pixels)
        encoded_image.save(output_path)
        print(f"Image saved to {output_path}")

def at_end_of_message(message):
    # check for null character (end point)
    return message[-8:] == ('0' * 8)

def decode_image(path):
    with Image.open(path) as image:
        pixels = image.getdata()
        
        # decode the LSB from each channel of each pixel
        binary_message = ""
        break_out = False

        for pixel in pixels:
            for channel in pixel:
                # capture last bit
                binary_message += str(channel & 1)

                if at_end_of_message(binary_message): 
                    break_out = True
                    break
                
            if break_out:
                break

        decoded_message = ""
        for i in range(0, len(binary_message), 8):
            # get each byte and convert it into a char
            byte = binary_message[i:i+8]
            decoded_message += chr(int(byte, 2))

        return decoded_message
                
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

def main():
    parser = argparse.ArgumentParser(description="LSB Steganography Tool")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image")
    encode_parser.add_argument("message", help="Message to encode")
    encode_parser.add_argument("image_path", help="Path to the image file")
    encode_parser.add_argument("output_path", help="Path to save the encoded image")

    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("image_path", help="Path to the encoded image")

    args = parser.parse_args()

    if not is_valid_image_path(args.image_path):
        print("Invalid image file path or format.")
        sys.exit(1)

    if args.mode == "encode":
        encode_image(args.image_path, args.message, args.output_path)
    elif args.mode == "decode":
        message = decode_image(args.image_path)
        print("Decoded Message:\n" + message)

if __name__ == "__main__":
    main()
