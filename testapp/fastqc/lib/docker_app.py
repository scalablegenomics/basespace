import os
import sys
import shutil

UROOT = "/data/output/appresults/"
DROOT = "/data/input/samples/"

#A base class which handles download, execution and upload
#By inheriting, the child app can supply the details of the app's execution
#and not worry about the plumbing
class DockerApp :

    def run( self ) :
        try :
            self.project_id = sys.argv[1]

            ######  Download  ######
            downloaded_files = self.getDownloadedFiles()

            ######  Run  ######
            upload_folders = self.runApp( downloaded_files )

            ######  Upload  ######
            self.setupUpload( upload_folders )

        except Exception as e :
            print "Exception: ", type(e), e
            sys.exit(1)

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
