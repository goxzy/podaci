from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from urllib.parse import urlparse
conn=sqlite3.connect('db.sqlite')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS poljoprivrednici')
cur.execute('''CREATE TABLE poljoprivrednici(
    naziv text,
    HR real,
    EU real
)''')
url='http://isplate.apprrr.hr/godina/2016'
url1='http://isplate.apprrr.hr'
count=0
grad=input("Unesi ime grada za koji te zanimaju potpore:")
pagei=int(input("Unesi broj stranica:"))
for x in range (1,pagei):
    r=requests.get(url,params={'page':x,'grad':grad})
    data=r.text
#print(data)
    soup=BeautifulSoup(data,'html.parser')
    for link in soup.find_all('a'):
        url2=urlparse(link.get('href'))
        if url2.path.startswith('/godina/2016/korisnik/'):
            dodatak=str(url2.path)
        else:
            continue
        count+=1
        print(count)
        url3=url1+dodatak
        r1=requests.get(url3)
        podaci_poljoprivrednik=r1.text

        soup1=BeautifulSoup(podaci_poljoprivrednik,'html.parser')
        for item in soup1.find_all('li'):

            if item.text.startswith('Naziv:'):
                podjela=item.text.split()
                try:
                    naziv=podjela[1]+' '+podjela[2]
                    print(naziv)
                except:
                    naziv=podjela[1]

        for item in soup1.find_all('td'):
            if item.text=='Program osnovnih plaćanja':
                indexic=soup1.find_all('td').index(item)
                p_iznos_HR=soup1.find_all('td')[indexic+2]
                p_iznos_EU=soup1.find_all('td')[indexic+3]
                p_iznos_EU1=p_iznos_EU.text.rstrip(' HRK')
                p_iznos_HR1=p_iznos_HR.text.rstrip(' HRK')
                a_iznos_HR=p_iznos_HR1.replace(".","")
                a_iznos_EU=p_iznos_EU1.replace(".","")
                iznos_HR=a_iznos_HR.replace(',','.')
                iznos_EU=a_iznos_EU.replace(',','.')
                print(iznos_HR)
                print(iznos_EU)
                cur.execute('INSERT INTO poljoprivrednici (naziv,HR,EU) VALUES(?,?,?)',(naziv,iznos_HR,iznos_EU))
conn.commit()
conn.close()
