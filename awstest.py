import os
import boto3

# note, in part 2 we will move these to a separate .env file so they
# aren't accidentally published in a public repository.
os.environ["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"]
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
#next is elk stack

userdata = """#!/bin/bash
yum update -y
wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
rpm --import http://pkg.jenkins-ci.org/redhat-stable/jenkins-ci.org.key
yum install jenkins -y
service jenkins start
chkconfig jenkins on


"""


ec2 = boto3.resource('ec2')
instances = ec2.create_instances(
    ImageId='ami-7172b611',
    InstanceType='t2.micro',
    KeyName='AWS_Testing',
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['Jenkins'],
    UserData=userdata
)

for instance in instances:
    print("Waiting until running...")
    instance.wait_until_running()
    instance.reload()
    print((instance.id, instance.state, instance.public_dns_name,
instance.public_ip_address))