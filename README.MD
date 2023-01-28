# Exchange an Oracle Managed encryption keys with a Customer Managed encryption key for Block Storage

This function uses Policies and Dynamic Groups to make API calls to OCI 
services using the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html). It returns the block storage volumes 
that were changed and the volumes that were unaffected due to their status
not being AVAILABLE.

The function calls the following OCI Python SDK class:
* [Block Storage Client](https://docs.oracle.com/en-us/iaas/tools/python/2.90.3/api/core/client/oci.core.BlockstorageClient.html#oci.core.BlockstorageClient) to authenticate

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.

## Pre-requisites

1. Before you deploy this sample function, make sure you have run steps A, B 
and C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm)
    * A - Set up your tenancy
    * B - Create application
    * C - Set up your Cloud Shell dev environment

2. Have your Oracle Object Storage Namespace available. This can be found by
logging into your [cloud account](https://cloud.oracle.com/), under your user profile, click on your Tenancy.
Your Object Storage Namespace is shown there.

3. Have the OCID for a master encryption key for the volumes you would like to encrypt.

4. Apply the policy statements to the compartment where this function will operate.

## List Applications 

Assuming you have successfully completed the prerequisites, you should see your 
application in the list of applications.

```
fn ls apps
```

## Create or Update your Dynamic Group

In order to use other OCI Services, your function must be part of a dynamic 
group. For information on how to create a dynamic group, refer to the 
[documentation](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

When specifying the *Matching Rules*, we suggest matching all functions in a compartment with:

```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaxxxxx'}
```


## Create or Update IAM Policies

Create a new policy that allows the dynamic group to `manage volumes` in
the functions related compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group name> to manage volumes in compartment <compartment-name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to manage volumes in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize the function

Review the following files in the current folder:

- [requirements.txt](./requirements.txt) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [func.py](./func.py) which is your actual Python function

The name of your function *ociswapkms* is specified in [func.yaml](./func.yaml).

You will need to supply the OCID of the master encryption key to be used.

![user input icon](./images/userinput.png)

```
fn config app <app-name> kmskeyid <Master Encryption Key OCID>
```
e.g.
```
fn config app myapp kmskeyid ocid.key.oc1.iad.t8swpkfj.u6qomsh52acdusxxs5qqutmabuwcljtjfd
```

## Deploy the function

In Cloud Shell, run the *fn deploy* command to build the function and its dependencies as a Docker image, 
push the image to the specified Docker registry, and deploy the function to Oracle Functions 
in the application created earlier:

![user input icon](./images/userinput.png)

```
fn -v deploy --app <app-name>
```
e.g.
```
fn -v deploy --app myapp
```


## Test
![user input icon](./images/userinput.png)
```
fn invoke <app-name> <function-name>
```
e.g.
```
fn invoke myapp ociswapkms
```

## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)