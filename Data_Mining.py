import requests
import pandas as pd
import numpy as np
import datetime
import ast
from datetime import timezone
from Help_Func import *
from dateutil import parser
import time as wait_time




class OKEX_Data_Mining():                      #data mining based on v5 api, rest api
    def __init__(self):
        self.rest_api = "https://www.okex.com"
        self.Helper_Func = Help_Func()          #initial help_func
        self.request_feq = 20
        self.sleep_duration = 2
        self.bar_dic = self.Helper_Func.Make_bar_deltatime()
        self.dbefore = self.Helper_Func.Datetime_to_Timestamp(parser.parse("2017-01-01 00:00:00"))    #default datetime





    def Instruments(self, instType: str, uly=None, instld=None):
        ##确定最初接口
        url = self.rest_api + "/api/v5/public/instruments?"

        ##将用户参数加在url后面
        if instType == None:
            print("Error: instType can not be empty!!")
            return
        else:
            url = url + "instType=" + instType
        if uly != None:
            url = url + "&uly=" + uly
        if instld != None:
            url = url + "&instld=" + instld
        print('url = ', url)

        # 访问网站，将返回数据转换为dic
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        # 如果返回值错误，打印错误信息
        if dics["code"] != '0':
            print("Error: {}".format(dics["msg"]))
            return

        #将数据插入pandas dataframe， 并且做数据转换
        df = {}
        for dic in dics["data"]:
            for key in dic.keys():
                if key not in df.keys():
                    df[key] = []

                try:
                    temp = int(dic[key])
                    if key == "listTime" or key == "expTime":
                        temp = self.Helper_Func.Timestamp_to_UTCDatetime(temp)
                    df[key].append(temp)
                except:
                    try:
                        temp = float(dic[key])
                        df[key].append(temp)
                    except:
                        if dic[key] == '':
                            df[key].append(np.nan)
                        else:
                            df[key].append(dic[key])
        df = pd.DataFrame(df)
        return df

    def System_Time(self):
        url = self.rest_api + "/api/v5/public/time"
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            data = dics["data"]
            system_time = self.Helper_Func.Timestamp_to_UTCDatetime(int(data[0]["ts"]))
            print("System Time = ", system_time)
            return

    def Liquidation_Orders(self, instType, mgnMode = None, instId = None, ccy = None, uly = None, alias = None,
                           state = None, before = None, after = None, limit = None):
        print("Liquidation Orders is not finished!!!")
        return
        basic_url = self.rest_api + "/api/v5/public/liquidation-orders?"
        if instType not in ['MARGIN', 'SWAP', 'FUTURES', 'OPTION']:
            print("Error: instType is empty or instType is wrong!!")
            return
        else:
            basic_url = basic_url + "instType={}".format(instType)
        if mgnMode:
            basic_url = basic_url + "&mgnMode={}".format(mgnMode)
        if instId:
            basic_url = basic_url + "&instId={}".format(instId)
        if ccy:
            basic_url = basic_url + "&ccy={}".format(ccy)
        if uly:
            basic_url = basic_url + "&uly={}".format(uly)
        if alias:
            basic_url = basic_url + "&alias={}".format(alias)
        if state:
            basic_url = basic_url + "&state={}".format(state)
        if limit:
            basic_url = basic_url + "&limit={}".format(limit)


        # after 为请求此时间戳之前（更旧的数据）的分页内容
        if after == None:
            print("after = ", self.Helper_Func.Current_UTC_Datetime())
            after = self.Helper_Func.Datetime_to_Timestamp((self.Helper_Func.Current_UTC_Datetime()))


        # before 为请求此时间戳之后（更新的数据）的分页内容
        if before == None:
            dbefore = self.dbefore
            before = self.Helper_Func.Timestamp_Deltatime(after, datetime.timedelta(days=1), "-")
        else:
            dbefore = before
            before = self.Helper_Func.Timestamp_Deltatime(after, datetime.timedelta(days=1), "-")

        url = basic_url + "&after={}&before={}".format(after, before)
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        # 判断是否出错
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            matrix = np.array(dics["data"])
            df = pd.DataFrame(matrix.copy(),
                              columns=["time", "open", "high", "low", "close"])
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            data = dics["data"]
            system_time = self.Helper_Func.Timestamp_to_UTCDatetime(int(data[0]["ts"]))
            print("System Time = ", system_time)
            return
        return

    def Mark_Price(self, instType, uly=None, instId=None):
        url = self.rest_api + "/api/v5/public/mark-price?"
        if instType not in ['MARGIN', 'SWAP', 'FUTURES', 'OPTION']:
            print("Error: instType is empty or instType is wrong!!")
            return
        else:
            url = url + "instType={}".format(instType)
        if uly:
            url = url + "&uly={}".format(uly)
        if instId:
            url = url + "&instId={}".format(instId)

        # 访问网站，将返回数据转换为dic
        r = requests.get(url)
        dics = ast.literal_eval(r.text)
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        df = {}
        for dic in dics["data"]:
            for key in dic.keys():
                if key not in df.keys():
                    df[key] = []
                try:
                    temp = int(dic[key])
                    if key == "ts":
                        temp = self.Helper_Func.Timestamp_to_UTCDatetime(temp)
                    df[key].append(temp)
                except:
                    try:
                        temp = float(dic[key])
                        df[key].append(temp)
                    except:
                        if dic[key] == '':
                            df[key].append(np.nan)
                        else:
                            df[key].append(dic[key])
        df = pd.DataFrame(df)
        return df





    def Position_Tiers(self, instType, tdMode, uly = None, instId = None, ccy = None, tier = None):
        url = self.rest_api + "/api/v5/public/tier?"
        if instType not in ['MARGIN', 'SWAP', 'FUTURES', 'OPTION']:
            print("Error: instType is empty or instType is wrong!!")
            return
        else:
            url = url + "instType={}".format(instType)

        if tdMode not in ['isolated', 'cross']:
            print("Error: instType is empty or instType is wrong!!")
            return
        else:
            url = url + "&tdMode={}".format(tdMode)
        if uly:
            url = url + "&uly={}".format(uly)
        if instId:
            url = url + "&instId={}".format(instId)
        if ccy:
            url = url + "&ccy={}".format(ccy)
        if tier:
            url = url + "&tier={}".format(tier)

        # 访问网站，将返回数据转换为dic
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        df = {}
        for dic in dics["data"]:
            for key in dic.keys():
                if key not in df.keys():
                    df[key] = []
                try:
                    temp = int(dic[key])
                    if key == "ts":
                        temp = self.Helper_Func.Timestamp_to_UTCDatetime(temp)
                    df[key].append(temp)
                except:
                    try:
                        temp = float(dic[key])
                        df[key].append(temp)
                    except:
                        if dic[key] == '':
                            df[key].append(np.nan)
                        else:
                            df[key].append(dic[key])
        df = pd.DataFrame(df)

        return df


    def Mark_Price_Candlesticks(self, instId, after = None, before = None, bar = None, limit = None):
        ##确定最初接口
        basic_url = self.rest_api + "/api/v5/market/mark-price-candles?"

        ##将用户参数加在url后面
        if instId == None:
            print("Error: instId can not be empty!!")
            return

        #设置默认值
        if bar == None:
            bar = "1m"
        elif bar not in  self.bar_dic.keys():
            print("Error: granularity input wrongly")
            return False

        if limit == None:
            limit = 100

        #after 为请求此时间戳之前（更旧的数据）的分页内容
        if after == None:
            print("after = ", self.Helper_Func.Current_UTC_Datetime())
            after = self.Helper_Func.Datetime_to_Timestamp((self.Helper_Func.Current_UTC_Datetime()))
        dafter = after

        #before 为请求此时间戳之后（更新的数据）的分页内容
        if before == None:
            dbefore = self.dbefore
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar]*limit, "-")
        else:
            dbefore = before
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(dbefore)
        print("D_before= ", datetime)

        #建立第一次访问数据
        url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        #判断是否出错
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            matrix = np.array(dics["data"])
            df = pd.DataFrame(matrix.copy(),
                              columns=["time", "open", "high", "low", "close"])

        after = before
        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
        print("after = ", datetime)
        before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar]*limit, "-")
        feq_count = 0
        #循环访问到dbefore数据集
        while after > dbefore:
            if feq_count == self.request_feq:
                print("I need to sleep for a little while!")
                wait_time.sleep(self.sleep_duration)
                feq_count = 0
            else:
                feq_count = feq_count + 1
            url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
            print("url = ", url)
            r = requests.get(url)
            # print("dics = ", dic)
            dics = ast.literal_eval(r.text)

            if dics["code"] != "0":
                print("Error: ", dics)
                return
            else:
                if dics["data"]:
                    matrix = np.array(dics["data"])
                    df2 = pd.DataFrame(matrix.copy(),
                                      columns=["time", "open", "high", "low", "close"])
                    df = df.append(df2, ignore_index=True)
                else:
                    print("The Exchange have no data for {} between {} and {}".format(instId, self.Helper_Func.Timestamp_to_UTCDatetime(after),
                                                                                      self.Helper_Func.Timestamp_to_UTCDatetime(before)))
                    break
            after = before
            datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
            print("after = ", datetime)
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        #格式数据转换
        for i in df.columns:
            try:
                df = df.astype({i: 'float'})
            except:
                pass
        df['time'] = pd.to_datetime(df["time"],  unit='ms')

        # 最后将数据集切掉多余的一小部分
        df = df.loc[(df["time"] >= dbefore) & (df["time"] <= dafter)].copy()
        df['time'] = pd.to_datetime(df["time"], unit='ms')
        return df


    def Candlesticks_History(self, instId, after = None, before = None, bar = None, limit = None):
        ##确定最初接口
        basic_url = self.rest_api + "/api/v5/market/history-candles?"

        ##将用户参数加在url后面
        if instId == None:
            print("Error: instId can not be empty!!")
            return

        # 设置默认值
        if bar == None:
            bar = "1m"
        elif bar not in self.bar_dic.keys():
            print("Error: granularity input wrongly")
            return False

        if limit == None:
            limit = 100

        # after 为请求此时间戳之前（更旧的数据）的分页内容
        if after == None:
            print("after = ", self.Helper_Func.Current_UTC_Datetime())
            after = self.Helper_Func.Datetime_to_Timestamp((self.Helper_Func.Current_UTC_Datetime()))

        # before 为请求此时间戳之后（更新的数据）的分页内容
        if before == None:
            dbefore = self.dbefore
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar]*limit, "-")
        else:
            dbefore = before
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(dbefore)
        print("D_before= ", datetime)

        dafter = after

        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(dafter)
        print("D_after= ", datetime)

        # 建立第一次访问数据
        url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        # 判断是否出错
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            matrix = np.array(dics["data"])
            df = pd.DataFrame(matrix.copy(),
                              columns=["time", "open", "high", "low", "close", "volume", "volCcy"])

        after = before
        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
        print("after = ", datetime)
        before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")
        feq_count = 0
        # 循环访问到dbefore数据集
        while after > dbefore:
            if feq_count == self.request_feq:
                print("I need to sleep for a little while!")
                wait_time.sleep(self.sleep_duration)
                feq_count = 0
            else:
                feq_count = feq_count + 1
            url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
            print("url = ", url)
            r = requests.get(url)
            # print("dics = ", dic)
            dics = ast.literal_eval(r.text)

            if dics["code"] != "0":
                print("Error: ", dics)
                return
            else:
                if dics["data"]:
                    matrix = np.array(dics["data"])
                    df2 = pd.DataFrame(matrix.copy(),
                                       columns=["time", "open", "high", "low", "close", "volume", "volCcy"])
                    df = df.append(df2, ignore_index=True)
                else:
                    print("The Exchange have no data for {} between {} and {}".format(instId,
                                                                                      self.Helper_Func.Timestamp_to_UTCDatetime(
                                                                                          after),
                                                                                      self.Helper_Func.Timestamp_to_UTCDatetime(
                                                                                          before)))
                    break
            after = before
            datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
            print("after = ", datetime)
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        # 格式数据转换
        for i in df.columns:
            try:
                df = df.astype({i: 'float'})
            except:
                pass

        #最后将数据集切掉多余的一小部分
        df = df.loc[(df["time"] >= dbefore) & (df["time"] <= dafter)].copy()
        df['time'] = pd.to_datetime(df["time"], unit='ms')
        return df


    def Index_Candlesticks(self, instId, after = None, before = None, bar = None, limit = None):
        ##确定最初接口
        basic_url = self.rest_api + "/api/v5/market/index-candles?"

        ##将用户参数加在url后面
        if instId == None:
            print("Error: instId can not be empty!!")
            return

        # 设置默认值
        if bar == None:
            bar = "1m"
        elif bar not in self.bar_dic.keys():
            print("Error: granularity input wrongly")
            return False

        if limit == None:
            limit = 100

        # after 为请求此时间戳之前（更旧的数据）的分页内容
        if after == None:
            print("after = ", self.Helper_Func.Current_UTC_Datetime())
            after = self.Helper_Func.Datetime_to_Timestamp((self.Helper_Func.Current_UTC_Datetime()))

        # before 为请求此时间戳之后（更新的数据）的分页内容
        if before == None:
            dbefore = self.dbefore
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar]*limit, "-")
        else:
            dbefore = before
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(dbefore)
        print("D_before= ", datetime)

        dafter = after

        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(dafter)
        print("D_after= ", datetime)

        # 建立第一次访问数据
        url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)

        # 判断是否出错
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            matrix = np.array(dics["data"])
            df = pd.DataFrame(matrix.copy(),
                              columns=["time", "open", "high", "low", "close"])

        after = before
        datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
        print("after = ", datetime)
        before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")
        feq_count = 0
        # 循环访问到dbefore数据集
        while after > dbefore:
            if feq_count == self.request_feq:
                print("I need to sleep for a little while!")
                wait_time.sleep(self.sleep_duration)
                feq_count = 0
            else:
                feq_count = feq_count + 1
            url = basic_url + "instId={}&after={}&before={}&bar={}&limit={}".format(instId, after, before, bar, limit)
            print("url = ", url)
            r = requests.get(url)
            # print("dics = ", dic)
            dics = ast.literal_eval(r.text)

            if dics["code"] != "0":
                print("Error: ", dics)
                return
            else:
                if dics["data"]:
                    matrix = np.array(dics["data"])
                    df2 = pd.DataFrame(matrix.copy(),
                                       columns=["time", "open", "high", "low", "close", "volume", "volCcy"])
                    df = df.append(df2, ignore_index=True)
                else:
                    print("The Exchange have no data for {} between {} and {}".format(instId,
                                                                                      self.Helper_Func.Timestamp_to_UTCDatetime(
                                                                                          after),
                                                                                      self.Helper_Func.Timestamp_to_UTCDatetime(
                                                                                          before)))
                    break
            after = before
            datetime = self.Helper_Func.Timestamp_to_UTCDatetime(after)
            print("after = ", datetime)
            before = self.Helper_Func.Timestamp_Deltatime(after, self.bar_dic[bar] * limit, "-")

        # 格式数据转换
        for i in df.columns:
            try:
                df = df.astype({i: 'float'})
            except:
                pass

        #最后将数据集切掉多余的一小部分
        df = df.loc[(df["time"] >= dbefore) & (df["time"] <= dafter)].copy()
        df['time'] = pd.to_datetime(df["time"], unit='ms')
        return df

    def Trades(self, instId, limit = None):
        ##确定最初接口
        basic_url = self.rest_api + "/api/v5/market/trades?"

        ##将用户参数加在url后面
        if instId == None:
            print("Error: instId can not be empty!!")
            return

        # 设置默认值
        if limit == None:
            limit = 500

       # 访问数据
        url = basic_url + "instId={}&limit={}".format(instId, limit)
        print("url = ", url)
        r = requests.get(url)
        dics = ast.literal_eval(r.text)
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        df = {}
        for dic in dics["data"]:
            for key in dic.keys():
                if key not in df.keys():
                    df[key] = []
                try:
                    temp = int(dic[key])
                    if key == "ts":
                        temp = self.Helper_Func.Timestamp_to_UTCDatetime(temp)
                    df[key].append(temp)
                except:
                    try:
                        temp = float(dic[key])
                        df[key].append(temp)
                    except:
                        if dic[key] == '':
                            df[key].append(np.nan)
                        else:
                            df[key].append(dic[key])
        df = pd.DataFrame(df)

        return df


    def Total_Volume(self):
        ##确定最初接口
        basic_url = self.rest_api + "/api/v5/market/platform-24-volume"
        print("url = ", basic_url)
        r = requests.get(basic_url)
        dics = ast.literal_eval(r.text)
        if dics["code"] != "0":
            print("Error: ", dics)
            return
        else:
            df = {}
            for dic in dics["data"]:
                for key in dic.keys():
                    if key not in df.keys():
                        df[key] = []
                    try:
                        temp = int(dic[key])
                        if key == "ts":
                            temp = self.Helper_Func.Timestamp_to_UTCDatetime(temp)
                        df[key].append(temp)
                    except:
                        try:
                            temp = float(dic[key])
                            df[key].append(temp)
                        except:
                            if dic[key] == '':
                                df[key].append(np.nan)
                            else:
                                df[key].append(dic[key])
            df = pd.DataFrame(df)
            print(df)
            return df