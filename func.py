#
# oci-kms-swap version 1.0.
#
# Copyright (c) 2023 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
from fdk import response

import oci

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = swap_kms_instances(ctx, signer)
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

# List instances ---------------------------------------------------------------
def swap_kms_instances(ctx, signer):
    cfg = ctx.Config()
    key = cfg["kmskeyid"]
    status = ""
    client = oci.core.BlockstorageClient(config={}, signer=signer)
    # Applies Customer Managed Keys to new compute instances
    try:
        # Applies keys to the boot volumes in the current compartment
        current_boot_volumes = client.list_boot_volumes(compartment_id=signer.compartment_id)
        for v in current_boot_volumes.data:
            if v.kms_key_id == key:
                print(v.id, "Correct Key Present")
            else:
                if v.lifecycle_state == "AVAILABLE":
                    client.update_boot_volume_kms_key(
                        boot_volume_id=v.id,
                        update_boot_volume_kms_key_details=oci.core.models.UpdateBootVolumeKmsKeyDetails(
                            kms_key_id="ocid1.key.oc1.iad.b5r33vmcaah4o.abuwcljtjfdyu6qomsh52acdusxxs5qqutmeyzsdxw2b4exzmnyif4r6jydq",
                        )
                    )
                    status += "Key Applied for " + v.id + ".\n"
                else:
                    status += "This function not available for " + v.id + " because it is " + v.lifecycle_state + ".\n"
        # Applies keys to the boot volumes in the current compartment
        current_block_volumes = client.list_volumes(compartment_id=signer.compartment_id)
        for v in current_block_volumes.data:
            if v.kms_key_id == key:
                print(v.id, "Correct Key Present")
            else:
                if v.lifecycle_state == "AVAILABLE":
                    client.update_volume_kms_key(
                        volume_id=v.id,
                        update_volume_kms_key_details=oci.core.models.UpdateVolumeKmsKeyDetails(
                            kms_key_id="ocid1.key.oc1.iad.b5r33vmcaah4o.abuwcljtjfdyu6qomsh52acdusxxs5qqutmeyzsdxw2b4exzmnyif4r6jydq",
                        )
                    )
                    status += "Key Applied for " + v.id + ".\n"
                else:
                    status += "Status not available for " + v.id + " because it is " + v.lifecycle_state + ".\n"
    except Exception as ex:
        print("ERROR: accessing Block Volumes failed", ex, flush=True)
        raise
    resp = { "Operation Complete" : status }
    return resp
