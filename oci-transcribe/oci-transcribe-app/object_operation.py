import os
import logging
import oci
import json
import uuid
from autonomous import upload_data, get_connection

def rename_object(object_storage_client, object_name, namespace, bucket_name, destination_folder):

    new_object_name = destination_folder + object_name
    new_object_name = new_object_name.replace(" ", "")

    try: 
        resp = object_storage_client.rename_object(
        namespace_name=namespace,
        bucket_name=bucket_name,
        rename_object_details=oci.object_storage.models.RenameObjectDetails(
            source_name=object_name,
            new_name=new_object_name))

        logging.getLogger().info("INFO - Response " + json.dumps(resp.data))
        logging.getLogger().info("INFO - Object {0} moved to Folder {1}".format(object_name,destination_folder))

    except Exception as error:
        logging.getLogger().error('ERROR: ' + error)
        print(error)
        raise Exception(error)

    return new_object_name
    

def move_objects(object_storage_client, namespace, bucket_name, extension, destination_folder):
    files = []

    list_objects_response = object_storage_client.list_objects(
        namespace_name=namespace, bucket_name=bucket_name)
    objects = list_objects_response.data.objects

    for obj in objects:
        if obj.name.endswith(extension) and (not obj.name.startswith(destination_folder)) :
            new_object_name = rename_object(object_storage_client, obj.name, namespace, bucket_name, destination_folder) 
            files.append(new_object_name)    
    return files

def transcribe_to_db(signer, files, object_storage_client, namespace, bucket_name, compartment_id):
    
    adb_ocid = os.getenv("ADB_OCID")     
    db_client = oci.database.DatabaseClient(config={}, signer=signer)
    #db_client = oci.database.DatabaseClient(config=signer)

    if(adb_ocid==None) :
        list_autonomous = db_client.list_autonomous_databases(
            compartment_id=compartment_id, 
            lifecycle_state="AVAILABLE")
        adb_ocid = list_autonomous.data[0].id
        print(adb_ocid)

    dbwallet_dir = "/tmp/dbwallet"
    dbconnection = get_connection(dbwallet_dir, db_client, adb_ocid)

    for file in files:
        get_object_response = object_storage_client.get_object(
            namespace_name=namespace,
            bucket_name=bucket_name,
            object_name=file)

        # Get the data from response  
        data = json.loads(get_object_response.data.content.decode('utf-8'))["transcriptions"] 
        id = uuid.uuid4().hex
        
        #print(data[0]["transcription"])
        #print(data[0]["confidence"])        
        #print(id)
        upload_data(signer, [id, data[0]["transcription"], data[0]["confidence"]], dbconnection)





