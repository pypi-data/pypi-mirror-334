import asyncio
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import json
import logging
import socket


from .crypto_utils import calu_crc, encrypt_aes, decrypt_aes
from .custom_exceptions import InvalidDataException
from .socket_utils import async_send_http_request, send_http_request, DEFAULT_PORT


# Set up logging
_LOGGER = logging.getLogger(__name__)

def check_not_found_case(response):
    """Check if the response indicates a 'not found' case."""
    return "404 Not Found" not in response

# Main function to send operation data
# {"port1":{"temperature":<value>}}
def send_operation_data(ip_address, key, data, command_suffix):
    """ Api to send command to the device."""
    try:
        send_data = data + command_suffix
        raw_data = send_data.encode("utf-8")
        
        # Generate AES IV
        aes_iv = get_random_bytes(16)
        
        # Decode the AES key
        aes_key = base64.b64decode(key)
        
        # Encrypt the data
        encrypted_data = encrypt_aes(aes_key, aes_iv, raw_data)
        
        # Prepare the data packet
        key_send_data = bytearray(aes_iv + encrypted_data)
        
        # Calculate and append CRC
        checksum = calu_crc(0, key_send_data, len(key_send_data))
        key_send_data.extend([(checksum & 0xFF), (checksum >> 8) & 0xFF])
        
        # Encode the packet with Base64
        body_data = base64.b64encode(key_send_data).decode("utf-8")

        # Prepare HTTP POST request
        request_str = (
            f"POST /acstatus HTTP/1.1\r\n"
            f"Host: {ip_address}\r\n"
            f"Content-Length: {len(body_data)}\r\n"
            f"\r\n{body_data}"
        )
        
        # Use the common function to send the request and get the parsed response
        headers, body = send_http_request(ip_address, DEFAULT_PORT, request_str, timeout=10)

        if len(body) == 0:
            _LOGGER.debug("Received empty data.")
            raise InvalidDataException()

        # Process the response body
        _LOGGER.debug(f"Command sent successfully.")

        # Extract the Base64 encoded body
        encoded_body = body
        decoded_body = base64.b64decode(encoded_body)

        # Verify CRC
        total_len = len(decoded_body)
        checksum_received = ((decoded_body[total_len - 1] & 0xFF) << 8) | (decoded_body[total_len - 2] & 0xFF)
        calculated_checksum = calu_crc(0, decoded_body, total_len - 2) & 0xFFFF
        _LOGGER.debug(f"Calculated checksum: {calculated_checksum}, Packet checksum: {checksum_received}")
        
        if checksum_received != calculated_checksum:
            _LOGGER.debug("Checksum validation failed.")
            raise InvalidDataException()
        
        # Extract AES IV and encrypted data
        aes_iv = decoded_body[:16]
        encrypted_data = decoded_body[17:-2]

        # Decrypt data
        decrypted_data = decrypt_aes(aes_key, aes_iv, encrypted_data)
        decrypted_str = decrypted_data.decode("utf-8")
        
        # Parse the decrypted data as JSON
        try:
            device_status = json.loads(decrypted_str)
            return device_status
        except json.JSONDecodeError:
            _LOGGER.debug("Failed to decode decrypted data as JSON.")
            raise InvalidDataException()
    
    except Exception as e:
        _LOGGER.error("Failed to send command: %s", e)
        return None

async def async_send_operation_data(ip_address, key, data, command_suffix):
    """Async API to send command to the device with the same logic """
    try:
        send_data = data + command_suffix
        raw_data = send_data.encode("utf-8")
        
        # Generate AES IV
        aes_iv = get_random_bytes(16)
        
        # Decode the AES key
        aes_key = base64.b64decode(key)
        
        # Encrypt the data
        encrypted_data = encrypt_aes(aes_key, aes_iv, raw_data)
        
        # Prepare the data packet
        key_send_data = bytearray(aes_iv + encrypted_data)
        
        # Calculate and append CRC
        checksum = calu_crc(0, key_send_data, len(key_send_data))
        key_send_data.extend([(checksum & 0xFF), (checksum >> 8) & 0xFF])
        
        # Encode the packet with Base64
        body_data = base64.b64encode(key_send_data).decode("utf-8")

        # Prepare HTTP POST request
        request_str = (
            f"POST /acstatus HTTP/1.1\r\n"
            f"Host: {ip_address}\r\n"
            f"Content-Length: {len(body_data)}\r\n"
            f"\r\n{body_data}"
        )
        
        # Use the common function to send the request and get the parsed response
        headers, body = await async_send_http_request(ip_address, DEFAULT_PORT, request_str, timeout=10)

        if len(body) == 0:
            _LOGGER.debug("Received empty data.")
            raise InvalidDataException()

        # Process the response body
        _LOGGER.debug(f"Command sent successfully.")

        # Extract the Base64 encoded body
        encoded_body = body
        decoded_body = base64.b64decode(encoded_body)

        # Verify CRC
        total_len = len(decoded_body)
        checksum_received = ((decoded_body[total_len - 1] & 0xFF) << 8) | (decoded_body[total_len - 2] & 0xFF)
        calculated_checksum = calu_crc(0, decoded_body, total_len - 2) & 0xFFFF
        _LOGGER.debug(f"Calculated checksum: {calculated_checksum}, Packet checksum: {checksum_received}")
        
        if checksum_received != calculated_checksum:
            _LOGGER.debug("Checksum validation failed.")
            raise InvalidDataException()
        
        # Extract AES IV and encrypted data
        aes_iv = decoded_body[:16]
        encrypted_data = decoded_body[17:-2]

        # Decrypt data
        decrypted_data = decrypt_aes(aes_key, aes_iv, encrypted_data)
        decrypted_str = decrypted_data.decode("utf-8")
        
        # Parse the decrypted data as JSON
        try:
            device_status = json.loads(decrypted_str)
            return device_status
        except json.JSONDecodeError:
            _LOGGER.debug("Failed to decode decrypted data as JSON.")
            raise InvalidDataException()
    
    except Exception as e:
        _LOGGER.error("Failed to send command: %s", e)
        return None
