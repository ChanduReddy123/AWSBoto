#!/bin/bash
#This script will give the size of each and every bucket in your account 

aws s3 ls | awk '{print $3}' > BucketList

while IFS= read -r BucketName;do

echo -n $BucketName;  aws s3 ls s3://$BucketName --recursive --human-readable --summarize | grep "Total Size"
done < BucketList

rm BucketList
