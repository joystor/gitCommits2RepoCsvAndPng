import datetime, time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# git log --all --author="Joys" > all_commits_by_user.txt
file_input = "all_commits_by_user.txt"
file_output = "commits_table.csv"

# CONFIGURATION VARS
browser_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
user_data_chrome = "--user-data-dir=C:/Users/USERNAME/AppData/Local/Google/Chrome/User Data/"
git_url = 'https://GITURL_USER_REPO/commits/'

dt_format = '%a %b %d %H:%M:%S %Y %z'

f = open(file_input, "r", encoding="utf8")
commit = ""
date = ""
desc = ""
cmts = {}
dt = None
for line in f:
  
  if "commit" in line:
    if date is not "" and commit is not "" and desc is not "":
      if dt is not None:
        key = "{}_{}".format(dt.year, dt.month)
      if key not in cmts:
            cmts[key] = []
      cmts[key].append("{}|{}|{}".format(date,desc,commit))
      #print("{}|{}|{}".format(date,desc,commit))
      commit = ""
      date = ""
      desc = ""
      dt = None
    commit = line.replace("commit ","").replace("\n","").strip()
  if "Date:   " in line:
    date = line.replace("Date:   ","").replace("\n","")
    dt = datetime.datetime.strptime(date, dt_format)
  if line.startswith("    ") and "Merge branch '" not in line:
    desc = "{} {}".format(desc, line.replace("    ","").replace("\n",""))
	
if dt is not None:
  key = "{}_{}".format(dt.year, dt.month)
if key not in cmts:
  cmts[key] = []
cmts[key].append("{}|{}|{}".format(date,desc,commit))




options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument(user_data_chrome)
browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
#browser.set_window_size(1800, 900)

try:
  os.remove(file_output)
except:
  pass

file = open("{}".format(file_output),"w+")

for key in cmts:
  cmts[key].sort()
  for l in cmts[key]:
    print("{}|{}".format(key,l))
    commit = l.split("|")[2]
    url = git_url + commit
    browser.get(url)
    time.sleep(6)
    browser.save_screenshot("screenshot_git_" + "_" + key + "_"+ commit + ".png")
    file.write(key+"|"+l + "\n")

file.close()
browser.close()