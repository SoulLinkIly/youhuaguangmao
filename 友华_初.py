def GetInit():
    url = "http://192.168.1.1/cgi-bin/luci"
    ret = {}
    payload = {"username":"useradmin","psd":"1234567"}
    headers = {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Content-Length': '68',
      'Content-type': 'application/x-www-form-urlencoded',
      'DNT': '1',
      'Host': '192.168.1.1',
      'Origin': 'http://192.168.1.1',
      'Referer': 'http://192.168.1.1/cgi-bin/luci',
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data = payload,allow_redirects=False)
    spam = requests.utils.dict_from_cookiejar(response.cookies)
    if 'sysauth' in spam.keys():
        cookie = requests.utils.dict_from_cookiejar(response.cookies)['sysauth']
        headers['cookie'] = 'sysauth='+cookie
        response = requests.request("GET", url, headers = headers,allow_redirects=False)
        if response.text[1495:1500] == "token" :
            token = response.text[1503:1535]
            headers["Referer"] = "http://192.168.1.1/cgi-bin/luci/"
            payload = {"token":token}
            ret.update(act=True)
            ret.update(headers=headers)
            ret.update(payload=payload)
            return ret
    else:
        ret.update(act=False)
        return ret

def NewOpenFolder(dirname,files,ALL,n = 1,w=1):
    ALL['payload']['path']=dirname
    url = "http://192.168.1.1/cgi-bin/luci/admin/storage/openFolder"
    response = requests.request("POST", url, headers=ALL['headers'], data=ALL['payload'], allow_redirects=False)
    jsonR = json.loads(response.text)
    #print(jsonR)
    return all_run(dirname,files,jsonR,ALL,n,w)

def NewCopyMove(olddirname,filename,newdirname,ALL,w=1):
    ALL['payload']['opstr'] = act+"|"+olddirname+"|"+newdirname+"|"
    ALL['payload']['fileLists']=filename+"/"
    url = "http://192.168.1.1/cgi-bin/luci/admin/storage/copyMove"
    response = requests.request("POST", url, headers=ALL['headers'], data=ALL['payload'], allow_redirects=False)
    jsonR = json.loads(response.text)
    #print(jsonR)
    return all_run(dirname,jsonR,ALL,n,w)

def all_run(dirname,files,jsonR,ALL,n = 1,w = 1):
    result = {} #所有的文件 
    f = 1
    d = 1
    for k in jsonR.keys() :
        #folder = json.loads(json[k])
        if type(jsonR[k]).__name__ == 'dict' :
            #print(jsonR[k]['name'])
            
            if jsonR[k]["isFolder"] :
                value = "n{0}d{1}".format(n,d)
                d = d+1
                dic = {
                    value : jsonR[k]["name"]
                }

                result.update(dic)
                for i in range(1,n):
                    print(" ",end='',file=files)

                print("|d ",end='',file=files)
                print(jsonR[k]["name"]+"\n",end='',file=files)
                if w != 1 :
                    dic = {
                        value+"-"+jsonR[k]["name"] : NewOpenFolder(dirname+jsonR[k]["name"]+"/",files,ALL,n+1,w - 1)
                    }
                result.update(dic)
            else:
                value = "n{0}f{1}".format(n,f)
                dic = {
                    value : jsonR[k]["name"]
                }
                for i in range(1,n):
                    print(" ",end='',file=files)
                    
                print("|f ",end='',file=files)
                print(jsonR[k]["name"]+"\n",end='',file=files)
                result.update(dic)
                f = f+1
    print(".",end="")
    return result

def PrintJsonR (jsonr):
    for k in jsonr.keys():
        if type(jsonr[k]).__name__ == "dict" :
            PrintJsonR (jsonr[k])
        else:
            print(jsonr[k])

import requests
import json
import linecache

headers={}
ALL={}
headers['cookie'] = 'sysauth=fcf73e7ac4e91684a9c020ec7f28f68f'
payload = {"token":"18f6fb322c724350dbd9874b087bd94e"}

headers.update({
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Content-Length': '68',
  'Content-type': 'application/x-www-form-urlencoded',
  'DNT': '1',
  'Host': '192.168.1.1',
  'Origin': 'http://192.168.1.1',
  'Referer': 'http://192.168.1.1/cgi-bin/luci',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
})

ALL.update(headers=headers)
ALL.update(payload=payload)

response = requests.request("GET", 'http://192.168.1.1/cgi-bin/luci/admin/allInfo', headers=ALL['headers'], data=ALL['payload'],allow_redirects=False)
if response.text[2:5] != "pc1" :
    ALL = GetInit()
    print("New!")
else:
    ALL['act']=True
print("cookie:"+ALL['headers']['cookie'])
print("token:"+ALL['payload']['token'])
if ALL['act']:
    print("初始化成功！")
    print("loading",end="")
    files = open('./1.txt','a')
    jsonr = NewOpenFolder('//',files,ALL,w=1)
    #print(jsonr)
    #PrintJsonR (jsonr)
    files.close()
    print("完成！")
else:
    print("初始化失败！")

def ChangeToTreeView():
    f = open('ALL_NEW.txt')
    #lines = f.readlines()
    location_old = 0

    files=open('C:/Users/lch/Test/treeview/test/ALL_NEW1.html','w')
    a = 0
    hold = 0
    for lines in f:
        location = lines.find('|')+1
        print(location)

        line = lines.strip('\n')

        if location_old < location :
            space_num = location * 2 - 1
            if space_num >= 0 :
                print("",file=files)
                for num in range(0,space_num-1):
                    print("    ",end="",file=files)
                print("<ul>",file=files)
            for num in range(0,space_num):
                print("    ",end="",file=files)



        elif location_old == location :
            print("</li>",file=files)
            space_num = location * 2 - 1
            for num in range(0,space_num):
                print("    ",end="",file=files)



        elif location_old > location :
            print("</li>",file=files)

            for i in range(0,location_old - location):
                space_num = (location_old-1)*2
                for num in range(0,space_num):
                    print("    ",end="",file=files)
                print("</ul>",file=files)
                space_num = space_num - 1
                for num in range(0,space_num):
                    print("    ",end="",file=files)
                print("</li>",file=files)
                location_old = location_old - 1
            for num in range(0,space_num):
                print("    ",end="",file=files)

        location_old = location

        if lines[location] == "d":
            print("<li><span class='folder'>",end="",file=files)
            print(line[location+2:],end="",file=files)
            print("</span>",end="",file=files)
        elif lines[location] == "f":
            print("<li><span class='file'>",end="",file=files)
            print(line[location+2:],end="",file=files)
            print("</span>",end="",file=files)
    print("</li>",file=files)
    for i in range(0,location_old-1):
        space_num = (location_old-1)*2
        for num in range(0,space_num):
            print("    ",end="",file=files)
        print("</ul>",file=files)
        space_num = space_num - 1
        for num in range(0,space_num):
            print("    ",end="",file=files)
        print("</li>",file=files)
        location_old = location_old - 1
    print("</ul>",file=files)
    f.close()
    files.close()

