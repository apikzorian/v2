import os
import uuid
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError
import ibm_s3transfer.manager

def log_done():
    print("DONE!\n")

def log_client_error(e):
    print("CLIENT ERROR: {0}\n".format(e))

def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))

def get_uuid():
    return str(uuid.uuid4().hex)

def generate_big_random_file(file_name, size):
    with open('%s'%file_name, 'wb') as fout:
        fout.write(os.urandom(size))

# Retrieve the list of available buckets
def get_buckets():
    print("Retrieving list of buckets")
    try:
        bucket_list = cos_cli.list_buckets()
        for bucket in bucket_list["Buckets"]:
            print("Bucket Name: {0}".format(bucket["Name"]))

        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to retrieve list buckets: {0}".format(e))

# Retrieve the list of contents for a bucket
def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        file_list = cos_cli.list_objects(Bucket=bucket_name)
        if file_list.has_key("Contents"):
            for file in file_list["Contents"]:
                print("Item: {0} ({1} bytes).".format(file["Key"], file["Size"]))

            log_done()
        else:
            print("Bucket {0} has no items.".format(bucket_name))
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to retrieve bucket contents: {0}".format(e))

# Retrieve a particular item from the bucket
def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos_cli.get_object(Bucket=bucket_name, Key=item_name)
        print("File Contents: {0}".format(file["Body"].read()))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to retrieve file contents for {0}:\n{1}".format(item_name, e))

# Create new bucket
def create_bucket(bucket_name):
    print("Creating new bucket: {0}".format(bucket_name))
    try:
        cos_cli.create_bucket(
            Bucket=bucket_name, 
            CreateBucketConfiguration={
                "LocationConstraint":COS_STORAGE_CLASS
            }
        )
        print("Bucket: {0} created!".format(bucket_name))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to create bucket: {0}".format(e))

# Create new text file
def create_text_file(bucket_name, item_name, file_text):
    print("Creating new item: {0} in bucket: {1}".format(item_name, bucket_name))
    try:
        cos_cli.put_object(
            Bucket=bucket_name,
            Key=item_name,
            Body=file_text
        )
        print("Item: {0} created!".format(item_name))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to create text file: {0}".format(e))

# Delete item
def delete_item(bucket_name, item_name):
    print("Deleting item: {0} from bucket: {1}".format(item_name, bucket_name))
    try:
        cos_cli.delete_object(
            Bucket=bucket_name, 
            Key=item_name
        )
        print("Item: {0} deleted!".format(item_name))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to delete item: {0}".format(e))

# Delete bucket
def delete_bucket(bucket_name):
    print("Deleting bucket: {0}".format(bucket_name))
    try:
        cos_cli.delete_bucket(Bucket=bucket_name)
        print("Bucket: {0} deleted!".format(bucket_name))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to delete bucket: {0}".format(e))

def upload_large_file(bucket_name, item_name, file_path):
    print("Starting large file upload for {0} to bucket: {1}".format(item_name, bucket_name))

    # set the chunk size to 5 MB
    part_size = 1024 * 1024 * 5

    # set threadhold to 5 MB
    file_threshold = 1024 * 1024 * 5

    # set the transfer threshold and chunk size in config settings
    transfer_config = ibm_boto3.s3.transfer.TransferConfig(
        multipart_threshold=file_threshold,
        multipart_chunksize=part_size
    )

    # create transfer manager
    transfer_mgr = ibm_boto3.s3.transfer.TransferManager(cos_cli, config=transfer_config)

    try:
        # initiate file upload
        future = transfer_mgr.upload(file_path, bucket_name, item_name)

        # wait for upload to complete
        future.result()

        print ("Large file upload complete!")
    except Exception as e:
        print("Unable to complete large file upload: {0}".format(e))
    finally:
        transfer_mgr.shutdown()

# Constants for IBM COS values
COS_ENDPOINT = "s3.us-south.cloud-object-storage.appdomain.cloud" # example: https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY_ID = "M2vVCP3n-GibcrdUvC_9p56VnwwhRK0diIK1U-zrBohj" # example: xxxd12V2QHXbjaM99G9tWyYDgF_0gYdlQ8aWALIQxXx4
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_SERVICE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/0440d900927541e98236cd4faaa71c3a:3667a31b-8e2f-4d5b-b9fa-9bfe337ba1c0::" # example: crn:v1:bluemix:public:cloud-object-storage:global:a/xx999cd94a0dda86fd8eff3191349999:9999b05b-x999-4917-xxxx-9d5b326a1111::
COS_STORAGE_CLASS = "us-south-standard" # example: us-south-standard

