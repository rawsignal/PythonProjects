import os
import sys
import datetime

class Canada_Data_Base(object) :
    def __init__(self, province_code, postal_deliv_area_nm, deliv_inst_area_nm, deliv_inst_type_desc, deliv_inst_qual_nm, record_type_code) :
        self.province_code = province_code
        self.postal_deliv_area_nm = postal_deliv_area_nm
        self.deliv_inst_area_nm = deliv_inst_area_nm
        self.deliv_inst_type_desc = deliv_inst_type_desc
        self.deliv_inst_qual_nm = deliv_inst_qual_nm
        self.record_type_code = record_type_code

    def get_Province_Code(self) :
        return self.province_code

    def get_Postal_Deliv_Area_Name(self) :
        return self.postal_deliv_area_nm

    def get_Deliv_Inst_Area_Name(self) :
        return self.deliv_inst_area_nm

    def get_Deliv_Inst_Type_Desc(self) :
        return self.deliv_inst_type_desc

    def get_Deliv_Inst_Qual_Nm(self) :
        return self.deliv_inst_qual_nm


class Delivery_Installation_Address(Canada_Data_Base) :
    def __init__(self, province_code, postal_deliv_area_nm, deliv_inst_area_nm, deliv_inst_type_desc, deliv_inst_qual_nm, record_type_code,
                 deliv_inst_postal_code, street_address_num, street_address_num_suff, street_name, street_type_code, street_direction_code, suite_num,
                 deliv_inst_tele) :
        Canada_Data_Base.__init__(self, province_code, postal_deliv_area_nm, deliv_inst_area_nm, deliv_inst_type_desc, deliv_inst_qual_nm, record_type_code)
        self.deliv_inst_postal_code = deliv_inst_postal_code
        self.street_address_num = street_address_num
        self.street_address_num_suff = street_address_num_suff
        self.street_name = street_name
        self.street_type_code = street_type_code
        self.street_direction_code = street_direction_code
        self.suite_num = suite_num
        self.deliv_inst_tele = deliv_inst_tele

    def get_Province_Code(self) :
        return self.province_code
    
    def get_Deliv_Inst_Postal_Code(self) :
        return self.deliv_inst_postal_code

    def get_Street_Address_Num(self) :
        return self.street_address_num

    def get_Street_Address_Num_Suff(self):
        return self.street_address_num_suff

    def get_Street_Name(self) :
        return self.street_name

    def get_Type(self) :
        return "INSTALLATION"

    def get_Record_Type_Code(self) :
        return self.record_type_code

    def easy_Compare(self) :
        return "{0},{1}".format(self.province_code, self.deliv_inst_postal_code)

    def get_Str_Out(self) :
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format(self.province_code, self.postal_deliv_area_nm, self.deliv_inst_area_nm, self.deliv_inst_type_desc,
                                                                     self.record_type_code, self.street_address_num, self.street_address_num_suff, self.street_name,
                                                                     self.street_type_code, self.street_direction_code, self.suite_num, self.deliv_inst_tele)

class Demographic_Data(Canada_Data_Base) :
    def __init__(self, province_code, postal_deliv_area_nm, deliv_inst_area_nm, deliv_inst_type_desc, deliv_inst_qual_nm, record_type_code,
                 deliv_mode_type, deliv_mode_ident, deliv_inst_abb_nm, deliv_inst_postal_code, fsa_code, apartment_count, business_count,
                 farm_count, house_count, split_fsa_ind, split_deliv_ind, apartment_ttl_poc_count, business_ttl_poc_count, farm_ttl_poc_count, house_ttl_poc_count) :
        Canada_Data_Base.__init__(self, province_code, postal_deliv_area_nm, deliv_inst_area_nm, deliv_inst_type_desc, deliv_inst_qual_nm, record_type_code)
        self.deliv_mode_type = deliv_mode_type
        self.deliv_mode_ident = deliv_mode_ident
        self.deliv_inst_abb_nm = deliv_inst_abb_nm
        self.deliv_inst_postal_code = deliv_inst_postal_code
        self.fsa_code = fsa_code
        self.apartment_count = apartment_count
        self.business_count = business_count
        self.farm_count = farm_count
        self.house_count = house_count
        self.split_fsa_ind = split_fsa_ind
        self.split_deliv_ind = split_deliv_ind
        self.apartment_ttl_poc_count = apartment_ttl_poc_count
        self.business_ttl_poc_count = business_ttl_poc_count
        self.farm_ttl_poc_count = farm_ttl_poc_count
        self.house_ttl_poc_count = house_ttl_poc_count

    def get_FSA_Code(self) :
        return self.fsa_code

    def get_Apartment_Count(self) :
        return self.apartment_count

    def get_Business_Count (self) :
        return self.business_count

    def get_House_Count (self) :
        return self.house_count

    def get_Farm_Count (self) :
        return self.farm_count

    def get_Type(self) :
        return "DEMOGRAPHIC"

    def get_Record_Type_Code(self) :
        return self.record_type_code

