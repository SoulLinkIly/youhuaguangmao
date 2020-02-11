def GetInit():
    import requests
    import json
    headers={}
    ALL={}
    headers['cookie'] = 'sysauth=ba005573b651bdc77b17cd1db9c8d954'
    payload = {"token":"e002daf20ab5325c2dcced0310c0d343"}
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
    ret = {}
    response = requests.request("GET", 'http://192.168.1.1/cgi-bin/luci/admin/allInfo', headers=ALL['headers'], data=ALL['payload'],allow_redirects=False)
    if response.text[2:5] != "pc1" :
        ret.update(new=True)
        url = "http://192.168.1.1/cgi-bin/luci"
        payload = {"username":"useradmin","psd":"1234567"}

        response = requests.request("POST", url, headers=headers, data = payload,allow_redirects=False)
        spam = requests.utils.dict_from_cookiejar(response.cookies)
        if 'sysauth' in spam.keys():
            cookie = requests.utils.dict_from_cookiejar(response.cookies)['sysauth']
            headers['cookie'] = 'sysauth='+cookie
            response = requests.request("GET", url, headers = headers,allow_redirects=False)
            token = response.text[1503:1535]
            
            self_file = open('./友华光猫.ipynb',"r+", encoding='UTF-8')
            i = 0
            seek_num = 0
            for line in self_file:
                i=i+1
                if line.find('cookie') >=0 :
                    seek_num = seek_num + line.find('sysauth=') + 8
                    break
                seek_num = len(line) + seek_num
            self_file.seek(seek_num)
            self_file.write(cookie)
            self_file.seek(seek_num+70)
            self_file.write(token)
            self_file.close()
            
            headers["Referer"] = "http://192.168.1.1/cgi-bin/luci/"
            payload = {"token":token}
            ret.update(act=True)
            ret.update(headers=headers)
            ret.update(payload=payload)
            print("New!")
            print("cookie:"+cookie)
            print("token:"+token)
            return ret
        else:
            ret.update(act=False)
            return ret
    else:
        print("cookie:"+headers["cookie"])
        print("token:"+payload["token"])
        ret.update(act=True)
        headers["Referer"] = "http://192.168.1.1/cgi-bin/luci/"
        ret.update(headers=headers)
        ret.update(payload=payload)
        return ret

def NewCopyMove(olddirname,newdirname,act,ALL,filename='*',folder=True,w=1):
    import requests
    import json
    result = {} #所有的文件 
    ALL['payload']['path']=olddirname

    if filename=='*':
        if w > 0 :
            url = "http://192.168.1.1/cgi-bin/luci/admin/storage/openFolder"
            response = requests.request("POST", url, headers=ALL['headers'], data=ALL['payload'], allow_redirects=False)
            jsonR = json.loads(response.text)
            for k in jsonR.keys() :
                if type(jsonR[k]).__name__ == 'dict' :
                    NewCopyMove(olddirname,newdirname,act,ALL,filename=jsonR[k]["name"],folder=jsonR[k]["isFolder"],w=w-1)
        else:
            print("文件名错误！")
    else:
        if folder :
            ALL['payload']['opstr'] = act+"|"+olddirname+"|"+newdirname+"|"
            ALL['payload']['fileLists']=filename+"/"
        else:
            ALL['payload']['opstr'] = act+"|"+olddirname+"|"+newdirname+"|"+filename
            ALL['payload']['fileLists']=filename+"/"
    url = "http://192.168.1.1/cgi-bin/luci/admin/storage/copyMove"
    response = requests.request("POST", url, headers=ALL['headers'], data=ALL['payload'], allow_redirects=False)
    #print(response.text)
    New_dict = NewOpenFolder(newdirname,ALL,n = 1,w=1)
    ret = False
    del New_dict["ret"]
    del New_dict["dirname"]
    del New_dict["layer"]
    for name in New_dict:
        if name[name.find('|')+1:] == filename:
            ret = True
            break
    return ret

def NewOpenFolder(dirname,ALL,n = 1,d = 0,w=1):
    import requests
    import json
    ALL['payload']['path']=dirname
    url = "http://192.168.1.1/cgi-bin/luci/admin/storage/openFolder"
    response = requests.request("POST", url, headers=ALL['headers'], data=ALL['payload'], allow_redirects=False)
    jsonR = json.loads(response.text)
    result={}
    result.update(ret=False)
    result.update(layer=0)
    for k in jsonR.keys() :
        if type(jsonR[k]).__name__ == 'dict' :
            if jsonR[k]["isFolder"] :
                dic = {
                    dirname+"/"+"{0}|".format(n)+jsonR[k]["name"] : True
                }
                result.update(dic)
                if w > 1 :
                    dic = NewOpenFolder(dirname+"/"+jsonR[k]["name"],ALL,n+1,d,w - 1)
                    if dic['ret']:
                        dic = {
                            dirname+"/"+"{0}|".format(n)+jsonR[k]["name"] : dic
                        }
                        result.update(dic)
            else:
                dic = {
                    dirname+"/"+"{0}|".format(n)+jsonR[k]["name"] : False
                }
                result.update(dic)
            if result['layer'] < w:
                result.update(layer=w)
            result.update(dirname=dirname)
            result.update(ret=True)
    return result

def ReadNewOpenFolder(ret):
    import requests
    import json
    if ret["ret"]:
        del ret["ret"]
        dirname = ret["dirname"]
        del ret["dirname"]
        layer_max = ret['layer']
        del ret["layer"]
        for name in ret:
            for i in range(0,int(name[len(dirname)+1:name.find('|')])-1):
                print("    ",end="")
            if type(ret[name]) == bool:
                if ret[name]:
                    print("|d ",end="")
                else:
                    print("|f ",end="")
                print(name[name.find('|')+1:])
            elif type(ret[name]) == dict:
                print("|d ",end="")
                print(name[name.find('|')+1:])
                if ReadNewOpenFolder(ret[name]) == False:
                    print("有错误！")
                    exit()
        return True
    else:
        return False

ALL = GetInit()
if ALL['act']:
    del ALL['act']
    olddirname = '/mnt/usb1_2/../../opt/upt/apps/youhua'
    filename = 'lastgood.xml'
    folder = True
    newdirname = '/mnt/usb1_2'
    act='"whoami'

    print("源目录：")
    ReadNewOpenFolder(NewOpenFolder(olddirname,ALL,w=1))

    print("原目标目录：")
    ReadNewOpenFolder(NewOpenFolder(newdirname,ALL,w=1))

    if NewCopyMove(olddirname,newdirname,act,ALL,filename,folder,w=1):
        print("复制后目标目录：")
        ReadNewOpenFolder(NewOpenFolder(newdirname,ALL,w=1))
        print("复制成功！")
    else:
        print("复制后目标目录：")
        ReadNewOpenFolder(NewOpenFolder(newdirname,ALL,w=1))
        print("复制失败！")

ALL = GetInit()

if ALL['act']:
    del ALL['act']
    #newdirname = '/mnt/../dev/bus/usb/../../../tmp'
    #NewOpenFolder(newdirname,ALL,w=1)
    print("")
    dirname = '/mnt/usb1_2'
    ret = NewOpenFolder(dirname,ALL,w=1)
    ReadNewOpenFolder(ret)
    print(ret)