import os
import sys
import sybpydb as sybase
import datetime
from collections import Counter

db_UN = 'gisuser'
db_PW = 'bng67f'
db_SN = 'ctmtst'

# The purpose of this script is to automate the gathering of data that is
# Required to ensure that the collation address file data is accurate for
# Selective Insertion testing. This currently is not designed to validate
# the format of the file, though that can be done.

class Collation_Address(object) :
    #This object represents a single line item in the collation address file

    def __init__(self, job_id, nta_id, envelope_Seq_Num, add_ln_1, add_ln_2, add_ln_3, add_ln_4, add_ln_5, wht_spc, quality_divert, tray_serial_num, final_dest,
                 finished_dt_tm, machine_id, imb_code) :
        self.job_id = job_id
        self.nta_id = nta_id
        self.envelope_Seq_Num = envelope_Seq_Num
        self.add_ln_1 = add_ln_1
        self.add_ln_2 = add_ln_2
        self.add_ln_3 = add_ln_3
        self.add_ln_4 = add_ln_4
        self.add_ln_5 = add_ln_5
        self.wht_spc = wht_spc
        self.quality_divert = quality_divert
        self.tray_serial_num = tray_serial_num
        self.final_dest = final_dest
        self.finished_dt_tm = finished_dt_tm
        self.machine_id = machine_id
        self.imb_code = imb_code

    def get_Job_ID(self) :
        return self.job_id

    def get_NTA_ID(self) :
        return self.nta_id

    def get_Job_NTA(self) :
        return self.job_id + self.nta_id
    
    def get_Address(self) :
        return self.add_ln_4

    def get_AddLn2(self) :
        return self.add_ln_2

    def get_Quality_Divert(self) :
        return self.quality_divert

    def get_Feeder_Code(self) :
        return self.finished_dt_tm

    def get_Tray_SN(self) :
        return self.tray_serial_num

    def is_Sample(self) :
        is_Sample = False
        if 'QC' in self.add_ln_2 or 'Samples' in self.add_ln_1 or self.tray_serial_num == '00000000' :
            is_Sample = True

        return is_Sample

    def simple_Compare(self) :
        return "{0}, {1}, {2}".format(self.get_Job_NTA(), self.get_Address(), self.get_Feeder_Code())


class Collation_Data_Simple(object) :
    def __init__(self, address, feeder_code) :
        self.address = address
        self.feeder_code = feeder_code

    def get_Address(self) :
        return self.address

    def get_Feeder_Code(self) :
        return self.feeder_code

    def __str__(self) :
        return self.address + ", " + self.feeder_code

class Collation_Data_Trays(object) :
    def __init__(self, jobnta, tray_SN) :
        self.jobnta = jobnta
        self.tray_SN = tray_SN

    def get_Job_NTA(self) :
        return self.jobnta

    def get_Tray_SN(self) :
        return self.tray_SN

    def __str__(self) :
        return self.jobnta + ", " + self.tray_SN

    

class Client_Address(object) :
    #This object represents a single line item in the client file

    def __init__(self, address, zip4, jobid, nta, feeder_code) :
        self.address = address
        self.zip4 = zip4
        self.jobid = jobid
        self.nta = nta
        self.feeder_code = feeder_code

    def get_Address(self) :
        return self.address

    def get_zip4(self) :
        return self.zip4

    def get_Job_ID(self) :
        return self.jobid

    def get_NTA(self) :
        return self.nta

    def get_Feeder_Code(self) :
        return self.feeder_code

    def set_Feeder_Code(self, feeder_code) :
        self.feeder_code = feeder_code

    def get_Job_NTA(self) :
        return self.jobid + self.nta

    def simple_Compare(self) :
        return "{0}, {1}, {2}".format(self.get_Job_NTA(), self.get_Address(), self.get_Feeder_Code())
    
    def simple_Compare_ZIP(self) :
        return "{0}, {1}, {2}, {3}".format(self.get_Job_NTA(), self.get_Address(), self.get_zip4(), self.get_Feeder_Code())

    def simple_Compare_NF(self) :
        return "{0}, {1}, {2}".format(self.get_Job_NTA(), self.get_Address(), self.get_zip4())

    def export_Format(self) :
        return "{0}	{1}	{2}	{3}".format(self.get_Address(), self.get_zip4(), self.get_Job_NTA(), self.get_Feeder_Code())

    def __str__(self) :
        return "{0}	{1}	{2}{3}	{4}".format(self.address, self.zip4, self.jobid, self.nta, self.feeder_code)

