![Python application](https://github.com/amackillop/asyncio-web-service/workflows/Python%20application/badge.svg?branch=master)

# An Asyncronous Web Service
The original purpose of this application was mostly for me to experiment with 
asynchronous programming in python and to learn best practices. The service 
consumes jobs that consist of a list of urls of images to be downloaded and 
stored somewhere. The service also allows users to query the live state of any 
running job to see for example, how many images are left to be downloaded or 
which images have failed.

## Requirements
All that you should need is `docker` and a system capable of running `make`.

## Quickstart
To build and run the app locally, simply use:  
```make build run```

This will build and launch the necessary docker containers. You can then hammer
the app with the `spam` script. For example,    
```./spam 1000 localhost 8080```  
Will send a thousand jobs to the application for processing.

You can query the status of any job via the following endpoint:  
```curl localhost:8080/v1/jobs/<job_id>```


## Dojo

Github actions docs: https://help.github.com/en/actions
Workflow syntax: https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions

Feel free to use my repo to mess around on your own:

Clone: `git clone git@github.com:amackillop/asyncio-web-service.git`
Branch: `git branch <branch_name>`
Switch: `git switch <branch_name>`

Make changes to the `.github/workflows/pythonapp.yml` file then create a pull request to trigger the pipeline.
Alternatively, I can edit the workflow file on master to include your branch on push.