import json,datetime
#datatime类型日期解码
class DateEncondingTool(json.JSONEncoder):
    def default(self,o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        else:  
            return json.JSONEncoder.default(o)
class DateEnconding():
    def date(self,datetimedate:datetime.date):
        return json.dumps(datetimedate, cls=DateEncondingTool) 

class Enconding():
    def enconding(self,data:list):
        #print(data,'\n')
        if(data==None):
            return data
        else:
            encodingdata=[]
            for datat in data:
                #datajson=DateEnconding().date(datat['ptime'])
                datajson=str(datat['ptime'])
                datat.pop('ptime') 
                datat['ptime']=datajson
                encodingdata.append(datat)

            return encodingdata


