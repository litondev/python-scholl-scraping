import dump 
import database
import time 

def cites():
    try:
        database.mycursor.execute("SELECT id,code,name,done_childs FROM provinces")

        # provinsi[0] => id
        # provinsi[1] => kode
        # provinsi[2] => name
        # provinsi[3] => done_childs

        is_success = True 

        for provinsi in database.mycursor.fetchall():      
            if(int(provinsi[3]) == 1) :
                print(provinsi[0])
                continue;   

            database.mycursor.execute("DELETE FROM cites WHERE province_id='"+str(provinsi[0])+"'")
            database.mydb.commit()            
            time.sleep(1)

            is_done = dump.cites(provinsi)

            if is_done == True :
                print("Success Dump Cites : "+provinsi[2])
                database.mycursor.execute("UPDATE provinces SET done_childs=1 where id='"+str(provinsi[0])+"'")
                database.mydb.commit()            
                time.sleep(3)
            else :
                print("Failed Dump Cites : "+provinsi[2])                 
                is_success = False
                break;  
        
        return is_success

    except Exception as e:
        print()
        print("Terjadi Kesalahan => ")
        print(e)
        print()
        print("Get Will Repeat Again After 30 Seconds . . .")
        time.sleep(30)
        print("Start Repeat Again")
        print()
        cites()

def districts():
    try:
        database.mycursor.execute("SELECT id,code,province_id,name,done_childs FROM cites")

        # city[0] => id
        # city[1] => kode
        # city[2] => province_id
        # city[3] => name
        # city[4] => done_childs

        is_success = True 

        for city in database.mycursor.fetchall():      
            if(int(city[4]) == 1) :
                print(city[0])
                continue;       

            database.mycursor.execute("DELETE FROM districts WHERE city_id='"+str(city[0])+"'")
            database.mydb.commit()
            time.sleep(1)    

            is_done = dump.districts(city)           

            if is_done == True :
                print("Success Dump Districes : "+city[3])
                database.mycursor.execute("UPDATE cites SET done_childs=1 where id='"+str(city[0])+"'")
                database.mydb.commit()            
                time.sleep(3)
            else :
                print("Failed Dump Districes : "+city[3])                 
                is_success = False
                break;  

        return is_success

    except Exception as e:
        print()
        print("Terjadi Kesalahan => ")
        print(e)
        print()
        print("Get Will Repeat Again After 30 Seconds . . .")
        time.sleep(30)
        print("Start Repeat Again")
        print()
        cites()

# def get_cites():
#     provinces = dump_provinces()

#     # provinsi[0] => id
#     # provinsi[1] => kode
#     # provinsi[2] => name
#     # provinsi[3] => done_childs
    

#     for provinsi in provinces:      
#         if(int(provinsi[3]) == 1) :
#             print(provinsi[0])
#             continue;       
    
#         mycursor.execute("DELETE FROM cites WHERE province_id='"+str(provinsi[0])+"'")
#         mydb.commit()
#         time.sleep(1)

#         dump_cites(provinsi)       

#         time.sleep(3)

#         mycursor.execute("UPDATE provinces SET done_childs=1 where id='"+str(provinsi[0])+"'")

#         print("Done "+provinsi[2])

#     return True
            

# def get_districts():
#     mycursor.execute("SELECT id,code,province_id,name,done_childs FROM cites")

#     # city[0] => id
#     # city[1] => kode
#     # city[2] => province_id
#     # city[3] => name
#     # city[4] => done_childs

#     for city in mycursor.fetchall():      
#         if(int(city[4]) == 1) :
#             print(city[0])
#             continue;       

#         mycursor.execute("DELETE FROM districts WHERE city_id='"+str(city[0])+"'")
#         mydb.commit()
#         time.sleep(1)

#         print()
#         print("Dump "+city[3])        

#         dump_districts(city)           

#         time.sleep(3)

#         mycursor.execute("UPDATE cites SET done_childs=1 where id='"+str(city[0])+"'")

#         print("Done "+city[3])
#         print()

#     return True
            