# SFTP-Client

## List of commands and description:
```
Command    Description
---------  ----------------------------------------------
ls         list directories and files on remote server   
get_file   get file from remote server
chmod      change permissions on remote server
closeconn  close connection
logoff     logout from remote server
rm         delete file from remote server
mkdir      create directory on remote server
lsl        list of directories and files on local machine
cd         change directory on remote server
rename     rename file on remote server
renamel    rename file on local machine
copydir    copy directories on remote server
cdl        change directory on local machine
rmd        delete directory on remote server
put        put file/files onto remote server

```

## Installing python packages:

Install pysftp

```shell
pip install pysftp
```
Install tabulate

```shell
pip install tabulate
```

Install termcolor

```shell
pip install termcolor
```

## How to run SFTP client:

From root directory: `SFTP-Client/`, use command: python main.py


## How to run the unit tests:

1. Add your credentials - replace `<username> and <password>` in `data.json` file with your credentials.

2. From root directory: `SFTP-Client/`, use command: pytest test_sftpshellfuncs.py