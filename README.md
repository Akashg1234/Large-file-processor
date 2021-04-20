# Large-file-processor

---

### REQUIREMENTS
**WAMPP or MySQL server, Python, Python-mysql-connector**

---
### STEPS TO RUN THE CODE

#### step 1: Install WAMPP or MySQL server,Python with `pip` on system
#### step 2: Run the command on `cmd` -> `python -m pip install mysql-connector-python` or just run `pip install mysql-connector-python`
#### step 3: Just type `python <location_of_the_file> assignment.py` and hit the `Enter`

Now you see the following options and give options according to you
```cmd
<===== Welcome to large file processing =====>

1 -> For creating Database
2 -> For creating Table
3 -> For Using Database
4 -> For Insert data Database
5 -> For Update data Database
6 -> For Truncate data Database
7 -> For query on data Database
8 -> For Creating Aggreegate table Database   

 Enter operation option index..
Use database first (recomended)
```
just like that
![Screenshot (1)](https://user-images.githubusercontent.com/46678116/115434148-fd2ce680-a225-11eb-9a59-640d58ee3a5e.png)

---
### DETAILS OF THE TABLE AND THEIR SCHEMA

There are Two tables called `product` and `meta_table`(aggreegate table) 

And the schema of the `product` tables are
|NAME |SKU |DESCRIPTION |
|---|---|---|
|...|...|...|

**Command to recreate the table**

`CREATE TABLE <table_name> (NAME varchar(100) NOT NULL,SKU varchar(100) NOT NULL ,DESCRIPTION TEXT NOT NULL`

And the schema of the `meta_table` tables are
|NAME |NUMBER_OF_PRODUCT |
|---|---|
|...|...|

**Command to recreate the table**

`CREATE TABLE <table_name> 
  (
  NAME varchar(100) NOT NULL,
  NO_OF_PRODUCT TEXT NOT NULL
  )`
  
---
  
### What is done from “Points to achieve”
  
  1. My code follow concept of OOPS
  2. Support for updating existing products in the table based on `sku` as the primary key.
  3. All product details are to be ingested into a single table `product`
  4. An aggregated table `meta_table` on above rows with `name` and `no. of products` as the columns

![Screenshot (2)](https://user-images.githubusercontent.com/46678116/115444318-0a4fd280-a232-11eb-8bd8-ef4b3a71b3f3.png)


![Screenshot (3)](https://user-images.githubusercontent.com/46678116/115445278-46cffe00-a233-11eb-8ef4-492bcf723f70.png)


---

### What is not done from “Points to achieve”

  1. Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the
scale of what should happen if the file is to be processed in 2 mins

I can work around it with Multithreading and Multiprocessing to achive Concurrency and Parallelism

---

### What would you improve if give more days

I would like to work on the scalability section and modification on the Aggreegate table 
