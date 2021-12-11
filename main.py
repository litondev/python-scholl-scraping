import dump 
import get_data
import database
import time 

while True:        
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
    
    # if command == "5":
    #     print("Jika dibirakan kosong maka isinya akan")
    #     print("=> https://dapo.kemdikbud.go.id/rekap/dataSekolah")        
    #     print("")
    #     cmmand_inputkan = str(input("Masukan Url : "))

    #     print()
    #     print("Jika dibiarkan kosong maka isinya akan")
    #     print("=> semester terakhir *contoh => (1,2)")
    #     command_semester = str(input("Masukan semester : "))

    #     print()
    #     print("Jika dibiarkan kosong maka isinya akan")
    #     print("=> tahun tearkhir *conth => (2020,2021)")
    #     command_tahun = str(input("Masukan tahun semester : "))

    print()

    if command == "6" :
        print("Anda Keluar Bye")
        print()
        break;
    elif command == "5" :
        print("Dump Semuanya")
        print()
        break;
    elif command == "4" :
        print("Dump Sekolah")
        print()
        break;
    elif command == "3" :        
        is_done = get_data.districts()

        if is_done == True :
            print("Success Dump Districtes")
        else :
            print("Failed Dump Districtes") 

        print("Dump Kecamatan")
        print()
        break;
    elif command == "2" :        
        is_done = get_data.cites()

        if is_done == True :
            print("Success Dump Cites")
        else :
            print("Failed Dump Cites")   

        print("Dump Kota")
        print()
        break;
    elif command == "1" : 
        is_done = dump.provinces()

        if is_done == True :
            print("Success Dump Provinces")
        else :
            print("Failed Dump Provinces")   

        print("Dump Provinsi")
        print();
        break;