def get_Canada_File() :
    directory = 'Canada HH File Input'
    list_File = os.listdir(directory)
    return directory + "\\" + list_File[0]

def create_Canada_Data_Objects(canada_file) :
    file_Tmp = open(canada_file, "r")
    objs = []
    for record in file_Tmp :
        province_code = record[0:2]
        postal_delivery_area_name = record[2:30]
        delivery_installation_area_name = record[32:62]
        delivery_installation_type_description = record[62:67]
        delivery_installation_qualifier_name = record[67:82]
        record_type_code = record[82]
        if record_type_code == "1" or record_type_code == "3" :
            delivery_install_postal_code = record[104:110]
            street_address_num = record[110:116]
            street_address_num_suffix_code = record[116]
            street_name = record[117:147]
            street_type_code = record[147:153]
            street_direction_code = record[153:154]
            suite_number = record[155:161]
            delivery_install_tele_number = record[161:171]
            objs.append(Delivery_Installation_Address(province_code, postal_delivery_area_name,
                                                      delivery_installation_area_name,
                                                      delivery_installation_type_description,
                                                      delivery_installation_qualifier_name,
                                                      record_type_code, delivery_install_postal_code,
                                                      street_address_num, street_address_num_suffix_code,
                                                      street_name, street_type_code, street_direction_code, suite_number,
                                                      delivery_install_tele_number))

        if record_type_code == "2" or record_type_code == "4" :
            delivery_mode_type = record[83]
            delivery_mode_identifier = record[84:86]
            delivery_ins_abbreviated_name = record[86:89]
            delivery_ins_postal_code = record[89:104]
            fsa_code = record[110:113]
            apartment_count = record[113:120]
            business_count = record[120:127]
            farm_count = record[127:134]
            house_count = record[134:141]
            split_fsa_ind = record[141]
            split_demo_ind = record[142]
            apartment_poc = record[143:150]
            business_poc = record[150:157]
            farm_poc = record[157:164]
            house_poc = record[164:171]
            objs.append(Demographic_Data(province_code, postal_delivery_area_name,
                                         delivery_installation_area_name,
                                         delivery_installation_type_description,
                                         delivery_installation_qualifier_name,
                                         record_type_code, delivery_mode_type, delivery_mode_identifier,
                                         delivery_ins_abbreviated_name, delivery_ins_postal_code, fsa_code,
                                         int(apartment_count), int(business_count), int(farm_count), int(house_count),
                                         split_fsa_ind, split_demo_ind, apartment_poc, business_poc,
                                         farm_poc, house_poc))
    #del objs[0]

    return objs

def report_Counts(canada_objects) :
    instl = []
    demos = sum(a.get_Type() == "DEMOGRAPHIC" for a in canada_objects)
    for item in canada_objects :
        if item.get_Type() == 'INSTALLATION' and item.easy_Compare() not in instl:
            instl.append(item.easy_Compare())

    installations = len(instl)

    report_details = []

    report_details.append("DEMOGRAPHIC RECORD COUNT: " + str(demos))
    report_details.append("INSTALLATIONS RECORD COUNT: " + str(installations))


    demo_hh_count = sum(a.get_House_Count() for a in canada_objects if a.get_Type() == "DEMOGRAPHIC")
    demo_apartment_count = sum(a.get_Apartment_Count() for a in canada_objects if a.get_Type() == "DEMOGRAPHIC")
    demo_business_count = sum(a.get_Business_Count() for a in canada_objects if a.get_Type() == "DEMOGRAPHIC")
    demo_farm_count = sum(a.get_Farm_Count() for a in canada_objects if a.get_Type() == "DEMOGRAPHIC")

    report_details.append("Houses: " + str(demo_hh_count))
    report_details.append("Apartments: " + str(demo_apartment_count))
    report_details.append("Businesses: " + str(demo_business_count))
    report_details.append("Farms: " + str(demo_farm_count))

    province_list = set(a.get_Province_Code() for a in canada_objects if a.get_Type() == "INSTALLATION")

    for province in province_list :
        report_details.append(province + " " + str(sum(a.get_Province_Code() == province for a in canada_objects if a.get_Type() == "INSTALLATION")))

    test_list = [a.get_Str_Out() for a in canada_objects if a.get_Type() == "INSTALLATION" and a.get_Province_Code() == "NB"]
    
    installation_list = [a.get_Str_Out() for a in canada_objects if a.get_Type() == "INSTALLATION"]
    out_To_File("Installations", installation_list)
    out_To_File("NB", test_list)
    out_To_File("Summary", report_details)

def out_To_File(report_Name, data, ext=".txt", subpath="") :
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")
    prepath = 'Reports'
    final_path = prepath + subpath
    if not os.path.exists(final_path) :
        os.makedirs(final_path)
    new_Path = os.path.join(final_path, report_Name + formatted_date + ext)
    output = open(new_Path , "w")
    for element in data :
        output.write(element.rstrip("\n") + "\n")
    output.close()            

canada_file = get_Canada_File()
all_can = create_Canada_Data_Objects(canada_file)
report_Counts(all_can)
        
    
