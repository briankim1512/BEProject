# Back-end Project for Fullstacks Nanodegree @ Udacity

The orignal code for the vagrant file has been pulled from a git repo
cited in the CODEOWNERS file. All original creators have been cited
within that file.
=============

## Installing
In order to run this file, you must have the following programs installed

```
Vagrant: https://www.vagrantup.com/docs/installation/
```

Once vagrant is installed or you already have vagrant, navigate to this directory
where this file is located in through a terminal and type:

```
vagrant up
vagrant ssh
```

Once complete, cd into /vagrant and run the python code "DBSetup.py" and 
"initDBEntries.py" by typing:

```
python DBSetup.py
python initDBEntries.py
```

WARNING: ONLY EXECUTE initDBEntries.py ONCE OR ELSE YOU WILL GET DUPLICATES
=============

## Running the server
To run the server, run:

```
python server.py
```

into the terminal and connect to the server by using your localhost IP and
port 8080. (Make sure you're doing this through the vagrant ssh instance.)