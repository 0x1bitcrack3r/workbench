"""This client pushes a big directory of different files into Workbench."""

import zerorpc
import os
import client_helper
import hashlib
import pprint

def all_files_in_directory(path):
    """ Recursively ist all files under a directory """
    file_list = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_list.append(os.path.join(dirname, filename))
    return file_list

def run():
    """This client pushes a big directory of different files into Workbench."""
    
    # Grab server args
    args = client_helper.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])
    
    # Grab all the filenames from the data directory
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data')
    file_list = all_files_in_directory(data_dir)

    # Upload the files into workbench
    md5_list = []
    for path in file_list:

        # Skip OS generated files
        if '.DS_Store' in path: 
            continue

        with open(path,'rb') as f:
            filename = os.path.basename(path)

            # Here we're going to save network traffic by asking
            # Workbench if it already has this md5
            raw_bytes = f.read()
            md5 = hashlib.md5(raw_bytes).hexdigest()
            md5_list.append(md5)
            if workbench.has_sample(md5):
                print 'Workbench already has this sample %s' % md5
            else:
                # Store the sample into workbench
                md5 = workbench.store_sample(filename, raw_bytes, 'unknown')
                print 'Filename %s uploaded: type_tag %s, md5 %s' % (filename, 'unknown', md5)

    # Okay now explode any container types
    workbench.batch_work_request('unzip', {'type_tag': 'zip'})
    workbench.batch_work_request('pcap_bro', {'type_tag': 'pcap'})
    workbench.batch_work_request('mem_procdump', {'type_tag': 'mem'})
    

    # Make sure all files are properly identified
    print 'Info: Ensuring File Identifications...'
    type_tag_set = set()
    meta_all = workbench.batch_work_request('meta')
    for meta in meta_all:
        type_tag_set.add(meta['type_tag'])
    pprint.pprint(type_tag_set)


def test():
    """Executes file_upload test."""
    run()

if __name__ == '__main__':
    run()

