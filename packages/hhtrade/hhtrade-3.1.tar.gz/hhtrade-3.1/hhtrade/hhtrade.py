import time
import pandas as pd
from tqsdk import TqApi, TqAuth, TqKq, TargetPosTask
from tqsdk.datetime import _cst_now,_get_trade_timestamp,_datetime_to_timestamp_nano,_convert_user_input_to_nano
from datetime import datetime,timedelta
import math
import numpy as np
from itertools import groupby
import random
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re
import requests
import json
import base64
import hmac
import hashlib
import time
import requests
from texttable import Texttable


offsetdict = {'ag': '今昨,开', 'rb': '今昨,开', 'hc': '今昨,开', 'fu': '今昨,开', 'ru': '今昨,开', 'au': '今昨,开', 'ao': '今昨,开', 'zn': '今昨,开', 'sp': '今昨,开', 'ni': '今昨,开', 'ss': '今昨,开', 'bu': '今昨,开', 'al': '今昨,开', 'cu': '昨开', 'sn': '今昨,开', 'pb': '今昨,开', 'br': '今昨,开', 'wr': '昨开', 'RM': '今昨,开', 'SA': '今昨,开', 'TA': '今昨,开', 'FG': '今昨,开', 'MA': '今昨,开', 'OI': '今昨,开', 'SR': '今昨,开', 'CF': '今昨,开', 'UR': '今昨,开', 'SM': '今昨,开', 'AP': '昨开', 'PF': '今昨,开', 'PK': '今昨,开', 'PX': '今昨,开', 'PR': '今昨,开', 'SH': '今昨,开', 'CJ': '今昨,开', 'SF': '今昨,开', 'CY': '今昨,开', 'RS': '今昨,开', 'm': '今昨,开', 'v': '今昨,开', 'i': '今昨,开', 'p': '今昨,开', 'y': '今昨,开', 'c': '今昨,开', 'jd': '今昨,开', 'pp': '今昨,开', 'eb': '今昨,开', 'l': '今昨,开', 'eg': '今昨,开', 'b': '今昨,开', 'jm': '昨开', 'lh': '昨开', 'pg': '今昨,开', 'a': '今昨,开', 'cs': '今昨,开', 'j': '昨开', 'fb': '今昨,开', 'rr': '今昨,开', 'bb': '今昨,开', 'si': '今昨,开', 'lc': '今昨,开', 'sc': '今昨,开', 'ec': '昨开', 'lu': '今昨,开', 'nr': '今昨,开', 'bc': '今昨,开', 'IM': '昨开', 'IF': '昨开', 'IC': '昨开', 'T': '今昨,开', 'TF': '今昨,开', 'TL': '今昨,开', 'IH': '昨开', 'TS': '今昨,开'}
traderoffice = {
'SHFE':'上海期货交易所',
'DCE':'大连商品交易所',
'CZCE':'郑州商品交易所',
'CFFEX':'中国金融交易所',
'INE':'上海能源中心(原油在这里)',
'SSE':'上海证券交易所',
'SZSE':'深圳证券交易所',
'GFEX':'广州期货交易所'
}




