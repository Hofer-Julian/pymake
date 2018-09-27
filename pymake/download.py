from __future__ import print_function

import os
from zipfile import ZipFile
import tarfile


def download_and_unzip(url, pth='./', delete_zip=True, verify=True,
                       timeout=30, nattempts=10, chunk_size=204800):
    try:
        import requests
    except Exception as e:
        msg = "pymake.download_and_unzip() error import requests: " + \
              str(e)
        raise Exception(msg)
    if not os.path.exists(pth):
        print('Creating the directory: {}'.format(pth))
        os.makedirs(pth)
    print('Attempting to download the file: ', url)
    file_name = os.path.join(pth, url.split('/')[-1])
    # download the file
    success = False
    for idx in range(nattempts):
        print(' download attempt: {}'.format(idx + 1))
        #
        fs = requests.get(url, stream=True,
                          verify=verify).headers['Content-length']
        bfmt = '{:' + '{}'.format(18) + ',d} bytes'
        print('   file size: ' + bfmt.format(int(fs)))
        ds = 0
        try:
            req = requests.get(url, verify=verify, timeout=timeout)
            with open(file_name, 'wb') as f:
                for chunk in req.iter_content(chunk_size=chunk_size):
                    if chunk:
                        ds += len(chunk)
                        msg = '     downloaded ' + bfmt.format(ds) + \
                              ' of ' + bfmt.format(int(fs)) + \
                              ' ({:10.4%})'.format(float(ds)/float(fs))
                        print(msg)
                        f.write(chunk)
            success = True
        except:
            if idx + 1 == nattempts:
                msg = 'Cannot download file: {}'.format(url)
                raise Exception(msg)
        if success:
            break

    # Unzip the file, and delete zip file if successful.
    if 'zip' in os.path.basename(file_name) or \
                    'exe' in os.path.basename(file_name):
        z = ZipFile(file_name)
        try:
            print('Extracting the zipfile...')
            z.extractall(pth)
        except:
            p = 'Could not unzip the file.  Stopping.'
            raise Exception(p)
        z.close()
    elif 'tar' in os.path.basename(file_name):
        ar = tarfile.open(file_name)
        ar.extractall(path=pth)
        ar.close()
    if delete_zip:
        print('Deleting the zipfile...')
        os.remove(file_name)
    print('Done downloading and extracting...')
