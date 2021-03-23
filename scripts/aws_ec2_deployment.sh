git stash save
git checkout master
git branch -D v100-aws-apps
git pull
git checkout v100-aws-apps
supervisorctl restart ofd-backend
