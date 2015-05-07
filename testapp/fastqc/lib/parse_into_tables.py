import sys
from os.path import exists
from os import makedirs

#command args are in file, and out folder
def parseIntoTables( tablefile, out_folder ) :

    fin = open( tablefile )

    version_line = fin.readline()

    for status in ["pass","warn","fail"] :
        status_folder = "%s/%s" % (out_folder,status)
        if not exists( status_folder ) :
            makedirs( status_folder )

    for line in fin.readlines() :
        line = line.strip()

        #module start/end
        if line.startswith('>>') :
            if not line.endswith("END_MODULE") :
                splt = line[2:].rsplit("\t",1)
                module_name = splt[0].replace(" ","_")
                status = splt[1].lower()
                fout = open( "%s/%s/%s.tsv" % (out_folder,status,module_name) ,'w')
            else :
                fout.close()

        #header line
        elif line.startswith('#') :
            splt = line.strip('#').split('\t')
            fout.write( line[1:] + "\n" )

        #data lines
        else :
            fout.write( line + "\n" )

    fin.close()
