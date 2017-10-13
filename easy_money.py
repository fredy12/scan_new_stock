#coding=utf-8

import requests
import json
import datetime

all_datas = []


def get_new_stock_data(pages=2):
    all_result = []

    for page in xrange(pages):
        r = requests.get("http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSSTV5&st=12&sr=-1&p="+str(page+1)+"&ps=50&js=var%20oIGzltLU={paes:(pc),data:[(x)]}&stat=1&rt=4949403")
        x = r.text.strip("var oIGzltLU={paes:31,data:")
	print x
        result = json.loads(x[7:-1])
	all_result = all_result + result

    print_result(all_result)


def print_result(all_result):
    global all_datas
    for result in all_result:
        average_pe = result.split(",")[32]
	stock_init_pe = result.split(",")[14]
	now_price = result.split(",")[23]
	first_price = result.split(",")[10]
	now_state = result.split(",")[38]
	online_time = result.split(",")[13]
	stock_id = result.split(",")[4]
        stock_type = result.split(",")[19]
	firstday_price = result.split(",")[24]
	if result.split(",")[19] != u"sh":
	    stock_type = "sz"

	r = requests.get("http://qt.gtimg.cn/q=%s%s" % (stock_type, stock_id))
	stock_now_pe = r.text.split('~')[39]
        flow_value = r.text.split('~')[44]
        total_value = r.text.split('~')[45]

	try:
	    point = (float(average_pe) - float(stock_init_pe)) / float(stock_init_pe) - (float(now_price)-float(first_price)) / float(first_price)
	except Exception, e:
	    print "ERROR Stock is: " + result.split(",")[3] + " " + result.split(",")[4]
	    continue
	if point > 0 and now_state == u"开板" and datetime.datetime.strptime(online_time, "%Y-%m-%d") > datetime.datetime.strptime("2016-10-01", "%Y-%m-%d"):
            all_datas.append({
	        "stock_name": result.split(",")[3],
	        "stock_id": result.split(",")[4],
	        "stock_desc": result.split(",")[27],
	        "online_time": result.split(",")[13],
	        "first_price": result.split(",")[10],
	        "now_price": result.split(",")[23],
		"firstday_price": firstday_price,
	        "stock_init_pe": result.split(",")[14],
		"stock_now_pe": stock_now_pe,
	        "average_pe": result.split(",")[32],
	        "now_state": result.split(",")[38],
		"up_percent": result.split(",")[39],
	        "overroll": result.split(",")[40],
		"stock_type": stock_type,
	        "point": point,
                "flow_value": flow_value,
                "total_value": total_value,
	    })


if __name__ == "__main__":
    total_page = 10
    get_new_stock_data(total_page)
    last_datas = sorted(all_datas, key=lambda x:x["point"], reverse=True)
    for data in last_datas:
        print data["stock_name"]
        print data["stock_id"]
        print data["stock_desc"]
        print data["online_time"]
        print data["overroll"]
	print data["up_percent"]
	print "highest price: " + str(float(data["firstday_price"]) * (float(data["overroll"])*0.1 + 1.0))
	print "now price: " + data["now_price"]
	print "stock init price: "+ data["first_price"]
	print "stock init pe: "+ data["stock_init_pe"]
	print "expect pe: " + str(float(data["stock_init_pe"]) * (float(data["now_price"])) / float(data["first_price"]))
	print "now pe: " + data["stock_now_pe"]
	print "hang average pe: " + data["average_pe"]
        print data["point"]
        print "flow value (yi): " + data["flow_value"]
        print "total value (yi): " + data["total_value"]
	print


