import os,re
direct = os.listdir("sprites/hero")
newd = []
for item in direct:
    newit = os.path.splitext("sprites/hero/"+item)
    newit = (re.sub('[()0-9]','',newit[0]))
    if newit.strip().split("/")[2] not in newd:
        newd.append(newit.strip().split("/")[2])
print(newd)
