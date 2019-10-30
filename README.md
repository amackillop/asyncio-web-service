# An Asyncronous Web Service
The original purpose of this application was mostly for me to experiment with 
asynchronous programming in python and to learn best practices. The service 
consumes jobs that consist of a list of urls of images to be downloaded and 
stored somewhere. The service also allows users to query the live state of any 
running job to see for example, how many images are left to be downloaded or 
which images failed.

## Requirements
All that you should need is `docker` and a system capable of running `make`.

## Quickstart
To build and run the app locally, simply use:  
```make build run```

This will build and launch the necessary docker containers. You can then hammer
the app with the `spam` script. For example,    
```./spam 1000```  
Will send a thousand jobs to the application for processing.

You can query the status of any job via the following enpoint:  
```curl localhost:8000/v1/jobs/<job_id>```