import jenkins
import sys
import os, glob
import requests

#simply script to authenticate with Jenkins via CLI, make tree of all jobs/branches and delete logs older than last 30 number, by this script you can save a lot of space 
#please remember set jenkins-cli.jar in location, in this version in /tmp

server = jenkins.Jenkins('http://<192.168.0.1>:8080', username='<your_username>', password='<your_password>')

def project_list():
    project_path = "/jenkins/jobs/"
    return os.listdir(project_path)


def branches_list(job_name):
    list = server.get_job_info(job_name)['jobs']
    list_branch = []
    for branch in range(len(list)):
       job_branch = list[branch]['name']
       prepare_list_to_delete(job_name,job_branch)


def prepare_list_to_delete(job_name,job_branch):
    last_build_number = server.get_job_info(f"{job_name}/{job_branch}", fetch_all_builds=True)['lastBuild']
    if last_build_number is not None and last_build_number['number'] > 30:
     delete_logs(job_name,job_branch,last_build_number['number'] - 30)


def delete_logs(job_name,job_branch,delete_to_buld_number):
    cmd = "/usr/bin/java -jar /tmp/mateusz/jenkins-cli.jar" + " " + "-s" + " " + "http://192.168.0.1:8080" +" "  + "delete-builds" + " " + job_name + "/" + job_branch + " " + "1" + "-" + str(delete_to_buld_number)
    print(f"Clean up {job_name}:{job_branch}")
    os.system(cmd)


def remove_old_logs():
    for job_name in project_list():
     branches_list(job_name)


remove_old_logs()
