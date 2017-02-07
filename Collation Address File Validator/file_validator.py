import os
import sys
import sybpydb as sybase
import datetime
from collections import Counter
from collections import OrderedDict

db_UN = 'gisuser'
db_PW = 'bng67f'
db_SN = 'ctmtst'


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

    def get_zip4(self) :
        zip4cut = self.add_ln_5.rstrip(" ")
        zip4 = zip4cut[-10:]
        return zip4

    def is_Sample(self) :
        is_Sample = False
        if 'QC' in self.add_ln_2 or 'Samples' in self.add_ln_1 or self.tray_serial_num == '00000000' :
            is_Sample = True

        return is_Sample

    def tray_Dict(self) :
        return {self.get_Job_NTA():self.get_Tray_SN()}

    def client_Out_Format(self) :
        return "{0}	{1}	{2}	{3}".format(self.get_Address(), self.get_zip4(), self.get_Job_NTA(), self.get_Feeder_Code())

    def simple_Compare(self) :
        return "{0}, {1}".format(self.get_Job_NTA(), self.get_Address())


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
        return "{0}, {1}".format(self.get_Job_NTA(), self.get_Address())
    
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
        if files == "CORE_FTP.LOG" :
            os.remove(os.path.join('collation address files', files))
        else :
            returned_List.append(os.path.join('collation address files', files))

    return returned_List

def get_Client_File() :
    # This will simply return the first file it finds. The logic is not built to handle more than one client file at a time for this test.
    returned_List = []
    list_Files = os.listdir('client files')
        
    for files in list_Files :
        if files == "CORE_FTP.LOG" :
            os.remove(os.path.join('client files', files))
        else :
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
    x = 1
    for clfile in client_objects :
        x = 1
        job_NTA_List = []
        unique_Feeder_List = []
        summary_Report = []
        verify_Query = []
        for item in clfile :
            if item.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(item.get_Job_NTA())
            if item.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(item.get_Feeder_Code())
        file_name_start = client_file_list[i].rstrip(".TXT").rstrip(".txt").replace("client files\\", "")
        
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
            file_name = "{0}_ClientFile".format(file_name_start)
            out_To_File(file_name, tmp, subpath="\\Program Generated Client Files - {0}".format(file_name_start))
            x = get_Status(100.0, len(job_NTA_List), x)
            verify_Query.append('select * from selectiveinsert where job_id = {0} and nta = "{1}"'.format(jobnta[0:6], jobnta[6:]))

        out_To_File("Client_File_{0}_JobNTA_Summary".format(file_name_start), summary_Report)
        out_To_File("Verify_Query_{0}".format(file_name_start), verify_Query)
        i += 1

def generate_Clean_Client_File(client_objects, client_file_list) :
    i = 0
    x = 1
    output = []
    for clfile in client_objects :
        for item in clfile :
            output.append(str(item))
            x = get_Status(100.0, len(clfile), x)
        file_name_start = client_file_list[i].rstrip(".TXT").rstrip(".txt").replace("client files\\", "")
        file_name = "{0}_ClientFile".format(file_name_start)
        out_To_File(file_name, output, subpath="\\Rebuilt Client File - {0}".format(file_name_start))
        i += 1


def get_Counts_For_SAP(client_objects, client_file_list) :
    i = 0
    for clfile in client_objects :
        unique_Feeder_List = []
        for item in clfile :
            if item.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(item.get_Feeder_Code())
        job_NTA_List = []
        summary_Report = []
        for item in clfile :
            if item.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(item.get_Job_NTA())
        file_name_start = client_file_list[i].rstrip(".TXT").rstrip(".txt").replace("client files\\", "")
        x = 1
        for jobnta in job_NTA_List :
            tmp = []
            gttl = 0
            for feeder in unique_Feeder_List :
                ttl = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta for c in client_objects for a in c)
                gttl += ttl
                report_str = "{0}	{1}	{2}	{3}".format(feeder, "J" + jobnta[0:6], jobnta[6:], ttl)
                summary_Report.append(report_str)
            
            x = get_Status(100.0, len(job_NTA_List), x)

        out_To_File("Client_File_{0}_JobNTA_Summary".format(file_name_start), summary_Report, ".xls")
        i += 1

