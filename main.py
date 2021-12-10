import requests
import json
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="data_dapodik"
)

mycursor = mydb.cursor()

def dump_provinces():
    url_provinces = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=0&kode_wilayah=000000&semester_id=20211"

    page_province = requests.get(url_provinces)

    provinces = json.loads(page_province.content)

    if len(provinces) == 0:
        print("Data tidak ditemukan")
        return False
    else :        
        mycursor.execute("SELECT id,code,name,done_childs FROM provinces")
        myresult = mycursor.fetchall()
        if(len(myresult) > 0):
            return myresult;

        for index_provinsi,provinsi in enumerate(provinces):    
            if(index_provinsi < (len(provinces)-1)):
                name = provinsi["nama"][6:];
                mycursor.execute("INSERT INTO provinces SET name='"+name.strip()+"',code='"+provinsi['kode_wilayah'].strip()+"'")
                mydb.commit()
            time.sleep(1)

        print("Done Dump Province")                
        mycursor.execute("SELECT id,code,name,done_childs FROM provinces")
        myresult = mycursor.fetchall()        
        return myresult;

def dump_cites(provinsi):
    url_cites = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=1&kode_wilayah="+str(provinsi[1])+"&semester_id=20211"

    page_cites = requests.get(url_cites)

    cites = json.loads(page_cites.content)

    if len(cites) == 0:
        print("Data tidak ditemukan")
        return False
    else :
        mycursor.execute("SELECT id,code,province_id,name,done_childs FROM cites where province_id='"+str(provinsi[0])+"'")
        myresult = mycursor.fetchall()
        if(len(myresult) > 0):
            return myresult;

        for city in cites:                    
            name = city["nama"][5:];
            mycursor.execute("INSERT INTO cites SET name='"+name.strip()+"',code='"+city['kode_wilayah'].strip()+"',province_id='"+str(provinsi[0])+"'")
            mydb.commit()
            time.sleep(1)

        mycursor.execute("SELECT id,code,province_id,name,done_childs FROM cites where province_id='"+str(provinsi[0])+"'")
        myresult = mycursor.fetchall()    
        return myresult;

def dump_districts(city):
    url_districts = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah="+str(city[1])+"&semester_id=20211"

    page_districts = requests.get(url_districts)

    districts = json.loads(page_districts.content)

    if len(districts) == 0:
        print("Data tidak ditemukan")
        return False
    else :
        mycursor.execute("SELECT id,code,city_id,name,done_level_tk_childs,done_level_sd_childs,done_level_smp_childs,done_level_smk_childs,done_level_sma_childs,done_level_slb_childs FROM districts where city_id='"+str(city[0])+"'")
        myresult = mycursor.fetchall()
        if(len(myresult) > 0):
            return myresult;

        for district in districts:                    
            name = district["nama"][5:];
            mycursor.execute("INSERT INTO districts SET name='"+name.strip()+"',code='"+district['kode_wilayah'].strip()+"',city_id='"+str(city[0])+"'")
            mydb.commit()
            time.sleep(1)

        mycursor.execute("SELECT id,code,city_id,name,done_level_tk_childs,done_level_sd_childs,done_level_smp_childs,done_level_smk_childs,done_level_sma_childs,done_level_slb_childs FROM districts where city_id='"+str(city[0])+"'")
        myresult = mycursor.fetchall()        
        return myresult;

       
def dump_schools():
    pass 


while True:        
    print();
    print("--------")
    print("1.Dump Provinsi")
    print("2.Dump Kota")
    print("3.Dump Kecamatan")
    print("4.Dump Sekolah")
    print("5.Dump Semuanya")
    print("6.Keluar ")
    print("---------")
    print();

    command = str(input("Masukan Angka Perintah Angka : "))
    
    print()

    if command == "5":
        print("Jika dibirakan kosong maka isinya akan")
        print("=> https://dapo.kemdikbud.go.id/rekap/dataSekolah")        
        print("")
        cmmand_inputkan = str(input("Masukan Url : "))

        print()
        print("Jika dibiarkan kosong maka isinya akan")
        print("=> semester terakhir *contoh => (1,2)")
        command_semester = str(input("Masukan semester : "))

        print()
        print("Jika dibiarkan kosong maka isinya akan")
        print("=> tahun tearkhir *conth => (2020,2021)")
        command_tahun = str(input("Masukan tahun semester : "))

    print()

    if command == "6" :
        print("Anda Keluar Bye")
        break;
    elif command == "5" :
        print("Dump Semuanya")
        break;
    elif command == "4" :
        print("Dump Sekolah")
        break;
    elif command == "3" :
        mycursor.execute("SELECT id,code,province_id,name,done_childs FROM cites")

        # city[0] => id
        # city[1] => kode
        # city[2] => province_id
        # city[3] => name
        # city[4] => done_childs

        for city in mycursor.fetchall():      
            if(int(city[4]) == 1) :
                print(city[0])
                continue;       

            mycursor.execute("DELETE FROM districts WHERE city_id='"+str(city[0])+"'")
            mydb.commit()
            time.sleep(1)

            dump_districts(city)

            time.sleep(3)

            mycursor.execute("UPDATE cites SET done_childs=1 where id='"+str(city[0])+"'")

            print("Done "+city[3])
            
        print("Dump Kecamatan")
        break;
    elif command == "2" :
        provinces = dump_provinces()

        # provinsi[0] => id
        # provinsi[1] => kode
        # provinsi[2] => name
        # provinsi[3] => done_childs

        for provinsi in provinces:      
            if(int(provinsi[3]) == 1) :
                print(provinsi[0])
                continue;       
        
            mycursor.execute("DELETE FROM cites WHERE provinsi_id='"+str(provinsi[0])+"'")
            mydb.commit()
            time.sleep(1)

            dump_cites(provinsi)

            time.sleep(3)

            mycursor.execute("UPDATE provinces SET done_childs=1 where id='"+str(provinsi[0])+"'")

            print("Done "+provinsi[2])
                
        print("Dump Kota")
        break;
    elif command == "1" : 
        dump_provinces()
        print("Dump Provinsi Selesai")
        break;

