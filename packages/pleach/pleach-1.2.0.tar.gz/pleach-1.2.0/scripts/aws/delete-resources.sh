# aws cloudformation delete-stack --stack-name PleachAppStack
aws ecr delete-repository --repository-name pleach-backend-repository --force
# aws ecr delete-repository --repository-name pleach-frontend-repository --force
# aws ecr describe-repositories --output json | jq -re ".repositories[].repositoryName"