import os
import subprocess
import sys

#post-processing code for RainMaker Report integration
import lib.parse_into_tables as parser

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
        output_dir = "/home/apps/fastqc/output"

        if "use-contaminants" in form_parameters :
            contaminants_file = "/home/bin/fastqc_v0.10.1_source/FastQC/Contaminants/contaminant_list.txt"
            contaminants_switch = "--contaminants=%s" % contaminants_file
        else :
            contaminants_switch = ""

        #pick out the fastq files
        fastq_files = [file for file in downloaded_files \
                       if file.endswith(".fastq") or file.endswith(".fastq.gz")]

        print "THIS is STDOUTOTOTUTUTOUTOUTOTUOTU"
        sys.stderr.write("EROROROR\nOMGITSAn\nERRRRRRROOOOOOOOOOO")
        
        #execute FastQC on each file in parallel
        command_list = ['perl', \
                        '/home/bin/fastqc_v0.10.1_source/FastQC/my_fastqc/fastqc', \
                        '--outdir=%s' % output_dir, \
                        '--kmers=%s' % form_parameters['kmers'], \
                        '--threads=%d' % min( 8, len(fastq_files) ), \
                        contaminants_switch ] + \
                        fastq_files 
        #print " ".join( command_list)
        rcode = subprocess.call( command_list )
        if rcode != 0 : raise Exception("fastqc process exited abnormally")

        #map each file to the output folder FastQC created for it, and add to upload_folders
        for file in fastq_files :
            (head,tail) = os.path.split( file )
            sample_name = tail.replace(".gz",'').replace(".fastq",'')
            fastqc_output_folder = sample_name + "_fastqc"
            output_sample_folder = os.path.join( output_dir, fastqc_output_folder )
            upload_folders.append( output_sample_folder )

        #post-processing
        for output_folder in upload_folders :
            parsed_dir = os.path.join( output_folder, "parsed" )
            if not os.path.exists( parsed_dir ) :
                os.mkdir( parsed_dir )
            table_file = os.path.join( output_folder, "fastqc_data.txt" )
            parser.parseIntoTables( table_file, parsed_dir )

        #for file in downloaded_files :
            #if not (file.endswith( ".fastq" ) or file.endswith( ".fastq.gz" ) ) : continue

            ##run the app
            #output_dir = "/home/apps/fastqc/output"
            #command_list = ['perl', \
                            #'/home/bin/fastqc_v0.10.1_source/FastQC/my_fastqc/fastqc', \
                            #'--outdir=%s' % output_dir, \
                            #'--kmers=%s' % form_parameters['kmers'], \
                            #'--threads=%d' % len(files), \
                            #contaminants_switch , \
                            #file]

            #rcode = subprocess.call( command_list )
            #if rcode != 0 : raise Exception("fastqc process exited abnormally")

            ##identify the data file for post-processing
            #(head,tail) = os.path.split( file )
            #sample_name = tail.replace(".gz",'').replace(".fastq",'')
            #fastqc_output_folder = sample_name + "_fastqc"
            #output_sample_folder = os.path.join( output_dir, fastqc_output_folder )
            #table_file = os.path.join( output_sample_folder, "fastqc_data.txt" )

            ##post-processing
            #parsed_dir = os.path.join( output_sample_folder, "parsed" )
            #if not os.path.exists( parsed_dir ) :
                #os.mkdir( parsed_dir )
            #parser.parseIntoTables( table_file, parsed_dir )

            #upload_folders.append( output_sample_folder )
        
        return upload_folders

#the entry point
if __name__ == "__main__" :
    FastQCApp().run()

    #fca = FastQCApp()
    #inputs = fca.getInputs()
    #for item in inputs :
        #print item, inputs[item]
        #print "\n"

