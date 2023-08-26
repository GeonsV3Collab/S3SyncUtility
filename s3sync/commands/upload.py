import sys
import os
import boto3
from datetime import datetime

from botocore.exceptions import BotoCoreError, NoCredentialsError
from s3sync.commands.size import get_total_upload_size, format_size
from s3sync.commands.common import get_total_upload_objects
from s3sync.commands.state_management import load_state, save_state, calculate_checksum

def upload_to_s3(directory, s3_bucket, s3_prefix, exclude_list, dry_run=False, verbose=False):
    """Upload file(s) from a directory to an S3 bucket.

    Args:
        directory (str): The directory containing file(s) to upload.
        s3_bucket (str): The name of the S3 bucket.
        s3_prefix (str): The prefix to use for S3 object keys.
        exclude_list (list): List of items to exclude from upload.
        dry_run (bool, optional): Simulate the upload process without actual upload. Defaults to False.
        verbose (bool, optional): Increase verbosity of the upload process. Defaults to False.
    """

    # if not s3_bucket or not s3_prefix:
    #     print("Error: Both --s3-bucket [S3_BUCKET] and --s3-prefix [S3_PREFIX] are required.")
    #     sys.exit(1)

    if not s3_bucket or not s3_prefix:
        if not s3_bucket and not s3_prefix:
            print("Error: Both --s3-bucket [S3_BUCKET] and --s3-prefix [S3_PREFIX] are required.")
        elif not s3_bucket:
            print("Error: --s3-bucket [S3_BUCKET] is required.")
        else:
            print("Error: --s3-prefix [S3_PREFIX] is required.")
        sys.exit(1)

    try:
        print("Uploading to S3:")
        print(f"Bucket: {s3_bucket}")
        print(f"Uploading To: {s3_prefix}")

        # Calculate total objects and upload size
        total_objects = get_total_upload_objects(directory, exclude_list)
        upload_size = get_total_upload_size(directory, exclude_list)
        print(f"Total Objects: {total_objects}")
        print(f"Total upload size: {format_size(upload_size)}")

        confirm = input("Proceed with upload? (yes/no): ").lower()
        if confirm == 'yes':
            state = load_state()

            try:
                s3 = boto3.client('s3')
                for root, dirs, files in os.walk(directory):
                    dirs[:] = [d for d in dirs if d not in exclude_list]
                    for file in files:
                        if file not in exclude_list:
                            local_path = os.path.join(root, file)
                            relative_path = os.path.relpath(local_path, directory)
                            s3_key = os.path.join(s3_prefix, relative_path)
                            # Check if the file is already uploaded or unchanged
                            local_checksum = calculate_checksum(local_path)
                            file_size = os.path.getsize(local_path)
                            last_modified = os.path.getmtime(local_path)  # Get the last modified timestamp
                            if local_path in state and local_checksum == state[local_path]['hash']:
                                if verbose:
                                    print(f"Skipping {file} as it's already uploaded and unchanged.")
                            else:
                                # Upload the file(s)
                                if dry_run:
                                    print(f"Simulating: Would upload {file} to S3 bucket {s3_bucket} as {s3_key}")
                                else:
                                    print(f"Uploading {file} to S3 bucket {s3_bucket}")
                                    if verbose:
                                        print(f"Uploading {local_path} to S3 bucket {s3_bucket} with key {s3_key}")
                                    s3.upload_file(local_path, s3_bucket, s3_key)
                                    # Convert last_modified timestamp to string representation
                                    last_modified_formated = datetime.utcfromtimestamp(last_modified).isoformat()
                                    state[local_path] = {'hash': local_checksum, 'size': file_size, 'last_modified': last_modified_formated, 'extension': os.path.splitext(file)[1]}
                                    if verbose:
                                        print(f"Uploaded {file} as {s3_key}")
                # Save updated state
                save_state(state)
            except (BotoCoreError, NoCredentialsError) as e:
                print(f"Error occurred: {e}")
        else:
            print("Upload operation canceled.")

    except KeyboardInterrupt:
        print("\nOperation interrupted by the user.")
        sys.exit(0)
