import os
import sys
import shutil
import json

UROOT = "/data/output/appresults/"
INPUT = "/data/input"
DROOT = "%s/samples/" % INPUT
#APPSESSION_FILE = "/home/apps/fastqc/sample_session.json" #"%s/AppSession.json" % INPUT
APPSESSION_FILE = "%s/AppSession.json" % INPUT

#A base class which handles download, execution and upload
#By inheriting, the child app can supply the details of the app's execution
#and not worry about the plumbing
class DockerApp :

    def run( self ) :
        myerr = open("/home/apps/fastqc/stderr.txt",'w')
        #myout = open("/home/apps/fastqc/stdout.txt",'w')
        sys.stderr = myerr
        #sys.stdout = myout

        try :
            form_parameters = self.getInputs()
            self.project_id = form_parameters["project-id"]["Id"] #sys.argv[1]  

            ######  Download  ######
            downloaded_files = self.getDownloadedFiles()

            ######  Run  ######
            upload_folders = self.runApp( downloaded_files, form_parameters ) 

            ######  Upload  ######
            self.setupUpload( upload_folders )

        except Exception as e :
            print "Exception: ", type(e), e
            sys.exit(1)
        finally :
            myerr.close()
            #myout.close()

    def getDownloadedFiles(self) :
        downloaded_files = []
        for path, dirs, files in os.walk( DROOT ) :
            for file in files :
                downloaded_files.append( os.path.join( path, file ) )

        return downloaded_files

    def setupUpload( self, upload_folders ) :
        for upload_folder in upload_folders :
            (head, ar_name) = os.path.split( upload_folder )
            target = os.path.join( UROOT, self.project_id )
            shutil.move( upload_folder, os.path.join( target, ar_name ) ) 
            

    def getInputs(self) :
        fin = open(APPSESSION_FILE)
        obj = json.loads( fin.read() )
        fin.close()
        inputs = {}
        prefix = "Input."
        for item in obj["Properties"]["Items"] :
            if item["Name"].startswith(prefix) :
                name = item["Name"][len(prefix):]
                if "Content" in item :
                    inputs[name] = item["Content"]
                elif "Items" in item :
                    inputs[name] = item["Items"]

        return inputs


