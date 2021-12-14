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


def schools():
    try:    
        database.mycursor.execute("SELECT id,code,city_id,name,done_level_tk_childs,done_level_sd_childs,done_level_smp_childs,done_level_smk_childs,done_level_sma_childs,done_level_slb_childs FROM districts")

        # city[0] => id
        # city[1] => kode
        # city[2] => city_id
        # city[3] => name
        # city[4] => done_level_tk_childs
        # city[5] => done_level_sd_childs
        # city[6] => done_level_smp_childs
        # city[7] => done_level_smk_childs
        # city[8] => done_level_sma_childs
        # city[9] => done_level_slb_childs

        is_success_tk = True 
        is_success_sd = True
        is_success_smp = True 
        is_success_smk = True 
        is_sucesss_sma = True 
        is_success_slb = True 

        for district in database.mycursor.fetchall():      
            # level tk
            if(int(district[4]) == 1) :
                print("Skip Tk "+str(district[0]))                 
            else: 
                database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND level='TK'")
                database.mydb.commit()
                time.sleep(1)    

                is_done_tk = dump.schools(district,"tk")           

                if is_done_tk == True :
                    print("Success Dump Tk : "+district[3])
                    database.mycursor.execute("UPDATE districts SET done_level_tk_childs=1 where id='"+str(district[0])+"'")
                    database.mydb.commit()            
                    time.sleep(5)
                else :
                    print("Failed Dump Tk : "+district[3])                 
                    is_success_tk = False
                    break;  

            if(not is_success_tk):
                return False
            
            # level_sd 
            # if(int(district[5]) == 1):
            #     print("Skip Sd "+str(district[0]))            
            # else:
            #     database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND level='SD'")
            #     database.mydb.commit()
            #     time.sleep(1)    

            #     is_done_sd = dump.schools(district,"sd")           

            #     if is_done_sd == True :
            #         print("Success Dump SD : "+district[3])
            #         database.mycursor.execute("UPDATE districts SET done_level_sd_childs=1 where id='"+str(district[0])+"'")
            #         database.mydb.commit()            
            #         time.sleep(3)
            #     else :
            #         print("Failed Dump SD : "+district[3])                 
            #         is_success_sd = False
            #         break;  

            # if(not is_success_sd):
            #     return False
            
            # level_smp
            # if(int(district[6]) == 1):
            #     print("Skip Smp "+str(district[0]))            
            # else:
            #     database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND level='SMP'")
            #     database.mydb.commit()
            #     time.sleep(1)    

            #     is_done_smp = dump.schools(district,"smp")           

            #     if is_done_smp == True :
            #         print("Success Dump SMP : "+district[3])
            #         database.mycursor.execute("UPDATE districts SET done_level_smp_childs=1 where id='"+str(district[0])+"'")
            #         database.mydb.commit()            
            #         time.sleep(3)
            #     else :
            #         print("Failed Dump SMP : "+district[3])                 
            #         is_success_smp = False
            #         break;  

            # if(not is_success_smp):
            #     return False
            
            # level_smk
            # if(int(district[7]) == 1):
            #     print("Skip Smk "+str(district[0]))            
            # else:
            #     database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND  level='SMK'")
            #     database.mydb.commit()
            #     time.sleep(1)    

            #     is_done_smk = dump.schools(district,"smk")           

            #     if is_done_smk == True :
            #         print("Success Dump SMK : "+district[3])
            #         database.mycursor.execute("UPDATE districts SET done_level_smk_childs=1 where id='"+str(district[0])+"'")
            #         database.mydb.commit()            
            #         time.sleep(3)
            #     else :
            #         print("Failed Dump SMK : "+district[3])                 
            #         is_success_smk = False
            #         break;  

            # if(not is_success_smk):
            #     return False
            
            # level_sma
            # if(int(district[8]) == 1):
            #     print("Skip Sma "+str(district[0]))            
            # else:
            #     database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND level='SMA'")
            #     database.mydb.commit()
            #     time.sleep(1)    

            #     is_done_sma = dump.districts(district,"sma")           

            #     if is_done_sma == True :
            #         print("Success Dump SMA : "+district[3])
            #         database.mycursor.execute("UPDATE districts SET done_level_sma_childs=1 where id='"+str(district[0])+"'")
            #         database.mydb.commit()            
            #         time.sleep(3)
            #     else :
            #         print("Failed Dump SMA : "+district[3])                 
            #         is_success_sma = False
            #         break;  

            # if(not is_success_sma):
            #     return False
            
            # level_slb
            # if(int(district[9]) == 1):
            #     print("Skip Slb "+str(district[0]))            
            # else:
            #     database.mycursor.execute("DELETE FROM schools WHERE district_id='"+str(district[0])+"' AND level='SLB'")
            #     database.mydb.commit()
            #     time.sleep(1)    

            #     is_done_slb = dump.schools(district,"slb")           

            #     if is_done_slb == True :
            #         print("Success Dump SLB : "+district[3])
            #         database.mycursor.execute("UPDATE districts SET done_level_slb_childs=1 where id='"+str(district[0])+"'")
            #         database.mydb.commit()            
            #         time.sleep(3)
            #     else :
            #         print("Failed Dump SLB : "+district[3])                 
            #         is_success_slb = False
            #         break;  

            # if(not is_success_slb):
                # return False
            
        return True

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