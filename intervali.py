import sqlite3

intervali={'0,5000':[],'5001,10000':[],'10001,20000':[],'20001,50000':[],'50001,100000':[],
'100001,200000':[],'200001,300000':[],'300001,400000':[],'400001,500000':[],'500001,600000':[]}
conn=sqlite3.connect('poljoprivrednici_potpore_gradec.sqlite')
cur=conn.cursor()
for row in cur.execute('SELECT * FROM poljoprivrednici'):
    hr_iznos=float(row[1])
    eu_iznos=float(row[2])
    zbroj=hr_iznos+eu_iznos
    zbroj1=int(zbroj)
    for key in intervali:
        a=key.split(',')
        donja_granica=int(a[0])
        gornja_granica=int(a[1])
        if zbroj1 in range(donja_granica,gornja_granica):
            intervali[key].append(zbroj)

for key in intervali:
    print(key,len(intervali[key]),sum(intervali[key]))
