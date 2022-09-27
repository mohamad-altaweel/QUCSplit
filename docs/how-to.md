# How to run 

## OrientDb
OrientDB requires Java, version 1.7 or higher. You can download the binary version [here](https://orientdb.org/download) or use the zip file provided in /orietdb, unzip the file, and then you can run the scripts found in /bin.
To launch the server, start the terminal and type the following

```console
cd $ORIENTDB_HOME/bin
./server.sh
```

Or if you are running on windows you can open the bash file found in /bin/server.bat
The server should be accessible from broswer through http://localhost:2480
for full details, you can refer to the [orientdb documentation website](https://orientdb.com/docs/2.2.x/Tutorial-Installation.html)

## QuCMixx & QuPie
QuCMixx & QuPie are flask applications written in python. Hence, you need python version 3.7 to run those applications. In addition, several pip packages are required in requirements.txt file. to install them start the termin and type the following command. Make sure you installed pip environment as well.

```console
pip install -r requirements.txt
```

for QuCMixx we need to install an extra database for NLP purpose

```console
python -m nltk.downloader punkt
```

Now we need to provide some configuration to be able to run both services. In each folder of each service, create a config.json file
that has the following keys

```json
{
    "SECRET_KEY":"<secret_key>",
    "USERNAME":"<root>",
    "PASSWORD":"<password>",
    "ROOT_URL":"http://<ip_of_database>:<port>",
    "DATABASE":"<databasename>",
    "REF_FILES":"<folder_of_reference_cases>"
}
```

Secret key is a randomly generated string which is used to encrypt the session data. provide the username and password which have access on the database created in orientDB server. The ROOT_URL includes the ip address of the deployment node of database and its port. Usually the port is set to 2480 unless you customized it when running the orientdb server. If you are running everything locally then the ip would be localhost. REF_FILES is required for QuCMixx which access a set of documents for use cases where it find detailed description of them

Now we start the terimnal and move to the folder of each service to lanuch them.

```console
cd $Repositroy/QuCMixx
python ./app.py config.json
```
The config file could be located somewhere else. please provide the full path in this case and follow the explained templates. Missing those keys will not let the service start correctly.

## QuCface
If you are running QuCMixx on localhost, then you just need to open the hello.html file. Otherwise you need to replace the localhost in HTML/js code with the deployed IP address of QuCMixx

## Docker containers
