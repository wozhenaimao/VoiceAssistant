import os, shutil


__TEMP_FOLDER = 'temp'

def clear_temp_dir() -> None:

    for filename in os.listdir(__TEMP_FOLDER):
        file_path = os.path.join(__TEMP_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