def get_Status(start, end, i) :
	if end < i :
		return "Processing Complete!"
	else:
		status = start/end * i
		sys.stdout.write("\r")
		sys.stdout.write("{0:.1f}% complete.".format(status))
		sys.stdout.flush()
		i+=1
		return i

def get_Counts_For_All(client_objects) :
    i = 1
    for clfile in client_objects :
        
        unique_Feeder_List = []
        for item in clfile :
            if item.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(item.get_Feeder_Code())
                
        summary_Report = ["BATCH NUMBER	FEEDER CODE	TOTAL"]
        
        
        tmp = []
        gttl = 0
        for feeder in unique_Feeder_List :
            ttl = sum(a.get_Feeder_Code() == feeder for c in client_objects for a in c)
            gttl += ttl
            report_str = "{0}	{1}".format(feeder, ttl)
            summary_Report.append(report_str)
            
        i = get_Status(100.0, len(client_objects), i)
        
    out_To_File("AllMailDates", summary_Report, ".xls")
    


def list_Duplicates_From_Client_File(client_objects, client_file_list) :
    
    i = 0
    x = 1
    y = 1
    print("Building list. Please wait.")  
    for clfile in client_objects :
        simple_No_Feeder = []
        for item in clfile :
            simple_No_Feeder.append(item.simple_Compare_NF())
            x = get_Status(100.0, len(clfile), x)
        tmp = [k for k, v in Counter(simple_No_Feeder).items() if v>1]
        
        out_To_File("WARN_TMP", tmp)
        dupes = []
        output_List = []
        file_name_start = client_file_list[i].rstrip(".TXT").rstrip(".txt").replace("client files\\", "")
        print(" List built. Checking dupes...")
        update_Flag = raw_input("Do you need to update the dupe records on file: {0}? Type yes or no and hit enter. ".format(file_name_start))
        if update_Flag == "yes" :
            update_To = raw_input("What do you want the new feeder code to be? ")
        
        for x in clfile :
            if x.simple_Compare_NF() in tmp :
                dupes.append(x.export_Format())
                if update_Flag == "yes" :
                    x.set_Feeder_Code(update_To)
            output_List.append(x.export_Format())
            y = get_Status(100.0, len(clfile), y)


        out_To_File(file_name_start + "_DuplicateAddressInClientFile", dupes)
        print("File {0} processed...".format(file_name_start)) 
        if update_Flag == "yes" :
            out_To_File(file_name_start + "_updated", output_List, subpath="\\{0} Dupes Updated Client File".format(file_name_start))
        i += 1
        
def report_Counts(collation_Objects) :

    output = []
    i = 1
    print("Please wait. This could take some time when there are many collation address files. Processing...")
    for collationfile in collation_Objects :
        unique_Feeder_List = []
        job_NTA_List = []
        for address in collationfile :
            if address.get_Feeder_Code() not in unique_Feeder_List :
                unique_Feeder_List.append(address.get_Feeder_Code())
            if address.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(address.get_Job_NTA())

    
        for jobnta in job_NTA_List :
            for feeder in unique_Feeder_List :
                ttl_WO_Samples = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta and a.is_Sample() == False for c in collation_Objects for a in c)
                ttl_Sampls = sum(a.get_Feeder_Code() == feeder and a.get_Job_NTA() == jobnta for c in collation_Objects for a in c) - ttl_WO_Samples
                feeder_Report = ""
                if len(feeder) > 2 :  
                    feeder_Report = feeder_Decode_Internal(feeder, basic = True)
                report_String = "{0}, {1}, {2}, {3}".format(jobnta, feeder, ttl_WO_Samples, ttl_Sampls)
                output.append(report_String)
                output.append(feeder_Report)

        i = get_Status(100.0, len(collation_Objects), i)
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

def create_Collation_Address_File_Objects_For_Client_File_Creation(collation_Add_File_List) :
    
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
                                          "offer1", machine_id, imb_code))
        list_of_objs.append(objs)
        
        file_Tmp.close()
        

    return list_of_objs

