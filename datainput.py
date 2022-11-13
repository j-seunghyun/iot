import json
import asyncio
import requests_async as requests
import xmltodict
import base64

inputyear = input('검색할 년도를 입력해주세요 : ')
inputmonth = input('검색할 월을 입력해주세요 : ')

#sortdate는 년도의 뒷 2자리와 month를 더하면 된다.
sortdate = str(inputyear[2:]+inputmonth)
posthost = 'https://2anzgv6hl5.execute-api.ap-northeast-1.amazonaws.com/default/holidayPost'
gethost = 'https://p73z2wd1h8.execute-api.ap-northeast-1.amazonaws.com/default/holidayGet'
inputparams = {
  "sortdate": sortdate,
}

url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
params ={'serviceKey' : 'TYFoFL5xQ9HzUXRHT4Igl4rlNnwb7UVLbdrMQ6qgKA2ov05yY1zRMB7JP2EXChEquf8z9neJevoZvlyr76QIPA==', 'solYear' : inputyear, 'solMonth' : inputmonth}

async def req():
  response = await requests.get(gethost, params=inputparams)
  inputdata = json.loads(response.content)
  
  #리스트가 비어져 있는지 아닌지 확인
  #리스트가 비어져 있을 때
  if not inputdata:
    response = await requests.get(url,params=params)
    #print(response.content)
    data = json.loads(json.dumps(xmltodict.parse(response.content), indent=3))
    #print(data)
    datacount = int(data['response']['body']['totalCount'])
    data_list = data['response']['body']['items']['item']
  
    #datacount가 1일 경우는 data_list자체를 data로 보내준다.
    if datacount == 1:
      data_list['sortdate'] = sortdate
      response = await requests.post(posthost, data=data_list, headers=None)
      print(response)
    else:
      for datas in data_list:
        #datas json에 sortdate키 값 플러스 한 후 전송
        datas['sortdate'] = sortdate
        response = await requests.post(posthost, data=datas, headers=None)
        data = json.loads(response.content)
  
  #데이터베이스에 sortdate에 대한 결과가 존재할때에 
  else:
    print(json.dumps(inputdata, ensure_ascii=False, indent = 3))
    
asyncio.run(req())