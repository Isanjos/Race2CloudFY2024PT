import io
import oci
import os
import json
import oracledb
import logging
from zipfile import ZipFile
import string


def get_dbwallet_from_autonomousdb(dbwallet_dir, db_client, adb_ocid, dbpwd):
    dbwalletzip_location = "/tmp/dbwallet.zip"
    # the wallet password is only used for creation of the Java jks files, which aren't used by cx_Oracle so the value is not important
    atp_wallet_details = oci.database.models.GenerateAutonomousDatabaseWalletDetails(password=dbpwd)
    obj = db_client.generate_autonomous_database_wallet(adb_ocid, atp_wallet_details)
    with open(dbwalletzip_location, 'w+b') as f:
        for chunk in obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    with ZipFile(dbwalletzip_location, 'r') as zipObj:
            zipObj.extractall(dbwallet_dir)
    logging.getLogger().info("wallet generated.......")     
    return dbpwd   

def get_connection(signer, adb_ocid, db_client):

    dbuser = os.getenv("DBUSER")
    #dbuser = "ADMIN"
    dbpwd = os.getenv("DBPWD")
    #dbpwd = "ABCabc12341**"
    dbsvc = os.getenv("DBSVC")
    #dbsvc = "racing_medium"

    dbwallet_dir = "/tmp/dbwallet"

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

def retrieve_data():
    try:
        logging.getLogger().info('signer request')
        #signer = oci.config.from_file()
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

        object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        #object_storage_client = oci.object_storage.ObjectStorageClient(config=signer)

        bucket_name_dest = os.environ['BUCKET_NAME_DEST']
        #bucket_name_dest = 'transcribeAI'

        namespace = object_storage_client.get_namespace().data

        get_bucket_response = object_storage_client.get_bucket(
                namespace_name=namespace, bucket_name=bucket_name_dest)

        compartment_id = get_bucket_response.data.compartment_id

        adb_ocid = os.getenv("ADB_OCID")     
        db_client = oci.database.DatabaseClient(config={}, signer=signer)
        #db_client = oci.database.DatabaseClient(config=signer)   

        #Assumption: database created in the same compartment.
        if(adb_ocid==None) :
            list_autonomous = db_client.list_autonomous_databases(compartment_id=compartment_id, display_name='RACING')
            adb_ocid = list_autonomous.data[0].id

        dbconnection = get_connection(signer, adb_ocid, db_client)

        table = os.getenv("TABLE")
        #table = "WKSP_RACING.TRANSCRIBE_AUDIO"

        columns =  ['id','text','confidence']
        select_stmt =  str("SELECT *FROM {0}").format(table)

        with dbconnection.cursor() as dbcursor:
            dbcursor.execute(select_stmt)

            res_tuple_list = [dict(zip(columns, row)) for row in dbcursor.fetchall()]            
            json_res = json.dumps( res_tuple_list , ensure_ascii=False)

        #print(json_res)
        return json_res
        
    except Exception as error:        
        logging.getLogger().error("Failed:" + str(error))
        json_res = json.dumps( { "data":  "Failed:" + str(error) } , ensure_ascii=False)
        return json_res