def verify_Tray_Extract_From_Collation_Address_File(collation_Objects) :
    job_NTA_List = []
    tray_Objects_List = []
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")

    for clfile in collation_Objects :
        for address in clfile :
            if address.get_Job_NTA() not in job_NTA_List :
                job_NTA_List.append(address.get_Job_NTA())
        
    i = 1
    for jobnta in job_NTA_List :
        tray_Serial_List = []
        output = []
        for clfile in collation_Objects :
            for address in clfile :
                if address.get_Job_NTA() == jobnta and address.get_Tray_SN() not in tray_Serial_List :
                    tray_Serial_List.append(address.get_Tray_SN())
        for tray in tray_Serial_List :
            ttl = sum(a.get_Tray_SN() == tray for c in collation_Objects for a in c)
            report_String = "{0}, {1}, {2}".format(jobnta, tray, ttl)
            output.append(report_String)

        i = get_Status(100.0, len(job_NTA_List), i)
        out_To_File("TrayExtractReport_{0}".format(jobnta), output, subpath="\\Tray Extract Reports{0}".format(formatted_date))

    

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

    
def out_To_File(report_Name, data, ext=".txt", subpath="") :
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")
    prepath = 'report - output'
    final_path = prepath + subpath
    if not os.path.exists(final_path) :
        os.makedirs(final_path)
    new_Path = os.path.join(final_path, report_Name + formatted_date + ext)
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
        out_To_File(jobnta + "_MISSINGFROMCOLLATION", tmp, subpath="\\Missing Addresses in Collation Files - Detail Reports")
        report_Str = "JOBNTA: {0}, MISSING COUNT: {1}".format(jobnta, i)
        
        master_Report.append(report_Str)
        
    out_To_File("MissingReport", master_Report)

        
    
def feeder_Simulator() :
    run_Flag = True
    while run_Flag == True :
        off_Feeders = raw_input("Type the feeder ID's that you want OFF, seperated by commas. ")
        off_Feeder_List = off_Feeders.replace(" ", "").split(",")

        group1 = OrderedDict([("SIG4", 1), ("SIG3", 1), ("SIG2", 1), ("SIG1", 1)])
        group2 = OrderedDict([("4", 1), ("3", 1), ("2", 1), ("1", 1)])
        group3 = OrderedDict([("8", 1), ("7", 1), ("6", 1), ("5", 1)])
        group4 = OrderedDict([("12", 1), ("11", 1), ("10", 1), ("9", 1)])
        group5 = OrderedDict([("16", 1), ("15", 1), ("14", 1), ("13", 1)])
        group6 = OrderedDict([("20", 1), ("19", 1), ("18", 1), ("17", 1)])
        group7 = OrderedDict([("24", 1), ("23", 1), ("22", 1), ("21", 1)])
        group8 = OrderedDict([("NB", 1), ("NA", 1), ("PR2", 1), ("PR1", 1)])

        collator = [group1, group2, group3, group4, group5, group6, group7, group8]
        
        for x in off_Feeder_List :
            for i, item in enumerate(collator) :
                if x in collator[i] :
                    collator[i][x] = 0

        groupings = []

        for x in collator :
            tmp = ""
            for key, value in x.items() :
                tmp += str(value)
            groupings.append(tmp)

        feeder = ""
        for x in groupings :
            feeder += chr(int(x,2)+65)

        print(feeder)
        
        run_Check = raw_input("Press 1 to end. Press 2 to simulate another, or press enter.")
        if run_Check == "1" :
            run_Flag = False

def feeder_Decode_Internal(feeder_Code, basic = False) :
    run_Flag = True
    group1 = OrderedDict([("SIG4", 1), ("SIG3", 1), ("SIG2", 1), ("SIG1", 1)])
    group2 = OrderedDict([("4", 1), ("3", 1), ("2", 1), ("1", 1)])
    group3 = OrderedDict([("8", 1), ("7", 1), ("6", 1), ("5", 1)])
    group4 = OrderedDict([("12", 1), ("11", 1), ("10", 1), ("9", 1)])
    group5 = OrderedDict([("16", 1), ("15", 1), ("14", 1), ("13", 1)])
    group6 = OrderedDict([("20", 1), ("19", 1), ("18", 1), ("17", 1)])
    group7 = OrderedDict([("24", 1), ("23", 1), ("22", 1), ("21", 1)])
    group8 = OrderedDict([("NOTEXIST2", 1), ("NOTEXIST1", 1), ("PR2", 1), ("PR1", 1)])

    collator = [group1, group2, group3, group4, group5, group6, group7, group8]
    
    while run_Flag == True :
        
        groupings = []
        for x in feeder_Code :
            group_Val = format(ord(x)-65, 'b')
            
            if len(group_Val) < 4 :
                missing = 4 - len(group_Val)
                tmp = "0"*missing + group_Val
                group_Val = tmp
            groupings.append(group_Val)
        print(groupings)   
        for i, group in enumerate(groupings) :
            y = 0
            for key, value in collator[i].items() :
                
                collator[i][key] = int(group[y])
                y+=1

        report_String = ""

        if basic == False: 
            for x in collator :
                for key, value in x.items() :
                    if value == 1 :
                        value = "ON"
                    if value == 0 :
                        value = "OFF"
                    report_String += "FEEDER ID: {0}, STATE: {1}\n".format(key, value)
        if basic == True :
            for x in collator :
                for key, value in x.items() :
                    if value == 1 :
                        value = "ON"
                    if value == 0 :
                        value = "OFF"
                    if value == "OFF" :
                        report_String += "FEEDER ID: {0}, STATE: {1}\n".format(key, value)
                

        return report_String
        run_Flag = False 

