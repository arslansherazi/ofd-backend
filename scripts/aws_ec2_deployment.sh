git stash save
git checkout master
git branch -D v100-aws
git pull
git checkout v100-aws
supervisorctl restart ofd-backend
