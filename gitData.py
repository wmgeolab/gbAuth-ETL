import subprocess
from prefect import flow
import os
import shutil

#@flow(flow_run_name="Humanitarian Data",log_prints=True)
def GitData():
    # Move into the Local Dir
    os.chdir('/home/rohith/work/AuthData/gitData')

    #Delete the directory SYR2
    subdirectory = "/home/rohith/work/AuthData/gitData/geoBoundaries"
    if os.path.exists(subdirectory) and os.path.isdir(subdirectory):
        shutil.rmtree(subdirectory)


    # Enable sparse checkout
    subprocess.run(['git', 'sparse-checkout', 'init'])

    # Clone the repository
    subprocess.run(['git', 'clone', '--filter=blob:none', '--no-checkout', 'https://github.com/wmgeolab/geoBoundaries.git'])

    # Move into the cloned repository
    os.chdir('/home/rohith/work/AuthData/gitData/geoBoundaries')

    # Set up sparse checkout
    subprocess.run(['git', 'sparse-checkout', 'set', 'sourceData/gbAuthoritative'])
    subprocess.run(['git', 'sparse-checkout', 'add', '.gitattributes'])
    subprocess.run(['git', 'sparse-checkout', 'add', '.gitignore'])

    # Run git fetch
    # subprocess.run(['git', 'fetch'])
    

    # Checkout
    subprocess.run(['git', 'checkout'])
    print("Succesfully Downloaded Humanitarian Data from Git Hub")

 
GitData()