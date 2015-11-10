import sys
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
import re
import os
from datetime import datetime
import subprocess

import parse_into_tables

from docker_app import DockerApp

DO_DOWNLOAD = True 
CLOSE_SESSION = True 

class FastQCApp( DockerApp ):
    def __init__(self, access_token, app_session_id, url, version ) :
        self.client_key = "45c02aef58b64a318fb0d9e6debc1119" 
        self.client_secret = "440e9ac55b5842108d2b29cbd80082ce"
        self.api = BaseSpaceAPI( self.client_key, self.client_secret, url, version, app_session_id, access_token )

        self.download_dir = "/home/apps/fastqc/download"
        self.output_dir = "/home/apps/fastqc/output"

if __name__ == "__main__" :

    access_token = "a39cfac46f01453c9804174bb77680fc" 
    app_session_id = "25029"
    url = "https://api.cloud-naboo.illumina.com" #
    version = 'v1pre3'
    fca = FastQCApp( access_token, app_session_id, url, version )
    fca.run()


#ssn_inputs = api.getAppSessionInputsById( app_session_id )
#print ssn_inputs
#
#sample_id = ssn_inputs["sample-id"].Content.Id
#project_id = ssn_inputs["project-id"].Content.Id
#
##TODO make another thirdparty wrapper, and move this there
#def collectUploadFiles( local_dir ) :
    #paths = []
    #for listing in os.listdir( local_dir ) :
        #fullpath = os.path.join( local_dir, listing )
        #if os.path.isdir( fullpath ) :
            #paths.extend( collectUploadFiles( fullpath ) )
        #else :
            #if shouldUploadFile( fullpath ) :
                #paths.append( fullpath )
    #return paths
#
#def shouldUploadFile( filepath ) :
    #return True;
#
#def cleanPath( path ) :
    #r = path.replace(':','-').replace('.','-')
    #return r
#
##alternatively, do getAppResultFiles(...)
#files = api.getFilesBySample( sample_id )
#for f in files:
    #print f.Name
    #print f.Id
   # 
    ##some check to only grab fastq's ?
    #if DO_DOWNLOAD :
        #api.fileDownload( f.Id, download_dir, f.Name )
    #local_path = os.path.join( download_dir, f.Name )
#
    #################################################################
    ##processing with FastQC...
    ################################################################
    #command_list = ['perl', \
                    #'/home/bin/fastqc_v0.10.1_source/FastQC/my_fastqc/fastqc', \
                    #'--outdir=%s' % output_dir, local_path]
    #rcode = subprocess.call( command_list )
    #assert(rcode==0)
#
    #fastqc_output_folder = f.Name[:-6]+"_fastqc" 
    #output_sample_folder = os.path.join( output_dir, fastqc_output_folder )
    #table_file = os.path.join( output_sample_folder, "fastqc_data.txt" )
#
    #parsed_dir = os.path.join( output_sample_folder, "parsed" )
    #if not os.path.exists( parsed_dir ) :
        #os.mkdir( parsed_dir )
    #parse_into_tables.parseIntoTables( table_file, parsed_dir )
#
    ################################################################
    #### Upload
    ###############################################################
#
    ##create app result
    #fmt = "%Y-%m-%d-%H-%M-%S"
    #d = datetime.now( )
    #d_string = d.strftime(fmt)
    #ar_name = f.Name 
    #ar_desc = d_string 
    #ar = api.createAppResult( project_id, ar_name, ar_desc, appSessionId = app_session_id )
#
    #print "collect from: ", output_sample_folder
    #to_upload = collectUploadFiles( output_sample_folder )
    #for local_path in to_upload :
        #server_filepath, server_filename = os.path.split( local_path )
        #ix = server_filepath.find( fastqc_output_folder ) + len(fastqc_output_folder)
        #server_filepath = cleanPath(server_filepath[ix:])
        #print server_filepath, server_filename
        #something = api.appResultFileUpload( ar.Id, local_path, server_filename, server_filepath, "text/plain" )
#
#print "reached the end"
##TODO use the API for this
#if CLOSE_SESSION :
    #subprocess.call(['/bin/bash','/closeSession.sh',access_token,app_session_id,url])
