import csv
from os import access
import mysql.connector as mc
from mysql.connector import errorcode

class Access:
    
    # db connection class
    class db_operation:
        # initialization
        def __init__(self,dbuser=None,dbhost=None,dbpass=None,dbname=None):
            self.db_user=dbuser
            self.db_host=dbhost
            self.db_pass=dbpass
            self.db_name=dbname

        # drop database
        def drop_database(self,database_name,connect,cursor):
            try:
                cursor.execute("DROP DATABASE {}".format(database_name)) # drop the user input database
                print("successfully database {} droped...".format(database_name))
                connect.commit()
                return True
            except mc.Error as err:
                if err==errorcode.ER_DB_DROP_EXISTS:
                    print("Database {} does not exist".format(database_name))
                    connect.commit()
                    return False    
        
        #de connection
        def dbconnection(self,**kargs):
            connect=None
            try:
                connect = mc.connect(user=self.db_user,password=self.db_pass,host=self.db_host) # try to connect to the host

            except mc.Error as err:
                if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Oops.. something went wrong in credentials..")
                elif err.errno==errorcode.ER_BAD_DB_ERROR:
                    print("database does not exist")
                else:
                    print(err)
            
            if connect is not None:
                print("successfully connected...")
                return connect,connect.cursor() # return the cursor method and connection reference

        # use database
        def use_db(self,connect,cursor):
            count=1
            db_list={}
            cursor.execute("SHOW DATABASES")    # taking view of the all the available database
            for db in cursor:
                print(count,"->",db)
                db_list[count]=db;count+=1
            count=1    
            option=int(input("enter your choice index...\n"))   # choosing the desired database
            print("you are using {} database".format(db_list[option][0]))
            cursor.execute("USE {}".format(db_list[option][0]))
            connect.database=db_list[option][0]     # assigning the selected database
            self.db_name=db_list[option][0]
            connect.commit() 
            return cursor

        # create table with schema
        def create_table(self,table_name,connect,cursor):
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute("CREATE TABLE {} (NAME varchar(100) NOT NULL,SKU varchar(100) NOT NULL ,DESCRIPTION TEXT NOT NULL)".format(table_name))  # try to create table in the selected the database
            except mc.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("table {} already exists..".format(table_name))
                else:
                    print(err.msg)
            connect.commit()
            return cursor
        # method to create the aggregated table in the selected the database
        def create_aggregated_table(self,table_name,connect,cursor):
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute("CREATE TABLE {} (NAME varchar(100) NOT NULL,NO_OF_PRODUCT TEXT NOT NULL)".format(table_name))       # try to create the aggregated table in the selected the database
            except mc.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("table {} already exists..".format(table_name))
                else:
                    print(err.msg)
            connect.commit()
            return cursor
        
        # inserting data
        def insert_data(self,table_name,data,connect,cursor):
            
            insert_query="INSERT INTO {} (NAME,SKU,DESCRIPTION) VALUES (%s,%s,%s)".format(table_name)
            value=[tuple(y) for y in data]
            # print(value)
            print("Inserting data.......\n")
            try:
                cursor.executemany(insert_query,value) # Inserting all the readed data from the csv file to database table 
                # It is required to make the changes, otherwise no changes are made to the table
                connect.commit()
                print("Inserted....\n")
            except mc.errors as err:
                print(err)
            return cursor

        # updateing data
        def update_data(self,**values):
            if values["sku"] is None:   # checking the presence of the primary key
                print("Update not possible..!")
                return
            update_query="UPDATE {} SET "
            # checking the valid data , if the value is valid then concatinate the query string
            if values["name"] is not None:
                update_query+="NAME=%s "
            else:update_query+=""
            if values["description"] is not None:
                update_query+="DESCRIPTION= %s "
            else:update_query+=""
            update_query+="WHERE SKU=%s "
            val=[]  # coresponding values for the table attributes
            if values["name"] is not None:
                val.append(values["name"])
            if values["description"] is not None:
                val.append(values["description"])
            val.append(values["sku"])
            try:       
                values["cursor"].execute(update_query.format(values["tablename"]),tuple(val))   # converting the value list to tuple 
            except mc.Error as err:
                print(err)    
            values["connect"].commit()

        # database querying
        def querying(self,table,connect,cursor):
            agreegate_query="SELECT NAME,COUNT(NAME) FROM {} GROUP BY NAME ORDER BY COUNT(NAME) DESC".format(table)
            # query to give us no. of products with the same name
            try:
                cursor.execute(agreegate_query)
                print("name\t no. product")
                for data in cursor:
                    print(data)
            except mc.Error as err:
                print(err)
            connect.commit()
            return cursor

        # create database
        def create_database(self,database_name,connect,cursor):
            try:
                cursor.execute("CREATE DATABASE {}".format(database_name))  # try to create database
                print("successfully created...")
            except mc.Error as err:
                print("Oops!..unable to create database..{}".format(err))
                if err == errorcode.ER_DB_CREATE_EXISTS:
                    print("{} already exist..".format(database_name))
                    option=input("Would you want to use it or not..[y/n]")  # asking to create the database
                    if option=="Y" or option=="y":
                        if self.use_db(connect,connect.cursor()):
                            print("Database using..")
                    elif option=="N" or option=="n":
                        option=input("Would you want to drop it or not..[y/n]")
                        if option=="Y" or option=="y":
                            # droping the database
                            if self.drop_database(database_name,connect,connect.cursor()):print("Database droped..")
                                
                    else:print("terminated operation...")
                
            connect.commit()
            return cursor
        
        # truncate the user defined table
        def truncate_data(self,table_name,connect,cursor):
            truncate_query="TRUNCATE TABLE {}".format(table_name)
            try:
                print("trancating.. data.. from {} table.....\n".format(table_name))    # truncate the user defined table
                cursor.execute(truncate_query)
            except mc.Error as err:
                print(err)

    class file_operation:
        # reading the file from a file object
        def reading(self,file):
            return csv.reader(file,quoting=csv.QUOTE_ALL)   # reading the csv File

        # opening the file for reading 
        def open_file(self,file_source):
            f=None
            try:
                f=open(file_source,mode='r',encoding='utf-8') # open the file in reading mode encoding it utf-8
                #print('file readed',f)
            except(OSError,IOError) as e:
                print('Oops! ...Error occured..{}'.format(e.errno))
            if f is not None:
                return f

