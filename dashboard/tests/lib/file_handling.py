import os, shutil

def test_create_files(filenames):
    '''

    '''
    for filename in filenames:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write("#")

    return None


def test_delete_folders(folders=[]):
    for folder in folders:
        if(os.path.isdir(folder)):
            shutil.rmtree(folder)
    return None