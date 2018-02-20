import tempfile
import os


static_tmp_path = os.path.join(os.path.dirname(__file__), 'tmp')

def save_file(content):
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, delete=False) as tf:
        for chunk in content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    return tempfile_path

def remove_file(file_path):
    os.remove(file_path)