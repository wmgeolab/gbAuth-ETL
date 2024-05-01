import subprocess
from prefect import flow
import os
import shutil
import datetime

#@flow(flow_run_name="Humanitarian Data",log_prints=True)
def generate_flow_run_name():
    date = datetime.datetime.now(datetime.timezone.utc)

    return f"On-{date:%A}-{date:%B}-{date.day}-{date.year}"

@flow(name="UNSALB: Git Data",flow_run_name=generate_flow_run_name, log_prints=True)
def GitData():
    # Move into the Local Dir
    os.chdir('/sciclone/geounder/dev/geoBoundaries/scripts/geoBoundaryBot/external/AuthData/gitData')

    #Delete the directory SYR2
    subdirectory = "/sciclone/geounder/dev/geoBoundaries/scripts/geoBoundaryBot/external/AuthData/gitData/geoBoundaries"
    if os.path.exists(subdirectory) and os.path.isdir(subdirectory):
        shutil.rmtree(subdirectory)


    # Enable sparse checkout
    subprocess.run(['git', 'sparse-checkout', 'init'])

    # Clone the repository
    subprocess.run(['git', 'clone', '--filter=blob:none', '--no-checkout', 'https://github.com/wmgeolab/geoBoundaries.git'])

    # Move into the cloned repository
    os.chdir('/sciclone/geounder/dev/geoBoundaries/scripts/geoBoundaryBot/external/AuthData/gitData/geoBoundaries')

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
