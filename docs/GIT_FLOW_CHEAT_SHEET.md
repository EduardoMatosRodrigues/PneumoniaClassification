# Git flow cheat sheet
## References:
### Git flow model
 * [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
 * ["git flow" vs. "git"](https://gist.github.com/JamesMGreene/cdd0ac49f90c987e45ac)
 * [Getting Started with GitFlow](https://www.red-gate.com/simple-talk/devops/tools/getting-started-with-gitflow/)
### Commits
 * [Conventional Commits
](https://www.conventionalcommits.org/en/v1.0.0/) (This convention is required for automated changelog generation to work with the Commitzen tool. This convention must be used in the GIT_COMMIT_MESSAGE variables)

---
# Initialise
> git init  
> git checkout -b master  
> git remote add origin REMOTE_REPOSITORY_URL`  
> git add .  
> git commit -m "first commit"  
> git push -u origin master  
> git checkout -b develop master
---
# Feature
## Start
> git checkout -b feature/FEATURE_BRANCH_NAME develop`  

## Save changes:
> git checkout feature/FEATURE_BRANCH_NAME  
> git commit -m GIT_COMMIT_MESSAGE  
> git push origin feature/FEATURE_BRANCH_NAME  

## Finish:
> git checkout develop  
> git merge --no-ff feature/FEATURE_BRANCH_NAME  
> git branch -d feature/FEATURE_BRANCH_NAME  
> git push origin develop  
---