class orderclass:
    def __init__(self,api = None , targetposition = None, sendmail = None, sendmailpwd = None,  filename = None, ifbalancehis = False ):
        self.filename = 'traderecord_%s.txt'%datetime.now().strftime('%Y%m%d') if filename is None else filename
        self.log("%s 调用交易类"%datetime.now().strftime('%Y%m%d %H:%M:%S'))
        self.api = api
        self.recordacount()
        self.targetposition = targetposition
        self.oldposition = self.get_initposition()
        assert self.checkcorrectcode(), "请检查品种代码"
        self.setoffmethod = {}
        self.printposition()
        self.get_orderquote()
        self.sendmail = sendmail
        self.sendmailpwd = sendmailpwd
        self.ifbalancehis = ifbalancehis


    def dftotb(self,df):
        table = Texttable()
        table.set_cols_align(["c"]*len(df.columns.tolist()))
        table.set_cols_valign(["c"]*len(df.columns.tolist()))
        table.set_header_align(["c"]*len(df.columns.tolist()))
        # table.set_deco(Texttable.VLINES | Texttable.HLINES|Texttable.BORDER| Texttable.HLINES)
        table.set_deco(Texttable.HEADER|Texttable.VLINES)
        table.set_max_width( 0 )
        # 添加列名
        table.header(df.columns.tolist())
        # table.add_row(df.columns.tolist())
        # 添加数据行
        for row in df.values:
            table.add_row(row.tolist())
        # table.set_cols_valign('m')

        return table.draw()




    def balancehisorder(self):
        print("开始平昨")
        self.multibanlance()

    def sendmsg(self, access_token = None, secret=None, msg=None):
        timestamp = str(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        sign = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(sign).decode('utf-8')
        msg = {
            'msgtype': 'text',
            'text': {
                'content': msg
            }
        }
        webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token,
                                                                                                         timestamp,sign)
        response = requests.post(webhook_url, data=json.dumps(msg), headers={'Content-Type': 'application/json'})
        return response

    def sendorder(self, symbol= 'CFFEX.IF2409', number = 5, offset = 'CLOSE',direction = 'SELL'):
        quote = self.api.get_quote( symbol )
        dtnow = time.strftime('%H:%M:%S', time.localtime())
        dtdf = pd.DataFrame(quote['trading_time']["day"] + quote['trading_time']["night"])
        if ((dtdf[0] < dtnow) * (dtdf[1] > dtnow)).any():
            istrade = True
            order={}
            while True:
                self.api.wait_update()
                # 当行情有变化且当前挂单价格不优时，则撤单
                if order and direction == 'SELL':
                    overp = quote.bid_price1 > order.limit_price
                elif order and direction == 'BUY':
                    overp = quote.ask_price1 > order.limit_price

                if order and self.api.is_changing(quote) and order.status == "ALIVE" and overp:
                    print("价格改变，撤单重下")
                    self.api.cancel_order(order)
                # 当委托单已撤或还没有下单时则下单
                if (not order and self.api.is_changing(quote)) or (
                        self.api.is_changing(order) and order.volume_left != 0 and order.status == "FINISHED"):
                    print("下单: 价格 %f" % quote.bid_price1)
                    if direction == 'SELL':
                        order = self.api.insert_order(symbol= symbol , direction=direction, offset= offset,
                                                 volume = order.get("volume_left", number), limit_price=quote.bid_price1)
                    else:
                        order = self.api.insert_order(symbol= symbol , direction=direction, offset= offset,
                                                 volume = order.get("volume_left", number), limit_price=quote.ask_price1)
                if self.api.is_changing(order):
                    print("单状态: %s, 已成交: %d 手" % (order.status, order.volume_orign - order.volume_left))
                    if order.status == 'FINISHED':
                        break

    @staticmethod
    def fastsendorder( api = None ,symbol= 'CFFEX.IF2409', number = 5, offset = 'CLOSE',direction = 'SELL'):
        quote = api.get_quote( symbol )
        dtnow = time.strftime('%H:%M:%S', time.localtime())
        dtdf = pd.DataFrame(quote['trading_time']["day"] + quote['trading_time']["night"])
        if ((dtdf[0] < dtnow) * (dtdf[1] > dtnow)).any():
            istrade = True
            order={}
            while True:
                api.wait_update()
                # 当行情有变化且当前挂单价格不优时，则撤单
                if order and direction == 'SELL':
                    overp = quote.bid_price1 > order.limit_price
                elif order and direction == 'BUY':
                    overp = quote.ask_price1 > order.limit_price

                if order and api.is_changing(quote) and order.status == "ALIVE" and overp:
                    print("价格改变，撤单重下")
                    api.cancel_order(order)
                # 当委托单已撤或还没有下单时则下单
                if (not order and api.is_changing(quote)) or (
                        api.is_changing(order) and order.volume_left != 0 and order.status == "FINISHED"):
                    print("下单: 价格 %f" % quote.bid_price1)
                    if direction == 'SELL':
                        order = api.insert_order(symbol= symbol , direction=direction, offset= offset,
                                                 volume = order.get("volume_left", number), limit_price=quote.bid_price1)
                    else:
                        order = api.insert_order(symbol= symbol , direction=direction, offset= offset,
                                                 volume = order.get("volume_left", number), limit_price=quote.ask_price1)
                if api.is_changing(order):
                    print("单状态: %s, 已成交: %d 手" % (order.status, order.volume_orign - order.volume_left))
                    if order.status == 'FINISHED':
                        break
        else:
            print(f"{symbol}不在交易时间范围")




    def multibanlance(self):
        hisposition = self.api.get_position()
        for orderrow in hisposition.keys():
            pos_long_his = hisposition[orderrow]['pos_long_his']
            pos_short_his = hisposition[orderrow]['pos_short_his']
            hispos = abs(pos_long_his - pos_short_his)
            vol_ = min(pos_long_his, pos_short_his)
            if pos_long_his != 0 and pos_short_his != 0:
                self.sendorder(symbol=orderrow, number=vol_, offset='CLOSE', direction='SELL')
                self.sendorder(symbol=orderrow, number=vol_, offset='CLOSE', direction='BUY')


    def recordacount(self):
        self.log("当前%s 账户资金信息如下：" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
        d = self.api.get_account()
        accountinfo = pd.DataFrame([k, d[k]] for k in d.keys())
        accountinfo.columns = ['账户','值']
        accountinfo = self.dftotb(df = accountinfo )
        # accountinfo.to_csv(self.filename, mode='a', sep='|', index=False, encoding='gbk')
        self.log(accountinfo)

    def sendmailto(self, body = None, subject = None ):
        try:
            msg = body + subject
            self.sendmsg( access_token = self.sendmail , secret= self.sendmailpwd, msg = msg)
        except:
            pass


    def log(self, recordtxt = None):
        with open(self.filename,'a') as f:
            f.write(recordtxt+ '\n')


    def checkcorrectcode(self):
        if len(self.targetposition.keys()) == 0:
            self.targetposition = {}
            for key in self.oldposition.keys():
                self.targetposition[key] = 0
            return True

        for k in self.targetposition.keys():
            try:
                quote = self.api.get_quote(k)
            except:
                print(f"{k} 查询合约服务报错 ,请检查品种代码")
                return False
        return True




    def printposition(self):
        '''
        打印持仓
        '''
        self.log("当前%s 持仓为："%datetime.now().strftime('%Y%m%d %H:%M:%S'))
        initialholdings = self.api.get_position()
        poslogstr = "持仓:\n"
        c_ = ['品种','历史多头','今日多头','历史空头','今日空头','当前多头','当前空头']
        df_ = pd.DataFrame(columns=c_)
        for k in initialholdings.keys():
            p = self.api.get_position(f"{k}")
            df_ = df_._append(pd.Series([p.instrument_id,p.pos_long_his,p.pos_long_today,p.pos_short_his,p.pos_short_today,p.pos_long,p.pos_short], index=c_),ignore_index=True)
            # poslog =  f"{p.instrument_id} 历史多头持仓 {p.pos_long_his}, 今日多头持仓 {p.pos_long_today}, 历史空头持仓 {p.pos_short_his} , 今日空头持仓 {p.pos_short_today}, 当前多头总持仓 {p.pos_long}, 当前空头总持仓 {p.pos_short}"
            # print(poslog)
            # poslogstr = poslogstr + poslog + '\n'
            # self.log("%s" % poslog)
        poslog = self.dftotb(df =df_ )
        self.log("%s" % poslog)
        return poslog



    def get_initposition(self):
        '''
        获取初始持仓
        '''
        initialholdings = self.api.get_position()
        initialholdingdict = {}
        for k in initialholdings.keys():
            initialholdingdict[k] = initialholdings[k].volume_long - initialholdings[k].volume_short
        return initialholdingdict

    def get_orderquote(self):
        order_diff, order_direction = self.calculate_order(self.oldposition, self.targetposition )
        self.orderqueue = self.order_to_queue(dict_data=order_diff.copy())
        self.orderplan =  self.orderplanset( oldposition = self.oldposition,targetposition = self.targetposition,\
                                             orderqueue = self.orderqueue,\
                                             order_direction = order_direction, \
                                             maxvol=5)

    def calculate_order(self,dict1, dict2):
        """
        计算交割单的差异和方向
        """
        all_keys = set(dict1.keys()).union(set(dict2.keys()))
        difference = {}
        direction = {}
        for key in all_keys:
            difference[key] = abs(dict2.get(key, 0) - dict1.get(key, 0))
            direction[key] = int(np.sign(dict2.get(key, 0) - dict1.get(key, 0)))
        return difference, direction

    def order_to_queue(self, dict_data):
        """
        将订单dict 变为执行序列 完全随机
        """
        # 获取股指期货序列
        queue = []
        for key, value in dict_data.items():
            queue.extend([key] * value)
        # 打乱股指期货序列
        random.shuffle(queue)
        # 到这里，理论上应该 dict_data 全是 0
        return queue

    def dictmatch(self,dict1, dict2):
        newdict = dict1.copy()
        for k in dict2:
            if k not in dict1:
                newdict[k] = 0
        return newdict

    def orderplanset(self, oldposition, targetposition, orderqueue, order_direction, maxvol=5):
        """
        这一步的目的是，限定了单次调仓的最大笔数。因为可能出现国债太多，尽管已经均匀切分，但是对市场冲击还是很大，通过maxvol，设定最大下单手数
        """
        grouped_order = [(key, len(list(group))) for key, group in groupby(orderqueue)]
        result_order = []
        for key, count in grouped_order:
            while count > maxvol:
                result_order.append((key, maxvol))
                count -= maxvol
            if count > 0:
                result_order.append((key, count))
        orderplan = []

        recorddict = self.dictmatch(oldposition, targetposition)
        targetpositiondict = self.dictmatch(targetposition, oldposition)

        for k,v in recorddict.items():
            if v==0:
                orderplan.append([k, 0])

        for order_tp in result_order:
            recorddict[order_tp[0]] = recorddict[order_tp[0]] + order_direction[order_tp[0]] * order_tp[1]
            orderplan.append([order_tp[0], recorddict[order_tp[0]]])

        orderplan = pd.DataFrame(orderplan, columns=['sid', 'targetvol'])

        last_tg = pd.DataFrame(oldposition.items(), columns=['sid', 'targetvol'])._append(orderplan).drop_duplicates(
            subset='sid', keep='last')

        # 检查经过目标调仓序列是不是可以完成调仓目标
        if targetpositiondict == last_tg.set_index('sid').to_dict()['targetvol']:
            print("目标调仓序列可以达到最终持仓目标")
            self.log("目标调仓序列可以达到最终持仓目标:\n")
            last_tg_ = self.dftotb(df = last_tg)
            self.log( last_tg_)
            # last_tg.to_csv(self.filename,mode='a',sep='|',index=False, encoding='gbk')
        else:
            assert False, "目标调仓序列不可以达到最终持仓目标"
        return orderplan

    def dynamic_sendorder(self, dforderplan = None, timestart = None, timeend =None ):
        """
        datetime.strptime(timestart, '%Y-%m-%d %H:%M:%S.%f')
        """
        print("开始执行交易")
        self.log("%s 开始执行交易"%datetime.now().strftime('%Y%m%d %H:%M:%S'))

        t_ = pd.DataFrame.from_dict(self.targetposition, orient='index')
        t_.reset_index(inplace=True)
        t_.columns = ['品种', '仓位']
        s_ = self.dftotb( df = t_)
        fst = "目标持仓为:\n"+ s_
        self.sendmailto(body=fst, subject="\n %s 开始执行交易"%datetime.now().strftime('%Y%m%d %H:%M:%S'))
        if len(dforderplan) == 0:
            print("无需调仓")
            self.log("%s 无需调仓" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            self.sendmailto(body='', subject="%s 无需调仓" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            return []


        timestart = datetime.strptime(timestart, '%Y%m%d %H:%M:%S')
        timeend = datetime.strptime(timeend, '%Y%m%d %H:%M:%S')
        timestart_nano, timeend_nano = _convert_user_input_to_nano(timestart,timeend )

        #每次成交中间间隔纳秒
        timedaly = float((timeend_nano - timestart_nano) / (len(dforderplan)) / 1000000000)
        self.sendmailto(body='', subject="每笔交易使用秒数 %f"%timedaly )
        unfinishorder = []

        for index, orderrow in self.orderplan.iterrows():
            # break
            # print(orderrow)
            newsetposition = self.get_initposition()

            if orderrow.sid in newsetposition:
                # print(index, orderrow)
                # "ACTIVE" 对价下单，在持仓调整过程中，若下单方向为买，对价为卖一价；若下单方向为卖，对价为买一价。
                # "昨开" 表示先平昨仓，再开仓，禁止平今仓，适合股指这样平今手续费较高的品种

                quote_ = self.api.get_quote(orderrow.sid)
                print( quote_['product_id'],  offsetdict[quote_['product_id']])
                self.sendmailto(body='', subject=f"交易{quote_['product_id']} 方向{offsetdict[quote_['product_id']]} 目标数量{orderrow.targetvol}")
                dtnow = time.strftime('%H:%M:%S', time.localtime())
                dtdf = pd.DataFrame(quote_['trading_time']["day"] + quote_['trading_time']["night"])
                if ((dtdf[0] < dtnow) * (dtdf[1] > dtnow)).any():
                    target_pos_active = TargetPosTask(self.api, orderrow.sid, price="ACTIVE",offset_priority = offsetdict[quote_['product_id']])
                    target_pos_active.set_target_volume(orderrow.targetvol)
                    nethold = target_pos_active._pos.volume_long -  target_pos_active._pos.volume_short
                    t = time.time()
                    ifhavetime = True
                    while (nethold)!= orderrow.targetvol and ifhavetime:
                        self.api.wait_update()
                        nethold = target_pos_active._pos.volume_long -  target_pos_active._pos.volume_short
                        # print(f"当前{orderrow.sid} 目标变动 {orderrow.targetvol}  当前持仓 空 {target_pos_active._pos.volume_short} 多 {target_pos_active._pos.volume_long}" )
                        costtime = time.time() - t
                        if costtime>timedaly:
                            self.sendmailto(body='', subject=f"交易花费时间{costtime} 超过阈值时间{timedaly} ")
                            print(f"交易花费时间{costtime} 超过阈值时间{timedaly}")
                            ifhavetime = False
                            unfinishorder.append([orderrow.sid, orderrow.targetvol , nethold ]  )

            else:
                if orderrow.targetvol != 0:
                    directioni = "BUY" if orderrow.targetvol >0 else "SELL"
                    self.sendmailto(body='', subject=f"交易 {orderrow.sid} 方向 {directioni} 数量 {orderrow.targetvol}")
                    self.sendorder( symbol= orderrow.sid, number =  abs(orderrow.targetvol), offset = "OPEN",direction = directioni)


            timestart_nano_s, timeend_nano_e = _convert_user_input_to_nano( _cst_now(), timeend )
            timedaly = float(( timeend_nano_e  - timestart_nano_s)/ (len(dforderplan)-index) /1000000000 )
            # time.sleep(timedaly)

        print("调仓完成")
        return unfinishorder

    def tradeorder(self, timestart = None, timeend = None , delaydt = 60):
        self.log("%s 开始执行交易" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
        timestart = self.checktimestart(inputtime=timestart)
        timeend = self.checktimeend(inputtime=timeend, delaydt=delaydt)
        self.unfinishorder =  self.dynamic_sendorder( dforderplan= self.orderplan , timestart=timestart, timeend=timeend)


        if len(self.unfinishorder) == 0:
            self.log("%s 交易完成" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            poslogstr = self.printposition()
            self.sendmailto(body=poslogstr, subject="%s 交易完成" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            self.write_order_txt()
            self.write_trade_txt()
            if self.ifbalancehis:
                self.log("%s 开始平昨" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
                self.balancehisorder()

        else:
            self.sendmailto(body='', subject="%s 重大错误，存在未成交订单" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            self.log("%s 重大错误，存在未成交订单" % datetime.now().strftime('%Y%m%d %H:%M:%S'))
            assert False,"重大错误，存在未成交订单"



    def checktimeend(self, inputtime = None, delaydt = 60):
        """
        检查输入时间是不是晚于当前时间
        inputtime 格式需要满足 '%Y%m%d %H:%M:%S' 例如 '20240815 10:10:00'
        """
        if inputtime is None:
            inputtime = datetime.now() +  timedelta(seconds=delaydt)
            return inputtime.strftime( '%Y%m%d %H:%M:%S')
        deltat = (datetime.now() - datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).total_seconds()
        assert (deltat < 0 ),'输入时间 应该晚于当前时间'



    def checktimestart(self, inputtime = None):
        """
        检查输入时间是不是晚于当前时间
        inputtime 格式需要满足 '%Y%m%d %H:%M:%S' 例如 '20240815 10:10:00'
        """
        if inputtime is None:
            inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
            return inputtime
        else:
            deltat = (datetime.now() - datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).total_seconds()
            if deltat >0 :
                inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
                print("调整输入时间为当前时间")
                return inputtime
            else:
                while deltat<0:
                    deltat = (datetime.now()- datetime.strptime(inputtime, '%Y%m%d %H:%M:%S')).seconds
                    print(f"未到下单时间 需要等待 {deltat}")
                    time.sleep(1)
                inputtime = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
                return inputtime

    def write_order_txt(self):
        order_cols = ["exchange_id", "instrument_id", "direction", "offset", "status",
                      "volume_orign", "volume_left", "limit_price", "price_type",
                      "insert_date", "last_msg"]
        orders = self.api.get_order()
        orderdf = pd.DataFrame()
        for item in orders.values():
            # print(item)
            dt = datetime.fromtimestamp(item['insert_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
            orderse = pd.Series(item)
            orderse['insert_date'] = dt
            orderdf = pd.concat( [orderdf,orderse],axis=1 )
        try:
            orderdf = orderdf.T
            orderdf = orderdf[order_cols]
            orderdf.rename( columns={"exchange_id":'交易所', "instrument_id":'交易品种', "direction":'方向',
                          "offset":'动作', "status":'状态',"volume_orign":'下单量', "volume_left":'剩余未成交', "limit_price":'下单价', "price_type":'下单价类型',
                          "insert_date":'下单时间', "last_msg":'消息'} ,inplace=True )
            self.log("下单记录为：\n")
            orderdf_ = self.dftotb(df = orderdf)
            self.log(orderdf_)

            # orderdf.to_csv(self.filename,mode='a',sep='|',index=False, encoding='gbk')
        except:
            pass

    def write_trade_txt(self):
        trade_cols = [ "exchange_id", "instrument_id", "direction",
                      "offset", "price", "volume", "trade_date",'commission']
        orders = self.api.get_trade()
        orderdf = pd.DataFrame()
        for item in orders.values():
            # print(item)
            dt = datetime.fromtimestamp(item["trade_date_time"] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
            orderse = pd.Series(item)
            orderse['trade_date'] = dt
            orderdf = pd.concat([orderdf, orderse], axis=1)
        try:
            orderdf = orderdf.T
            orderdf = orderdf[trade_cols]
            orderdf.rename( columns={"exchange_id":'交易所', "instrument_id":'交易品种', "direction":'方向',
                          "offset":'动作', "price":'成交价', "volume":'成交量', "trade_date":'成交日期','commission':'成交佣金'} ,inplace=True )
            self.log("交易记录为：\n")
            orderdf_ = self.dftotb(df = orderdf)
            self.log(orderdf_)

            # orderdf.to_csv(self.filename, mode='a', sep='|', index=False, encoding='gbk')
        except:
            pass

    def downloader_orders(self):
        order_cols = ["order_id", "exchange_order_id", "exchange_id", "instrument_id", "direction", "offset", "status",
                      "volume_orign", "volume_left", "limit_price", "price_type", "volume_condition", "time_condition",
                      "insert_date_time", "last_msg"]
        trade_cols = ["trade_id", "order_id", "exchange_trade_id", "exchange_id", "instrument_id", "direction",
                      "offset", "price", "volume", "trade_date_time"]
        def write_csv(file_name, cols, datas):
            file_exists = os.path.exists(file_name) and os.path.getsize(file_name) > 0
            with open(file_name, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, dialect='excel')
                if not file_exists:
                    csv_writer.writerow(['datetime'] + cols)
                for item in datas.values():
                    if 'insert_date_time' in cols:
                        dt = datetime.fromtimestamp(item['insert_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
                    elif 'trade_date_time' in cols:
                        dt = datetime.fromtimestamp(item['trade_date_time'] / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')
                    else:
                        dt = None
                    row = [dt] + [item[k] for k in cols]
                    csv_writer.writerow(row)
        with self.api as api:
            # 将当前账户下全部委托单、成交信息写入 csv 文件中
            write_csv("orders.csv", order_cols, api.get_order())
            write_csv("trades.csv", trade_cols, api.get_trade())

