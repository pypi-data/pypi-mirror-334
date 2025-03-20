# File: encryptionx/utils.py
import os
import io
import zipfile

def read_input(data, mode):
    """
    Read input data based on mode.
    Modes: 'text', 'file', 'folder'
    """
    if mode == 'text':
        return data.encode('utf-8')
    elif mode == 'file':
        with open(data, 'rb') as f:
            return f.read()
    elif mode == 'folder':
        # Compress folder into a zip archive in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(data):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, data)
                    zip_file.write(file_path, arcname)
        return zip_buffer.getvalue()
    else:
        raise ValueError("Invalid mode. Use 'text', 'file', or 'folder'.")

def write_output(data, mode, output):
    """
    Write output data based on mode.
    Modes: 'text', 'file', 'folder'
    """
    if output is None:
        return data
    if mode == 'text':
        with open(output, 'w', encoding='utf-8') as f:
            f.write(data.decode('utf-8'))
    elif mode == 'file':
        with open(output, 'wb') as f:
            f.write(data)
    elif mode == 'folder':
        # Assume data is a zip archive; extract to output folder
        with zipfile.ZipFile(io.BytesIO(data), 'r') as zip_file:
            zip_file.extractall(output)
    else:
        raise ValueError("Invalid mode. Use 'text', 'file', or 'folder'.")
