# pybraads Readme 📜
Brainstorming package, manage ODBC connexion to database Advantage Database.

# Installation ⚡
Opérating system :  Windows, MacOS & Linux :

# Available function/class 📑
## AdsConnection(DataDirectory, Uid, Pwd)
    To create ans open data base
    DataDirectory : a full path to the data dictionary with ".add" file.
    Uid  : the data base user.
    Pwd : The data base password
### Close()
    To close data base
### commit()
    To save all modification in data base
### rollback()
    To cancel all modification in data base after the last commit
### isconnected
    To test if the data base is connected
### error
    To get the last error
## AdsQuery(adsconn)
    To create à new query.
    adsconn : is the AdsConnection of the data base tu use.
### sql
    To get or set the query before open.
    the parameters in query must be prefixed by ":" like :prefref.
### addparam(aParamName, aParamValue)
    aParamName : the name of the parameter in the query (without the :) attention case sesitive.
    aParamValue : any value for the parameter.
### execute()
    Execute the query.
### open()
    Open the query.
### error
    The get the last execution error
### fieldnames
    To get a list of all field in the select
### FieldIndex(afieldname)
    To get the field position in the query, to use with the dataset.
### eof
    To navigate in all the database unti last record
### allrecords
    To get a list with all record in database
### dataset
    To get one record to read the specific field like :
    Query.dataset[aQuery.FieldIndex('FirstName')]

# Howto use 📰
    import pybraads
    import pybrastr

    try:
        DataDirectory = "\\\\192.168.91.1\\d\\DevBrain\\Python\\pybraads\\dbtest\\dbtest.add"
        user = "adssys"
        password = "123"
        aConn = pybraads.AdsConnection(DataDirectory, user, password)
        aQuery = pybraads.AdsQuery(aConn)

        #Chesk if table exist
        sql = ''.join(["select * from system.tables ",
                       "where Name = ", pybrastr.quotedStr("DEMO1")
                       ])
        aQuery.sql = sql
        aQuery.open()
        tblfound = aQuery.dataset[aQuery.FieldIndex('Name')] != "DEMO1"

        if tblfound:
            #Delete existing table
            print("Table DEMO1 not exist")            
            return False
        
        sql = ''.join(["select * from DEMO1 "])
        aQuery.sql = sql
        aQuery.open()

        fields = ''
        for field in aQuery.fieldnames:
            if fields == '':
                fields = fields + field.ljust(20, ' ')
            else:
                fields = fields + ' | ' + field.ljust(20, ' ')
        
        print(fields)
        print(''.center(len(fields), '-'))

        while not(aQuery.eof):
            ln = ''
            ln = aQuery.dataset[aQuery.FieldIndex('FirstName')].ljust(20, ' ')
            ln = ln + ' | ' + aQuery.dataset[aQuery.FieldIndex('Name')].ljust(20, ' ')
            ln = ln + ' | ' + aQuery.dataset[aQuery.FieldIndex('BirthDate')].strftime('%Y-%m-%d').ljust(20, ' ')
            print(ln)
        
    finally:
        aConn.Close()
        print(pybraads.version())

## Meta 💬
Brainstorming – Support.erp@brainstorming.eu

Distributed under the MIT license. See ``LICENSE`` for more information.