class Interfaced_Client_Address(Client_Address) :
    #This is an extension of Client_Address which is populated with data from the DB

    def __init__(self, job_id, nta, zip4, address, feeder_code, franchise, batch_id) :
        self.job_id = job_id
        self.batch_id = batch_id

    def get_Job_Id(self) :
        return self.job_id

    def get_Batch_ID(self) :
        return self.batch_id


def get_Collation_Address_Files() :
    returned_List = []
    list_Files = os.listdir('collation address files')
        
    for files in list_Files :
        returned_List.append(os.path.join('collation address files', files))

    return returned_List

def get_Client_File() :
    # This will simply return the first file it finds. The logic is not built to handle more than one client file at a time for this test.
    returned_List = []
    list_Files = os.listdir('client files')
        
    for files in list_Files :
        returned_List.append(os.path.join('client files', files))

    return returned_List

def query_DB(query, con) :
    db_DB = 'use insidevalpak'
    quer = con.cursor()
    quer.execute(db_DB)

    stored_Val = []

    quer.execute(query)

    for row in quer.fetchall() :
        stored_Val.append(row)

    if not stored_Val :
        stored_Val.append("ERROR. Query to sybase failed.")

        
    
    return stored_Val


def create_Client_File_Objects(client_file) :
    
    list_of_client_files = []
    for element in client_file :
        tmp_Client_File = open(element)
        cf_objs = []
        for line in tmp_Client_File :
            new_line = line.split("	")
            address = new_line[0]
            zip4 = new_line[1]
            jobid = new_line[2][0:6]
            nta = new_line[2][6:]
            feeder_code = new_line[3]

            cf_objs.append(Client_Address(address, zip4, jobid, nta, feeder_code.rstrip("\n")))
        list_of_client_files.append(cf_objs)
        tmp_Client_File.close()

    return list_of_client_files

def split_By_JobNTA(client_objects, client_file_list) :
    i = 0
    for clfile in client_objects :
        job_NTA_List = []
        unique_Feeder_List = []
        summary_Report = []
        for item in clfile :
            if item.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(item.get_Job_NTA())
            if item.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(item.get_Feeder_Code())
        file_name_start = client_file_list[i].rstrip(".TXT").replace("client files\\", "")
        for jobnta in job_NTA_List :
            tmp = []
            gttl = 0
            for item in clfile :
                if item.get_Job_NTA() == jobnta :
                    tmp.append(str(item))
            for feeder in unique_Feeder_List :
                ttl = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta for c in client_objects for a in c)
                gttl += ttl
                report_str = "{0}, {1}: {2}".format(jobnta, feeder, ttl)
                summary_Report.append(report_str)
            gttl_Summary = "Grand total of addresses: {0}, estimate of addresses that will be assigned to default feeder: {1}".format(gttl, 10000-gttl)
            summary_Report.append(gttl_Summary)
            file_name = "{0}_ClientFile_{1}".format(file_name_start, jobnta)
            out_To_File(file_name, tmp)

        out_To_File("Client_File_{0}_JobNTA_Summary".format(file_name_start), summary_Report)
        i += 1

def list_Duplicates_From_Client_File(client_objects, client_file_list) :
    simple_No_Feeder = []
    i = 0
    for clfile in client_objects :
        for item in clfile :
            simple_No_Feeder.append(item.simple_Compare_NF())     
        tmp = [k for k, v in Counter(simple_No_Feeder).items() if v>1]
        
    
        dupes = []
        output_List = []
        for item in clfile :
            for x in tmp :
                if item.simple_Compare_NF() == x :
                   dupes.append(item.simple_Compare_ZIP())
                   item.set_Feeder_Code('PPPPHKPP')
            output_List.append(item.export_Format())
        
        file_name_start = client_file_list[i].rstrip(".TXT").replace("client files\\", "")
        out_To_File(file_name_start + "_DuplicateAddressInClientFile", dupes)
        print("File {0} processed...".format(file_name_start))
        is_Shutterfly = raw_input("Is '{0}' a Shutterfly client file? Type 'yes' or 'no'.".format(file_name_start))  
        if is_Shutterfly == "yes" :
            out_To_File(file_name_start + "_updated", output_List)
        i += 1
        
