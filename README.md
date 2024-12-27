# LSB Steganography Tool
* A tool built with python and [Pillow](https://pillow.readthedocs.io/en/stable/) that uses the least significant bits of an image to encode a message*

## Features
- **Encode a message**: encode a message into an image by modifying the least significant bits of the image's pixels.
- **Decode a message**: decode a message from an image.

## Requirements
- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) library for image manipulation

## Installation
Install the required dependencies (just pillow):
    ```bash
    pip install -r requirements.txt
    ```

## Usage
- Encoding
    ```bash
    python3 stego.py encode <message> <image_path> <output_path>
    ```
- Decoding
    ```bash
    python3 stego.py decode <image_path>
    ```

#### Arguments:
- `<message>`: The text message to encode.
- `<image_path>`: Path to the input image file.
- `<output_path>`: Path to save the image with the encoded message.

#### Example:
```bash
python stego.py encode "Hello, World!" input.png output.png
```

## Notes
- Doesn't work with jpeg images due to lossy compression
- Made to work with png images, but can probably work for others
- The image needs enough pixels to store the message. Since a pixel can store 3 bits of a message; (len(message) * 8) / 3 = #pixels needed
- The longer the message, the easier it will be to detect encoding

## Disclaimer
This tool is for educational purposes only. Use responsibly and ensure compliance with applicable laws and regulations.



