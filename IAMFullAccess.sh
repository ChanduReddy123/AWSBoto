#! /bin/bash
aws iam list-users | jq  '.Users | .[].UserName' users | sed 's/"//g' > AWSUsers
while IFS= read -r line;do
if [ $(aws iam list-attached-user-policies --user-name $line  | jq  ' .AttachedPolicies  | select(.[].PolicyName=="IAMFullAccess")'| wc -l) -gt 3 ]
then
echo $line
fi
done < AWSUsers
rm AWSUsers
