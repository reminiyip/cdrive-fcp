#### Basic Flow

If you're not using any branching (i.e. you only work on master branch), you can follow the below simple and basic Git flow.

###### Step 0: install git

```
brew install git  
git config --global user.name <your-name> 
git config --global user.email <your-email>
```  

###### Step 1: clone a project from GitHub

`git clone https://github.com/<your-username>/<repo>.git`  

###### Step 2: make some changes

...

###### Step 3: saving changes

```
git status                                 # show which files are modified  

git add <file/dir>                         # tells Git you wanna include updates to a particular file in the next commit  
                                           # (i.e. put them in staging area)
OR git add -A                             # you wanna include ALL updates in the next commit

git commit -m <message>                   # actually commits what you added to the staging area
                                           # please include a concise commit message
```

###### Step 4: get updates from remote

```
git pull origin master                     # before you push it to the remote repo, pull down the latest version first.
                                           # Git will try to merge them, but you need to resolve any conflicts introduced manually  
```

###### Step 4b: get updates from other repo (i.e. repos other than your own forked one)

```
git remote -v                              # show what remote names you have, usually you'll have an 'origin' remote repo  
                                           # that's where you cloned your repo from in Step 1  

git remote add <remote-name> <repo-url>    # add a remote repo, usually from the repo you forked from
                                           # usually name it 'upstream'  

git pull <remote-name> master
```

###### Step 4c: resolve conflicts (if any)

Git tells you which files are having conflicts like this:  

```
...
Auto-merging <file>
CONFLICT (content): Merge conflict in <file>
Automatic merge failed; fix conflicts and then commit the result.
...
```

Open that file, you'll see:

```
<<<<<<< HEAD
<your version of code>
=======
<remote version code>
>>>>>>> branch-a
```

Decide what to keep and remove all other stuffs. Then commit again.  

```
git add -A 
git commit -m <message>
```

###### Step 5: push commits to remote

```
git push origin master                     # push to the master branch
```

###### Step 6: make a pull request

If your remote repo is a forked one, and you would like to request the original repo to merge your changes, go to GitHub and press the button __New Pull Request__. This will send the pull request to the original repo, and the authorized users can decide whether to merge your changes, or abort.

#### References

- [Git Tutorial](https://www.atlassian.com/git/tutorials)
