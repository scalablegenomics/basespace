import os
import subprocess

#Base class which handles download, execution and upload
#By inheriting, we only have to supply the details of the app's execution, not the plumbing
from lib.docker_app import DockerApp

class FastQCApp( DockerApp ):
    def __init__(self) :
        pass

    #The meat and potatoes
    #Input: A list of files that were downloaded.
    #       Form parameters (still TODO)
    #       Do with them what you will.
    #Output: A list of directories containing the output of your app's execution.
    #        Each folder in the list is turned into an AppResult and every file
    #        inside is uploaded into that AppResult, mirroring the directory structure to the server.
    #        The AppResult's name is that of the last folder in the path
    def runApp( self, downloaded_files, form_parameters={} ) :
        upload_folders = []

        for file in downloaded_files :
            if not (file.endswith( ".fastq" ) or file.endswith( ".fastq.gz" ) ) : continue

            #run the app
            output_dir = "/app/fastq2fasta/output"
            command_list = ['python', \
                            '/app/fastq2fasta/converter.py', \
                            '-o %s' % output_dir, file]
            rcode = subprocess.call( command_list )
            if rcode != 0 : raise Exception("fastq2fasta process exited abnormally")

            #identify the data file for post-processing
            (head,tail) = os.path.split( file )
            sample_name = tail.replace(".gz",'').replace(".fastq",'')
            fastqc_output_folder = sample_name + "_fastqc"
            output_sample_folder = os.path.join( output_dir, fastqc_output_folder )

            upload_folders.append( output_sample_folder )

        return upload_folders

#the entry point
if __name__ == "__main__" :
    FastQCApp().run()

