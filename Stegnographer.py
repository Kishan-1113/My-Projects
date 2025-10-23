import requests
from PIL import Image
from io import BytesIO

def decode_lsb_from_url(image_url):
    """
    Downloads an image from a URL and decodes a hidden message 
    using the Least Significant Bit (LSB) technique.
    """
    try:
        # 1. Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # 2. Open the image from the downloaded content
        img = Image.open(BytesIO(response.content))
        
        binary_message = ""
        # 3. Iterate through pixels to extract LSBs
        for y in range(img.height):
            for x in range(img.width):
                # Ensure we only process RGB, not alpha channel
                try:
                    r, g, b = img.getpixel((x, y))[:3]
                except ValueError:
                    # Handle grayscale or other single-channel images
                    pixel_value = img.getpixel((x,y))
                    binary_message += bin(pixel_value)[-1]
                    # Check for a stop condition
                    if len(binary_message) % 8 == 0 and binary_message.endswith("00000000"):
                         return binary_to_text(binary_message[:-8])
                    continue
                
                binary_message += bin(r)[-1]
                binary_message += bin(g)[-1]
                binary_message += bin(b)[-1]

                # A simple end-of-message marker: a null byte (8 zeros)
                if len(binary_message) % 8 == 0 and binary_message.endswith("00000000"):
                    # Stop here and return the decoded text
                    return binary_to_text(binary_message[:-8])
                    
    except requests.exceptions.RequestException as e:
        return f"Error downloading the image: {e}"
    except Exception as e:
        return f"Error decoding the image: {e}"

def binary_to_text(binary_string):
    """Converts a binary string to a human-readable text string."""
    text_data = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            text_data += chr(int(byte, 2))
    return text_data

# Example usage: Replace with your image URL
image_url = "https://dcchiring2ndyear.web.app/assets/breaking_bad.png"
hidden_message = decode_lsb_from_url(image_url)
print("Hidden message:", hidden_message)