# Create client connection
cos_cli = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_SERVICE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

# *** Main Program ***
def main():
    try:
        new_bucket_name = "py.bucket." + get_uuid()
        new_text_file_name = "py_file_" + get_uuid() + ".txt"
        new_text_file_contents = "This is a test file from Python code sample!!!"
        new_large_file_name = "py_large_file_" + get_uuid() + ".bin"
        new_large_file_size = 1024 * 1024 * 20 

        # create a new bucket
        create_bucket(new_bucket_name)

        # get the list of buckets
        get_buckets()

        # create a new text file
        create_text_file(new_bucket_name, new_text_file_name, new_text_file_contents)

        # get the list of files from the new bucket
        get_bucket_contents(new_bucket_name)

        # get the text file contents
        get_item(new_bucket_name, new_text_file_name)

        # create a new local binary file that is 20 MB
        generate_big_random_file(new_large_file_name, new_large_file_size)

        # upload the large file using transfer manager
        upload_large_file(new_bucket_name, new_large_file_name, new_large_file_name)

        # get the list of files from the new bucket
        get_bucket_contents(new_bucket_name)

        # remove the two new files
        delete_item(new_bucket_name, new_large_file_name)
        delete_item(new_bucket_name, new_text_file_name)

        # remove the new bucket
        delete_bucket(new_bucket_name)
    except Exception as e:
        log_error("Main Program Error: {0}".format(e))

if __name__ == "__main__":
    main()

package main
import (
    "bytes"
    "fmt"
    "github.com/IBM/ibm-cos-sdk-go/aws"
    "github.com/IBM/ibm-cos-sdk-go/aws/credentials/ibmiam"
    "github.com/IBM/ibm-cos-sdk-go/aws/session"
    "github.com/IBM/ibm-cos-sdk-go/service/s3"
    "io"
    "math/rand"
    "os"
    "time"
)

// Constants for IBM COS values
const (
    apiKey            = "<api-key>" // example: xxxd12V2QHXbjaM99G9tWyYDgF_0gYdlQ8aWALIQxXx4
    serviceInstanceID = "<resource-instance-id>" // example: crn:v1:bluemix:public:cloud-object-storage:global:a/xx999cd94a0dda86fd8eff3191349999:9999b05b-x999-4917-xxxx-9d5b326a1111::
    authEndpoint      = "https://iam.cloud.ibm.com/identity/token"
    serviceEndpoint   = "<endpoint>" // example: https://s3.us-south.cloud-object-storage.appdomain.cloud
)

// UUID
func random(min int, max int) int {
    return rand.Intn(max-min) + min
}