# url = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=1&kode_wilayah=050000&semester_id=20211"

#from bs4 import BeautifulSoup

# results = soup.find(id="box-table-a")
# print(results.prettify())

# def get_provinsi():        
#     url = "https://dapo.kemdikbud.go.id/sp"

#     provinsi_page = requests.get(url)

#     time.sleep(10)

#     soup = BeautifulSoup(provinsi_page.content, "html.parser")

#     # get table
#     table_results = soup.find("table")
#     print(table_results)
#     # get tbody
#     # tbody_results = table_results.find("tbody");

#     # get list provinsi
#     # tr_results = tbody_results.find_all("tr");

#     # foreach list provinsi
#     # for index_tr,tr in enumerate(tr_results):

#     #     # find all td
#     #     td_results = tr.find_all("td")
        
#     #     # foreach list td
#     #     for index_td,td in enumerate(td_results):
#     #     # get link 1 td
#     #         if(index_td == 1):
#     #             ps = td.find("a");
#     #             if(ps != None) :
#     #                 first_code = ps["href"][17:];
#     #                 last_code = first_code[:6]                            
#     #                 # get_kabpuaten(last_code)
#     #                 # pass
#     #                 # print(ps["href"])
#     #             print(td.get_text())    
#     #     time.sleep(2)
#     # time.sleep(3)

# def get_kabpuaten(kode):
#     url = "https://referensi.data.kemdikbud.go.id/index11.php?kode="+kode+"&level=1"

#     provinsi_page = requests.get(url)

#     soup = BeautifulSoup(provinsi_page.content, "html.parser")
#     # get tbody
#     tbody_results = soup.find("tbody");
#     # foreach list provinsi
#     tr_results = tbody_results.find_all("tr");
#     for index_tr,tr in enumerate(tr_results):

#         # find all td
#         td_results = tr.find_all("td")
        
#         # foreach list td
#         for index_td,td in enumerate(td_results):
#         # get link 1 td
#             if(index_td == 1):
#                 ps = td.find("a");
#                 if(ps != None) :
#                     first_code = ps["href"][17:];
#                     last_code = first_code[:6]                            
#                     get_kecamatan(last_code)
#                     # get_kabpuaten()
#                     # pass
#                     # print(ps["href"])
#                 print(td.get_text())    
#         time.sleep(2)
#     time.sleep(3)

# def get_kecamatan(kode):
#     url = "https://referensi.data.kemdikbud.go.id/index11.php?kode="+kode+"&level=2"

#     provinsi_page = requests.get(url)

#     soup = BeautifulSoup(provinsi_page.content, "html.parser")
#     # get tbody
#     tbody_results = soup.find("tbody");
#     # foreach list provinsi
#     tr_results = tbody_results.find_all("tr");
#     for index_tr,tr in enumerate(tr_results):

#         # find all td
#         td_results = tr.find_all("td")
        
#         # foreach list td
#         for index_td,td in enumerate(td_results):
#         # get link 1 td
#             if(index_td == 1):
#                 ps = td.find("a");
#                 if(ps != None) :
#                     first_code = ps["href"][17:];
#                     last_code = first_code[:6]                            
#                     get_sekolah(last_code)
#                     # get_kabpuaten()
#                     # pass
#                     # print(ps["href"])
#                 print(td.get_text())    
#         time.sleep(2)
#     time.sleep(3)

# def get_sekolah(kode):
#     print(kode)
#     url = "https://referensi.data.kemdikbud.go.id/index11.php?kode="+kode+"&level=3"

#     provinsi_page = requests.get(url)

#     soup = BeautifulSoup(provinsi_page.content, "html.parser")

#     aps = soup.find("table",{
#         "cellpadding" : 0,
#         "cellspacing" : 0,
#         "border" : 0,
#         "class" : "display",
#         "id" : "example"
#     })

#     print(aps.prettify())
#     # get tbody    
#     # tbody_results = soup.find("tbody",{"role" : "alert","area-live": "polite","aria-relevant": "all"});
#     # print(tbody_results)
#     # foreach list provinsi
#     # tr_results = tbody_results.find_all("tr");
#     # for index_tr,tr in enumerate(tr_results):

#     #     # find all td
#     #     td_results = tr.find_all("td")
        
#     #     # foreach list td
#     #     for index_td,td in enumerate(td_results):
#     #     # get link 1 td
#     #         if(index_td == 1):
#     #             # ps = td.find("a");
#     #             # if(ps != None) :
#     #             #     first_code = ps["href"][17:];
#     #             #     last_code = first_code[:6]                            
#     #                 # get_sekolah(last_code)
#     #                 # get_kabpuaten()
#     #                 # pass
#     #                 # print(ps["href"])
#     #             print(td.get_text())    
#     #     time.sleep(2)
#     # time.sleep(3)


# get_provinsi()