git stash save
git checkout master
git branch -D v100
git pull
git checkout v100
sh scripts/install_requirements.sh
