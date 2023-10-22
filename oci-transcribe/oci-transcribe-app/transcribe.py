import os
import logging
import oci
from object_operation import move_objects, transcribe_to_db

def transcription_job(signer):

    try:

        ai_client = oci.ai_speech.AIServiceSpeechClient(config={}, signer=signer)
        #ai_client = oci.ai_speech.AIServiceSpeechClient(signer)
        LANGUAGE_CODE = os.environ['LANG']
                
        object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        #object_storage_client = oci.object_storage.ObjectStorageClient(config=signer)

        bucket_name = os.environ['BUCKET_NAME']
        #bucket_name = 'DocumentAI'
        bucket_name_dest = os.environ['BUCKET_NAME_DEST']
        #bucket_name_dest = 'transcribeAI'

        namespace = object_storage_client.get_namespace().data

        files = move_objects(object_storage_client, namespace, bucket_name, '.wav', 'ProcessedFiles/')

        if (len(files)>0) :
            get_bucket_response = object_storage_client.get_bucket(
                namespace_name=namespace, bucket_name=bucket_name)

            compartment_id = get_bucket_response.data.compartment_id

            OBJECT_LOCATION = oci.ai_speech.models.ObjectLocation(
                namespace_name=namespace, 
                bucket_name=bucket_name,
                object_names=files)

            INPUT_LOCATION = oci.ai_speech.models.ObjectListInlineInputLocation(
                location_type="OBJECT_LIST_INLINE_INPUT_LOCATION", 
                object_locations=[OBJECT_LOCATION])
            
            try:
                get_bucket_response = object_storage_client.get_bucket(
                    namespace_name=namespace,
                    bucket_name=bucket_name_dest)
            except Exception as error:               
                print(error)
                print("*******CREATING DESTINATION BUCKET******")
                object_storage_client.create_bucket(
                    namespace_name=namespace,
                    create_bucket_details=oci.object_storage.models.CreateBucketDetails(
                        name=bucket_name_dest,
                        compartment_id=compartment_id))            

            OUTPUT_LOCATION = oci.ai_speech.models.OutputLocation(
                namespace_name=namespace, 
                bucket_name=bucket_name_dest)

            MODEL_DETAILS = oci.ai_speech.models.TranscriptionModelDetails(
                domain="GENERIC", 
                language_code=LANGUAGE_CODE)
            # Create Transcription Job with details provided
            job_details = oci.ai_speech.models.CreateTranscriptionJobDetails(
                            compartment_id=compartment_id,
                            model_details=MODEL_DETAILS,
                            input_location=INPUT_LOCATION,
                            output_location=OUTPUT_LOCATION)

            transcription_job = None
            print("***CREATING TRANSCRIPTION JOB***")
            try:
                transcription_job = ai_client.create_transcription_job(
                    create_transcription_job_details=job_details)
            except Exception as e:
                print(e)
            else:
                transcription_job_id = transcription_job.data.id
                time_finished = transcription_job.data.time_finished
                print(transcription_job_id)
                
            print("***GET TRANSCRIPTION JOB STATUS WITH ID***")
            print('Processing Audio', end="", flush=True)
            while time_finished == None:
                # Gets Transcription Job with given Transcription job id
                try:
                    if transcription_job.data:
                        transcription_job = ai_client.get_transcription_job(transcription_job.data.id)
                except Exception as e:
                    print(e)
                else:
                    time_finished = transcription_job.data.time_finished
                    print('.', end='', flush=True)

            print("***COMPLETE TRANSCRIPTION JOB***")

            print("***STORING DATABASE***")
            files = move_objects(object_storage_client, namespace, bucket_name_dest, '.json', 'StoredDB/')

            transcribe_to_db(signer, files, object_storage_client, 
                namespace, bucket_name_dest, compartment_id)

            print("***PROCESS COMPLETE***")
        else :
            print("***NO FOUND FILES TO PROCESS***")

    except Exception as error:
        raise Exception(error) 
