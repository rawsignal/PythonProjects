#######################################CONFIG DETAILS#######################################
import os
import sys
import ConfigParser

def get_Config(section) :
    data = {}
    options = config.options(section)

    for option in options :
        try:
            data[option] = config.get(section, option)
            if data[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            data[option] = None
            
    return data

config_File_Name = "config.ini"

config = ConfigParser.ConfigParser()

if os.path.isfile(config_File_Name) :
    config.read(config_File_Name)
else:
    raw_input("WARNING! Configuration file not found. Please close the application and ensure the {0} is present in the directory of the script, and try again.".format(config_File_Name))

db_UN = get_Config("Connections")['user']
db_PW = get_Config("Connections")['password']
db_SN = get_Config("Connections")['servername']
db_DB = get_Config("Connections")['db']
fn_MissingList = get_Config("FileNames")['missinglist']
fn_OutputFN = get_Config("FileNames")['outputfilename']
fn_L601 = get_Config("FileNames")['fromusps']
get_Keys = get_Config("Queries")['getkeys']
get_Missing_BMCs = get_Config("Queries")['missingbmcs']
use_File = config.getboolean("RunType", 'usefile')

import sybpydb as sybase

#######################################END OF SETUP#######################################




def initial_Check() :
    print("Current settings: \n" +
          "------------DB SETTINGS------------\n" +
          "Username: " + db_UN + "\n" +
          "Password: " + db_PW + "\n" +
          "Server: " + db_SN + "\n" +
          "Database: " + db_DB + "\n" +
          "--------------FILENAMES------------\n" +
          "Missing List Input: " + fn_MissingList + "\n" +
          "L601 USPS: " + fn_L601 + "\n" +
          "Output File: " + fn_OutputFN + "\n" +
          "---------------RUN TYPE-------------\n" +
          "Run type will determine if the program will use an input file or query sybase for missing BMC's." +
          "Run Type: " + str(use_File) + ".\n If True, it will use the input file. If False, it will query Sybase\n" +
          "Queries: {0} and {1}".format(get_Keys, get_Missing_BMCs))
    raw_input("If these settings are OK, press any key to continue. Otherwise, please exit this window and update config.ini")

def find_File() :
    # File can be downloaded from here: https://fast.usps.com/fast/fastApp/resources/labelListFiles.action

    file_Sto = fn_L601
    returned_List = []
    list_Files = os.listdir('input')

    for files in list_Files :
        if files.startswith(file_Sto) :
            returned_List.append(files)
        

    if not returned_List :
        input("Error! Unable to store a file within the program. This could be because there was no file in the directory of the script. Press any key to end.")

    file_Name = os.path.join('input', returned_List[0])

    return file_Name

def store_Values(file_Name) :
    file_Tmp = open(file_Name, "r")
    store_Value = []
    
    for line in file_Tmp :
        store_Value.append(line.split('|'))

    file_Tmp.close()

    return store_Value

# File spec:
# 2 = zip
# 5 = SCF or NDC
# 6 = CITY

# Now we want to import the missing BMC's, search the store_Value list for a match, and return the ZIP, City + SCF or NDC, and later we can query
# Sybase to find the drop ship code we need

def match_Values(store_Value, frm_DB, missing_BMCs) :
    # Create a dictionary to hold the translations between our NDC/LDC values vs. USPS
    # USPS value from the L601 file is the key, our translation is the value.
    translator = {'MPLS/STP' : 'MINNEAPOLIS SAINT PAUL',
                  'SAN FRAN' : 'SAN FRANCISCO',
                  'KANS CITY' : 'KANSAS CITY',
                  'JAXVILLE' : 'JACKSONVILLE',
                  'PHILA' : 'PHILADELPHIA',
                  'CINCINN' : 'CINCINNATI',
                  'SPFLD' : 'SPRINGFIELD'}
                  
                  
                  

    results = []
    db_Cln = []

    # Trim whitespace from db results
    for y in range(0, len(frm_DB)) :
        result = [frm_DB[y][0].rstrip(' ').rstrip('LDC').rstrip('NDC').rstrip(' '), frm_DB[y][1], frm_DB[y][2]]
        db_Cln.append(result)


    for element in list(missing_BMCs) :
        for i in range(0, len(store_Value)) :
            if element[0] in store_Value[i][2] :
                if store_Value[i][6] in translator :
                    store_Value[i][6] = translator[store_Value[i][6]]

                for y in range(0, len(db_Cln)) :
                    if db_Cln[y][0] == store_Value[i][6] :

                        result = [store_Value[i][2], frm_DB[y][0].rstrip(' '), frm_DB[y][2], frm_DB[y][1]]
                        results.append(result)
    print(results)
    return results

def query_DB(query, con) :
    quer = con.cursor()
    quer.execute(db_DB)

    stored_Val = []

    quer.execute(query)

    for row in quer.fetchall() :
        stored_Val.append(row)

    if not stored_Val :
        stored_Val.append("ERROR. Query to sybase failed.")

        
    
    return stored_Val

def get_Missing_From_File() :
    file_Name = os.path.join('input', fn_MissingList)
    file_Tmp = open(file_Name, "r")
    search_List = []

    for line in file_Tmp :
        search_List.append(line.rstrip('\n'))

    file_Tmp.close()
    
    return search_List


# Output to generate insert statements for the devs
def generate_Insert(results) :
    out_Path = os.path.join('output', fn_OutputFN)
    output_File = open(out_Path, "w+")

    output_File.write("begin transaction fixDropShipZips\n")

    for i in range(0, len(results)) :        
        output_File.write("INSERT drop_ship_zip_sites VALUES('{0}', '{1}', '{2}', '{3}')".format(results[i][0], "ALL", results[i][2], results[i][3]))
        output_File.write("\n")

    output_File.write("SELECT @error_count = @@error + @error_count\n")

    output_File.write(" IF ( @error_count = 0 )\n" +
                      " BEGIN\n" +
                      " COMMIT TRANSACTION fixDropShipZips\n" +
                      " PRINT ''\n" +
                      " PRINT 'No errors occurred - Changes have been committed'\n" +
                      " END\n" +
                      " ELSE\n" +
                      " BEGIN\n" +
                      " ROLLBACK TRANSACTION fixDropShipZips\n" +
                      " PRINT ''\n" +
                      " PRINT 'An error occurred - Changes have been rolled back'\n" +
                      " END\n")

    output_File.close()

def main() :
    conn = sybase.connect(user=db_UN, password=db_PW, servername=db_SN)
    initial_Check()
    query = get_Keys
    missing_BMCs = get_Missing_BMCs
    file_Name = find_File()
    stored_Value = store_Values(file_Name)
    
    
    if use_File == True :
        querydb = query_DB(query, conn)
        frm_File = get_Missing_From_File()
        results = match_Values(stored_Value, querydb, frm_File)
    else:
        querydb = query_DB(query, conn)
        queryformissing = query_DB(missing_BMCs, conn)
        results = match_Values(stored_Value, querydb, queryformissing)

    conn.close()
    
    generate_Insert(results)

main()


