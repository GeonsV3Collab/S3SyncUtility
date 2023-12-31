# S3SyncUtility

**S3SyncUtility** is a Python tool using Boto3 to simplify syncing local directories with Amazon S3, for easy uploads and downloads.

## Installation

You can install S3Sync using `pip` by providing the Git repository URL:

```bash
pip install git+https://github.com/GeonsV3Collab/S3SyncUtility.git@development

or

pip install s3sync_util
```


## Configuration

Initialize the S3Sync configuration:

```markdown
s3sync config init
```
This will interactively create a `.config.ini` file with your S3 bucket and prefix settings.

1. Modify **\`.config.ini`**:

    You can manually edit the **\`.config.ini`** file to change the configuration options.


## Usage

Before using the utility, make sure you have the required dependencies installed.

1. To upload **files/directories** to S3:

    ```markdown
    s3sync upload --directory <local_directory> --s3-bucket <bucket_name> --s3-prefix <prefix>
    ```

2. To download **files/directories** from S3:

    ```markdown
    s3sync download --s3-bucket <bucket_name> --s3-prefix <prefix> --directory <local_directory>
    ```

## Versioning Example

- Major version bump: `v1.0.0` (Breaking backward compatibility)
- Minor version bump: `v1.1.0` (Backward-compatible new features)
- Patch version bump: `v1.1.1` (Backward-compatible bug fixes)
- Alpha release: `v2.0.0-alpha` (Initial development)
- Beta release: `v2.0.0-beta` (Feature-complete, testing phase)
- Dev version: `v2.0.0-dev` (Development version)
- Stable release: `v2.0.0` (Production-ready)

## License

This project is licensed under the [MIT License](License).
