import os
from django.conf import settings

class Folder():
    '''
    Virtual Model for Handling Folders of a Dataset
    '''

    def all(path=None):
        '''
        list all folders available for user data path
        '''
        if path is None:
            path = settings.DATAFRONTEND['DATA_PATH']

        output = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        output.sort()
        return output


    def files(path, extensions=['.png', 'jpg']):
        '''
        get all files of type in folder
        '''
        files = []
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)) or (len(extensions) > 0 and not file.endswith(tuple(extensions))):
                continue
            files.append(file)
        return files


    def files_dataset(path, identifier=None, data=[]):
        '''
        create dataset recursive by folderpath
        uses folderpath as dataset_name
        '''
        if identifier is None:
            identifier = os.path.basename(os.path.normpath(path))

        for file in Folder.files(path):
            data.append([os.path.join(path, file), identifier])

        for folder in Folder.all(path):
            Folder.files_dataset(
                os.path.join(path, folder),
                identifier=('%s_%s' % (identifier, folder)),
                data=data
            )

        return data
            
