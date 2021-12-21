# gitCommits2RepoCsvAndPng

Script in python to generate a CSV file and take screenshot of the commit to make Reports


 - Fist create a file with all commits: 

```
git log --all --author="Joys" > all_commits_by_user.txt
```

 - Modify the script with you data, url of the git repo and the Chrome user data if the git require passwords

```
python git_commits_2_repo_csv_and_png.py
```


The Script generate a CSV file and take png files of the screenshot of thegit commit with the name screenshot_git_*