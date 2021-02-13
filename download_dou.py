#!/usr/bin/env python
# coding: utf-8

import requests
import http.cookiejar as cookie
import re
import os
import json
import certifi


path_base = os.getcwd()

def config():
    try:
        with open('config/auth.json') as json_file:
            autenticacao = json.load(json_file)
        with open('config/params.json') as json_file:
            param = json.load(json_file)
        os.chdir(param.get("diretorio"))
        return autenticacao,param
    except:
        print("Falha ao tentar acessar o diretório de configurações") 

def get():
    autenticacao,param = config()
    ano_mes_dia = param.get("ano")+'-'+param.get("mes")+'-'+param.get("dia")
    file = ano_mes_dia+'-'+param.get("tipos_dou")[0]+'.zip'
    param.get("url_download").replace("$ano_mes_dia",ano_mes_dia).replace("$file",file)
    headers = {'origem': param.get("origem")}
    res = requests.session()
    res.verify = certifi.where() #"../../imprensa_nacional.cer"
    res.post(param.get("url_login"), data=autenticacao, headers=headers, cookies=cookie.CookieJar(),verify=False)
    ct = res.get(param.get("url_download").replace("$ano_mes_dia",ano_mes_dia).replace("$file",file))
    open(file, 'wb').write(ct.content)
    res.get(param.get("url_logout"))
    os.chdir(path_base)