func main() {

    // UUID
    rand.Seed(time.Now().UnixNano())
    UUID := random(10, 2000)

    // Variables
    newBucket := fmt.Sprintf("%s%d", "go.bucket", UUID) // New bucket name
    objectKey := fmt.Sprintf("%s%d%s", "go_file_", UUID, ".txt") // Object Key
    content := bytes.NewReader([]byte("This is a test file from Go code sample!!!"))
    downloadObjectKey := fmt.Sprintf("%s%d%s", "downloaded_go_file_", UUID, ".txt") // Downloaded Object Key

    //Setting up a new configuration
    conf := aws.NewConfig().
        WithRegion("<storage-class>"). // Enter your storage class (LocationConstraint) - example: us-standard
        WithEndpoint(serviceEndpoint).
        WithCredentials(ibmiam.NewStaticCredentials(aws.NewConfig(), authEndpoint, apiKey, serviceInstanceID)).
        WithS3ForcePathStyle(true)

    // Create client connection
    sess := session.Must(session.NewSession()) // Creating a new session
    client := s3.New(sess, conf)               // Creating a new client

    // Create new bucket
    _, err := client.CreateBucket(&s3.CreateBucketInput{
        Bucket: aws.String(newBucket), // New Bucket Name
    })
    if err != nil {
        exitErrorf("Unable to create bucket %q, %v", newBucket, err)
    }

    // Wait until bucket is created before finishing
    fmt.Printf("Waiting for bucket %q to be created...\n", newBucket)

    err = client.WaitUntilBucketExists(&s3.HeadBucketInput{
        Bucket: aws.String(newBucket),
    })
    if err != nil {
        exitErrorf("Error occurred while waiting for bucket to be created, %v", newBucket)
    }

    fmt.Printf("Bucket %q successfully created\n", newBucket)

    // Retrieve the list of available buckets
    bklist, err := client.ListBuckets(nil)
    if err != nil {
        exitErrorf("Unable to list buckets, %v", err)
    }

    fmt.Println("Buckets:")

    for _, b := range bklist.Buckets {
        fmt.Printf("* %s created on %s\n",
            aws.StringValue(b.Name), aws.TimeValue(b.CreationDate))
    }

    // Uploading an object
    input3 := s3.CreateMultipartUploadInput{
        Bucket: aws.String(newBucket), // Bucket Name
        Key:    aws.String(objectKey), // Object Key
    }

    upload, _ := client.CreateMultipartUpload(&input3)

    uploadPartInput := s3.UploadPartInput{
        Bucket:     aws.String(newBucket), // Bucket Name
        Key:        aws.String(objectKey), // Object Key
        PartNumber: aws.Int64(int64(1)),
        UploadId:   upload.UploadId,
        Body:       content,
    }

    var completedParts []*s3.CompletedPart
    completedPart, _ := client.UploadPart(&uploadPartInput)

    completedParts = append(completedParts, &s3.CompletedPart{
        ETag:       completedPart.ETag,
        PartNumber: aws.Int64(int64(1)),
    })

    completeMPUInput := s3.CompleteMultipartUploadInput{
        Bucket: aws.String(newBucket), // Bucket Name
        Key:    aws.String(objectKey), // Object Key
        MultipartUpload: &s3.CompletedMultipartUpload{
            Parts: completedParts,
        },
        UploadId: upload.UploadId,
    }

    d, _ := client.CompleteMultipartUpload(&completeMPUInput)
    fmt.Println(d)

    // List objects within a bucket
    resp, err := client.ListObjects(&s3.ListObjectsInput{Bucket: aws.String(newBucket)})
    if err != nil {
        exitErrorf("Unable to list items in bucket %q, %v", newBucket, err)
    }
    for _, item := range resp.Contents {
        fmt.Println("Name:         ", *item.Key)          // Print the object's name
        fmt.Println("Last modified:", *item.LastModified) // Print the last modified date of the object
        fmt.Println("Size:         ", *item.Size)         // Print the size of the object
        fmt.Println("")
    }

    fmt.Println("Found", len(resp.Contents), "items in bucket", newBucket)


    // Download an object
    input4 := s3.GetObjectInput{
        Bucket: aws.String(newBucket), // The bucket where the object is located
        Key:    aws.String(objectKey), // Object you want to download
    }

    res, err := client.GetObject(&input4)
    if err != nil {
        exitErrorf("Unable to download object %q from bucket %q, %v", objectKey, newBucket, err)
    }

    f, _ := os.Create(downloadObjectKey)
    defer f.Close()
    io.Copy(f, res.Body)

    fmt.Println("Downloaded", f.Name())


    // Delete object within the new bucket
    _, err = client.DeleteObject(&s3.DeleteObjectInput{Bucket: aws.String(newBucket), Key: aws.String(objectKey)})
    if err != nil {
        exitErrorf("Unable to delete object %q from bucket %q, %v", objectKey, newBucket, err)
    }

    err = client.WaitUntilObjectNotExists(&s3.HeadObjectInput{
        Bucket: aws.String(newBucket),
        Key:    aws.String(objectKey),
    })
    if err != nil {
        exitErrorf("Error occurred while waiting for object %q to be deleted, %v", objectKey)
    }

    fmt.Printf("Object %q successfully deleted\n", objectKey)

    // Delete the new bucket
    // It must be empty or else the call fails
    _, err = client.DeleteBucket(&s3.DeleteBucketInput{
        Bucket: aws.String(newBucket),
    })
    if err != nil {
        exitErrorf("Unable to delete bucket %q, %v", newBucket, err)
    }

    // Wait until bucket is deleted before finishing
    fmt.Printf("Waiting for bucket %q to be deleted...\n", newBucket)

    err = client.WaitUntilBucketNotExists(&s3.HeadBucketInput{
        Bucket: aws.String(newBucket),
    })
    if err != nil {
        exitErrorf("Error occurred while waiting for bucket to be deleted, %v", newBucket)
    }

    fmt.Printf("Bucket %q successfully deleted\n", newBucket)
}


func exitErrorf(msg string, args ...interface{}) {
    fmt.Fprintf(os.Stderr, msg+"\n", args...)
    os.Exit(1)