def report_Counts(collation_Objects) :
    unique_Feeder_List = []
    job_NTA_List = []
    output = []
    for collationfile in collation_Objects :
        for address in collationfile :
            if address.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(address.get_Feeder_Code())
            if address.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(address.get_Job_NTA())
    print("Processing. Please wait. This could take some time.")
    for jobnta in job_NTA_List :
        for feeder in unique_Feeder_List :
            ttl_WO_Samples = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta and a.is_Sample() == False for c in collation_Objects for a in c)
            ttl_Sampls = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta for c in collation_Objects for a in c) - sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta and a.is_Sample() == False for c in collation_Objects for a in c)
            report_String = "{0}, {1}, {2}, {3}".format(jobnta, feeder, ttl_WO_Samples, ttl_Sampls)
            output.append(report_String)

    out_To_File("FeederCounts", output)


def create_Collation_Address_File_Objects(collation_Add_File_List) :
    
    list_of_objs = []
    for collation_File in collation_Add_File_List :
        file_Tmp = open(collation_File, "r")
        objs = []
        for line in file_Tmp :
            job_id = line[0:6].lstrip(' ').rstrip(' ')
            nta_id = line[6:11].lstrip(' ').rstrip(' ')
            envelope_seq_num = line[12:18].lstrip(' ').rstrip(' ')
            add_ln_1 = line[19:88].lstrip(' ').rstrip(' ')
            add_ln_2 = line[88:158].lstrip(' ').rstrip(' ')
            add_ln_3 = line[158:228].lstrip(' ').rstrip(' ')
            add_ln_4 = line[228:298].lstrip(' ').rstrip(' ')
            add_ln_5 = line[298:369].lstrip(' ').rstrip(' ')
            wht_spc = line[369:438]
            qual_div = line[438].lstrip(' ').rstrip(' ')
            tray_serial = line[439:447].lstrip(' ').rstrip(' ')
            final_dest = line[447].lstrip(' ').rstrip(' ')
            feeder_code = line[448:462].lstrip(' ').rstrip(' ')
            machine_id = line[462:467].lstrip(' ').rstrip(' ')
            imb_code = line[467:497].lstrip(' ').rstrip(' ')
            objs.append(Collation_Address(job_id, nta_id, envelope_seq_num, add_ln_1, add_ln_2, add_ln_3, add_ln_4, add_ln_5, wht_spc, qual_div, tray_serial, final_dest,
                                          feeder_code, machine_id, imb_code))
        list_of_objs.append(objs)
        
        file_Tmp.close()
        

    return list_of_objs

def verify_Tray_Extract_From_Collation_Address_File(collation_Objects) :
    job_NTA_List = []
    tray_Objects_List = []
    output = []
    for clfile in collation_Objects :
        for address in clfile :
            if address.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(address.get_Job_NTA())
        

    for jobnta in job_NTA_List :
        tray_Serial_List = []
        for clfile in collation_Objects :
            for address in clfile :
                if address.get_Job_NTA() == jobnta and address.get_Tray_SN() not in tray_Serial_List :
                    tray_Serial_List.append(address.get_Tray_SN())
        
        for tray in tray_Serial_List :
            ttl = sum(a.get_Tray_SN() == tray for c in collation_Objects for a in c if a.get_Job_NTA() == jobnta)
            report_String = "{0}, {1}, {2}".format(jobnta, tray, ttl)
            output.append(report_String)

    out_To_File("TrayExtractReport", output)
        

def compare_Collation_Files(collation_Objects) :
    run_Flag = True
    while run_Flag == True :
        count_Files = len(collation_Objects)
        print("There are a total of {0} collation files stored.".format(count_Files))

        for i in range(0, count_Files) :
            print("Press {0} for {1}".format(i, collation_Objects[i][1].get_Job_NTA()))

        file_location_1 = raw_input("Press the number for your selection, and then enter, to select the first file.")
        file_location_2 = raw_input("Press the number for your selection, and then enter, to select the second file.")
        file_loc_int_1 = int(file_location_1)
        file_loc_int_2 = int(file_location_2)

        raw_input("You wish to compare file {0} to file {1} - press enter to continue.".format(collation_Objects[file_loc_int_1][1].get_Job_NTA(), collation_Objects[file_loc_int_2][1].get_Job_NTA()))

        unique_Feeder_List = []
        for files in collation_Objects[file_loc_int_1] + collation_Objects[file_loc_int_2] :
            if files.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(files.get_Feeder_Code())
                
        file1_list = []
        for item in collation_Objects[file_loc_int_1] :
            if item.is_Sample() == False : 
                file1_list.append(item.simple_Compare())

        file2_list = []
        for item in collation_Objects[file_loc_int_2] :
            if item.is_Sample() == False : 
                file2_list.append(item.simple_Compare())

        s = set(file1_list)
        t = set(file2_list)

        diff1 = [x for x in file1_list if x not in file2_list]
        diff2 = [x for x in file2_list if x not in file1_list]

        tmp=[]
        diff = diff1 + diff2
        for x in diff :
            tmp.append(x)
        out_To_File("CollationDiff_", tmp)
        summary_Report = []
        for feeder in unique_Feeder_List :
            missing_First = sum(c.split(", ")[2] == feeder for c in diff1)
            missing_Second = sum(c.split(", ")[2] == feeder for c in diff2)
            cume_Missing = abs(missing_First - missing_Second)
            summary_Report.append(feeder + " (cumulative) " + str(cume_Missing))
        out_To_File("CollationDiffSummary_", summary_Report)
        run_Flag = False

    
