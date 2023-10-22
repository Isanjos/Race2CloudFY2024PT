import oci
import logging
from transcribe import transcription_job


try:       
    logging.getLogger().info('signer request')
    #signer = oci.auth.signers.get_resource_principals_signer()
    #signer = oci.config.from_file()
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    
    transcription_job(signer)    

except Exception as error:
    raise Exception(error)