## driver code    
if __name__=='__main__':
    access=Access.db_operation('root','localhost','')
    file_access=Access.file_operation()
    connect,cursor=access.dbconnection()
    
    # sql query handling method
    def trigger_query_data_db():
        table_name=input("Enter table name...:\n")
        if table_name is None or table_name =="":trigger_query_data_db()
        else:access.querying(table_name,connect,cursor)
    
    # table truncate triggering method
    def trigger_truncate_data_db():
        user_choice=input("Are you sure..to truncate data..")
        if user_choice=='y' or user_choice=='Y':
            table_name=input("Enter table name...:\n")
            if table_name is None or table_name =="":trigger_truncate_data_db()
            else:access.truncate_data(table_name,connect,cursor)
    
    # DB connection triggering method
    def trigger_db_creation():
        table_name=input("Enter database name...: \n")
        if table_name is None or table_name =="":trigger_db_creation()
        else:access.create_database(table_name,connect,cursor)
    
    # table creation triggering method    
    def trigger_table_creation():
        table_name=input("Enter table name...:\n")
        if table_name is None or table_name =="":trigger_table_creation()
        else:access.create_table(table_name,connect,cursor)
    
    # DB using triggering method    
    def trigger_use_db():
        access.use_db(connect,cursor)
    
    # data insert triggering method    
    def trigger_insert_data_db():
        table_name=input("Enter table name...:\n")
        if table_name is None or table_name =="":trigger_insert_data_db()
        else:access.insert_data(table_name,file_access.reading(file_access.open_file('/products.csv')),connect,cursor)
    
    # aggreeegate table creation triggering method
    def trigger_aggreegate_table():
        table_name=input("Enter table name...:\n")
        if table_name is None or table_name =="":trigger_aggreegate_table()
        else:access.create_aggregated_table(table_name,connect,cursor)
    
    # data update triggering method
    def trigger_update_data_db():
        sku,name,description,description_option=None,None,None,None
        table_name=input("Enter table name...: \n")
        sku=input("First input the id (mandatory):\n")
        if sku is None or sku=="" or table_name is None or table_name =="":
            trigger_update_data_db()
        name_option=input("would you want to update name [y/n]:\n")
        if name_option=='Y' or name_option=='y':
            name=input("Enter name...:\n")
        description_option=input("would you want to update description [y/n]:\n")
        if description_option=='Y' or description_option=='y':
            description=input("Enter description....:\n")
        
        if name is None and description is None:
            print("Nothing to update..")
        else:    
            access.update_data(tablename=table_name,sku=sku,name=name,description=description,connect=connect,cursor=cursor)    
    
    # option for user to choose operation with corresponding method reference
    switch={
            "1":["For creating Database",trigger_db_creation],
            "2":["For creating Table",trigger_table_creation],
            "3":["For Using Database",trigger_use_db],
            "4":["For Insert data Database",trigger_insert_data_db],
            "5":["For Update data Database",trigger_update_data_db],
            "6":["For Truncate data Database",trigger_truncate_data_db],
            "7":["For query on data Database",trigger_query_data_db],
            "8":["For Creating Aggreegate table Database",trigger_aggreegate_table]
        }
    option=None 
    
    # choosing option method
    def choice(option):
        switch[option][1]()
    
    # input taking method    
    def taking_input():
        option=input()
        if option in switch.keys():
            choice(option)
            user_input=input("Do you want to continue..?[y/n]")
            if user_input=='y'or user_input=='Y':
                print_choice()     
                taking_input()  # recall the method
        else:
            print("Invalid Choice..Try again")
            print_choice()     
            taking_input()
    print("\n<===== Welcome to large file processing =====>\n")
    
    def print_choice():    # user choice printing
        for i in switch.keys():
            print("{} -> {}".format(i,switch[i][0]))
        print("\n Enter operation option index..\nUse database first (recomended)")

    # calling the methods accordingly...    
    print_choice()     
    taking_input()