def out_To_File(report_Name, data) :
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")
    new_Path = os.path.join('report - output', report_Name + formatted_date + ".txt")
    output = open(new_Path , "w")
    for element in data :
        output.write(element.rstrip("\n") + "\n")
    output.close()


def compare_Client_Files_To_Collation_Files(client_objects, collation_objects) :
    list_Missing = []
    client_List = []
    collation_List = []
    match_List = []
    job_NTA_List = []
    master_Report = []
    for clfile in client_objects :
        for client in clfile :
            client_List.append(client.simple_Compare())

    for collationfile in collation_objects :
        for collation in collationfile :
            if collation.is_Sample() == False :
                collation_List.append(collation.simple_Compare())

    s = set(collation_List)
    diff = [x for x in client_List if x not in s]

    for x in diff :
        new = x.split(", ")
        if new[0] not in job_NTA_List :
            job_NTA_List.append(new[0])

    for jobnta in job_NTA_List :
        i = 0
        tmp = []
        for x in diff :
            new = x.split(", ")
            if jobnta == new[0] :
                i += 1
                tmp.append(x)
        out_To_File(jobnta + "_MISSINGFROMCOLLATION", tmp)
        report_Str = "JOBNTA: {0}, MISSING COUNT: {1}".format(jobnta, i)
        
        master_Report.append(report_Str)
        
    out_To_File("MissingReport", master_Report)

   
                

def main() :
    rescan = "1"
    while rescan == "1" :
        files = get_Collation_Address_Files()
        clfiles = get_Client_File()
        print(str(len(files)) + " collation address files identified.")
        print(str(len(clfiles)) + " client files identified.")
        rescan = raw_input("If you need to recheck for files, press 1, if not, press 2.")
        
    mode = raw_input("Please select a mode. \nPress 1 for reporting of feeder codes per Job/NTA.\nPress 2 to compare two collation address files." + 
                     "\nPress 3 to verify Tray Plan Extract.\nPress 4 to break the client file out by job/nta."+
                     "\nPress 5 to identify the missing addresses between the collation files and client files.\nPress 6 to list dupes from client file.")

    if mode == "1" :
        objects_List = create_Collation_Address_File_Objects(files)
        report_Counts(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")
    if mode == "2" :
        objects_List = create_Collation_Address_File_Objects(files)
        compare_Collation_Files(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")
    if mode == "3" :
        objects_List = create_Collation_Address_File_Objects(files)
        verify_Tray_Extract_From_Collation_Address_File(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")
    if mode == "4" :
        client_objects = create_Client_File_Objects(clfiles)
        split_By_JobNTA(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")
    if mode == "5" :
        collation_objects = create_Collation_Address_File_Objects(files)
        client_objects = create_Client_File_Objects(clfiles)
        compare_Client_Files_To_Collation_Files(client_objects, collation_objects)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")
    if mode == "6" :
        client_objects = create_Client_File_Objects(clfiles)
        list_Duplicates_From_Client_File(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO CLOSE.")


def main_Debug() :
    
    files = get_Collation_Address_Files()
    objects_List = create_Collation_Address_File_Objects(files)
    compare_Collation_Files(objects_List)
    
def run_Loop() :
    run = True
    while run == True :
        main()
        runflag = raw_input("Would you like to process more? Press 1 to run again. Press 2 to close.")

        if runflag == "1" :
            run = True
        if runflag == "2" :
            run = False

run_Loop() 
