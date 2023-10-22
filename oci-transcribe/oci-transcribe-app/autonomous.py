import io
import oci
import os
import json
import random
import oracledb
import logging
from zipfile import ZipFile
import string


def get_dbwallet_from_autonomousdb(dbwallet_dir, db_client, adb_ocid, dbpwd):
    dbwalletzip_location = "/tmp/dbwallet.zip"

    #atp_wallet_pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) # random string
    # the wallet password is only used for creation of the Java jks files, which aren't used by cx_Oracle so the value is not important
    atp_wallet_details = oci.database.models.GenerateAutonomousDatabaseWalletDetails(password=dbpwd)
    #print(atp_wallet_details, flush=True)
    obj = db_client.generate_autonomous_database_wallet(adb_ocid, atp_wallet_details)
    with open(dbwalletzip_location, 'w+b') as f:
        for chunk in obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    with ZipFile(dbwalletzip_location, 'r') as zipObj:
            zipObj.extractall(dbwallet_dir)
    logging.getLogger().info("wallet generated.......")     
    return dbpwd   

def get_connection(dbwallet_dir, db_client, adb_ocid):
    dbuser = os.getenv("DBUSER")
    #dbuser = "ADMIN"
    dbpwd = os.getenv("DBPWD")
    #dbpwd = "ABCabc12341**"
    dbsvc = os.getenv("DBSVC")
    #dbsvc = "racing_medium"

    wallet_password = get_dbwallet_from_autonomousdb(dbwallet_dir, db_client, adb_ocid, dbpwd)

    # Update SQLNET.ORA
    with open(dbwallet_dir + '/sqlnet.ora') as orig_sqlnetora:
        newText=orig_sqlnetora.read().replace('DIRECTORY=\"?/network/admin\"', 
        'DIRECTORY=\"{}\"'.format(dbwallet_dir))
    with open(dbwallet_dir + '/sqlnet.ora', "w") as new_sqlnetora:
        new_sqlnetora.write(newText)

    logging.getLogger().info("sqlnet.ora: "+ newText )
    # Create the DB Session Pool            
    logging.getLogger().info("dbwallet_dir: "+ dbwallet_dir )
    dbconnection = oracledb.connect(user=dbuser, password=dbpwd, dsn=dbsvc,
                              config_dir=dbwallet_dir, wallet_location=dbwallet_dir, 
                              wallet_password=wallet_password)    

    logging.getLogger().info("Connection "+ dbsvc +" created ")
    return dbconnection

def upload_data(signer, data, dbconnection):
    try:
        table = os.getenv("TABLE")
        #table = "WKSP_RACING.TRANSCRIBE_AUDIO"

        insert_stmt =  str("INSERT INTO {0} VALUES (:1, :2, :3)").format(table)



        with dbconnection.cursor() as dbcursor:        
            dbcursor.execute(insert_stmt, data)
            dbconnection.commit()
        
    except Exception as error:
        print(error)
        logging.getLogger().error("Failed:" + str(error))
        raise Exception(error)