def feeder_Decode() :
    run_Flag = True
    while run_Flag == True :
        feeder_Code = raw_input("Type the feeder code to find the feeders that are OFF. ")
        print(feeder_Decode_Internal(feeder_Code))

        run_Check = raw_input("Press 1 to end. Press 2 to simulate another, or press enter.")
        if run_Check == "1" :
            run_Flag = False

def create_Mock_Client_File_From_Collation_Addr_File(collation_objects) :
    output = []
    i = 1
    for collationfile in collation_objects :
        for address in collationfile :
            if address.is_Sample() == False :
                output.append(address.client_Out_Format())

        i = get_Status(100.0, len(collation_objects), i)
    out_To_File("MockClientFile", output)
        

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
                     "\nPress 5 to identify the missing addresses between the collation files and client files.\nPress 6 to list dupes from client file." +
                     "\nPress 7 to get the counts for SAP. "+
                     "\nPress 8 to get the counts for All Mail Dates in Client File Directory." +
                     "\nPress 9 to generate a clean client file. " +
                     "\nPress 10 to enter Feeder Code Simulation Mode. " +
                     "\nPress 11 to enter Feeder Code Decode Mode. ")

    if mode == "1" :
        objects_List = create_Collation_Address_File_Objects(files)
        report_Counts(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "2" :
        objects_List = create_Collation_Address_File_Objects(files)
        compare_Collation_Files(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "3" :
        objects_List = create_Collation_Address_File_Objects(files)
        verify_Tray_Extract_From_Collation_Address_File(objects_List)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "4" :
        client_objects = create_Client_File_Objects(clfiles)
        split_By_JobNTA(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "5" :
        collation_objects = create_Collation_Address_File_Objects(files)
        client_objects = create_Client_File_Objects(clfiles)
        compare_Client_Files_To_Collation_Files(client_objects, collation_objects)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "6" :
        client_objects = create_Client_File_Objects(clfiles)
        list_Duplicates_From_Client_File(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "7" :
        client_objects = create_Client_File_Objects(clfiles)
        get_Counts_For_SAP(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "8" :
        client_objects = create_Client_File_Objects(clfiles)
        get_Counts_For_All(client_objects)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "9" :
        client_objects = create_Client_File_Objects(clfiles)
        generate_Clean_Client_File(client_objects, clfiles)
        raw_input("PROCESSING COMPLETE. PRESS ANY KEY TO PROCEED.")
    if mode == "10" :
        print("Entering feeder simulation mode. This will allow you to generate a list of expected feeder codes based on unused feeders.")
        feeder_Simulator()
    if mode == "11" :
        print("Entering feeder decode mode.")
        feeder_Decode()
    if mode == "12" :
        client_objects = create_Collation_Address_File_Objects_For_Client_File_Creation(files)
        create_Mock_Client_File_From_Collation_Addr_File(client_objects)

def main_Debug() :
    
    files = get_Collation_Address_Files()
    objects_List = create_Collation_Address_File_Objects(files)
    verify_Tray_Extract_From_Collation_Address_File_tst(objects_List)
    
def run_Loop() :
    run = True
    while run == True :
        main()
        runflag = raw_input("Would you like to process more? Press 2 to run again. Press 1 to close.")

        if runflag == "2" :
            run = True
        if runflag == "1" :
            run = False

run_Loop() 
