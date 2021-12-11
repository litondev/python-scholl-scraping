import database
import time 
import requests
import json

def provinces():
    try:
        id_level_wilayah = "0"
        kode_wilayah = "000000"
        year = "2020"
        semester_id = "1"        
    
        url_provinces = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=" + str(id_level_wilayah) + "&kode_wilayah=" + str(kode_wilayah) + "&semester_id=" + str(year) +""+ str(semester_id);

        print(url_provinces);

        print("Request Send")

        page_province = requests.get(url_provinces,timeout=10)

        print("Get Json")

        provinces_data = json.loads(page_province.content)

        print("Done Get Json")

        if len(provinces_data) == 0:
            print("Data tidak ditemukan")
            
            return False
        else :        
            print("Process Dump")

            for index_provinsi,provinsi in enumerate(provinces_data):    
                database.mycursor.execute("SELECT id FROM provinces where code='"+provinsi['kode_wilayah'].strip()+"'")
                myresult = database.mycursor.fetchall()
                if(len(myresult) > 0):
                    continue;

                if(index_provinsi < (len(provinces_data)-1)):
                    name = provinsi["nama"][6:];
                    database.mycursor.execute("INSERT INTO provinces SET name='"+name.strip()+"',code='"+provinsi['kode_wilayah'].strip()+"'")
                    database.mydb.commit()
                
                time.sleep(1)

            print("Done Dump")                
            return True

    except Exception as e:
        print()
        print("Terjadi Kesalahan => ")
        print(e)
        print()
        print("Dump Will Repeat Again After 30 Seconds . . .")
        time.sleep(10)
        print("Start Repeat Again")
        print()
        provinces()


def cites(provinsi):
    try:
        id_level_wilayah = "1"
        kode_wilayah = provinsi[1]
        year = "2020"
        semester_id = "1"   

        url_cites = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=" + str(id_level_wilayah) + "&kode_wilayah=" + str(kode_wilayah) + "&semester_id=" + str(year) +""+ str(semester_id);

        print(url_cites);

        print("Request Send")

        page_cites = requests.get(url_cites,timeout=10)

        print(page_cites.content)

        print("Get Json")

        cites_data = json.loads(page_cites.content)

        print("Done Get Json")

        if len(cites_data) == 0:
            print("Data tidak ditemukan")

            return False
        else :
            print("Process Dump")         

            for city in cites_data:     
                database.mycursor.execute("SELECT id FROM cites where code='"+city['kode_wilayah'].strip()+"'")
                myresult = database.mycursor.fetchall()
                if(len(myresult) > 0):
                    continue;

                name = city["nama"][5:];
                is_city = city["nama"][3::-1][::-1].strip();
                if is_city == "Kota" or is_city == "KOTA" or is_city == "kota":
                    database.mycursor.execute("INSERT INTO cites SET name='"+name.strip()+"',code='"+city['kode_wilayah'].strip()+"',is_city=1,province_id='"+str(provinsi[0])+"'")
                else :
                    database.mycursor.execute("INSERT INTO cites SET name='"+name.strip()+"',code='"+city['kode_wilayah'].strip()+"',province_id='"+str(provinsi[0])+"'")
                database.mydb.commit()
                time.sleep(1)

            print("Done Dump")                
            return True
        
    except Exception as e:
        print()
        print("Terjadi Kesalahan => ")
        print(e)
        print()
        print("Dump Will Repeat Again After 30 Seconds . . .")
        time.sleep(10)
        print("Start Repeat Again")
        print()
        cites(provinsi)

def districts(city):
    try:
        id_level_wilayah = "2"
        kode_wilayah = city[1]
        year = "2020"
        semester_id = "1"   

        url_districts = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=" + str(id_level_wilayah) + "&kode_wilayah=" + str(kode_wilayah) + "&semester_id=" + str(year) +""+ str(semester_id);

        print(url_districts);

        print("Request Send")

        page_districts = requests.get(url_districts,timeout=10)

        print(page_districts.content)

        print("Get Json")    

        districts_data = json.loads(page_districts.content)

        print("Done Get Json")

        if len(districts_data) == 0:
            print("Data tidak ditemukan")

            return False
        else :    
            print("Process Dump")         
                    
            for district in districts_data:    
                database.mycursor.execute("SELECT id FROM districts where code='"+district['kode_wilayah'].strip()+"'")
                myresult = database.mycursor.fetchall()
                if(len(myresult) > 0):
                    continue;             

                name = district["nama"][5:];
                database.mycursor.execute("INSERT INTO districts SET name='"+name.strip()+"',code='"+district['kode_wilayah'].strip()+"',city_id='"+str(city[0])+"'")
                database.mydb.commit()
                time.sleep(1)

            print("Done Dump")                
            return True
    except Exception as e:
        print()
        print("Terjadi Kesalahan => ")
        print(e)
        print()
        print("Dump Will Repeat Again After 30 Seconds . . .")
        time.sleep(10)
        print("Start Repeat Again")
        print()
        districts(city)
       
# def dump_schools():
#     pass 