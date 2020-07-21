git stash save
git checkout master
git branch -D v10_rc
git pull
git checkout v10_rc
sh scripts/install_requirements.sh
