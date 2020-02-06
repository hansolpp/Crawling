import requests
import pandas as pd
from io import BytesIO


def krx_foriegn_hoding(p_tdate):

	tdate = p_tdate

	#GET
	gen_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
	headers = {
		'Referer': 'http://marketdata.krx.co.kr/mdi',
		'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
	}
	query_str_parms = {
		'name': 'fileDown',
		'filetype': 'xls',
		'url': 'MKD/13/1302/13020402/mkd13020402',
		'market_gubun': 'ALL',
		'lmt_tp': '1',
		'sect_tp_cd': 'ALL',
		'schdate': str(tdate),
		'pagePath': '/contents/MKD/13/1302/13020402/MKD13020402.jsp'
	}

	r = requests.get(gen_req_url, query_str_parms, headers=headers)

	#POST
	gen_req_url = 'http://file.krx.co.kr/download.jspx'
	headers = {
		'Referer': 'http://marketdata.krx.co.kr/mdi',
		'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
	}
	form_data = {
		'code': r.content
	}
	r = requests.post(gen_req_url, form_data, headers=headers)

	#Make excel file
	df = pd.read_excel(BytesIO(r.content))
	df['거래일자'] = tdate

	file_dir = '//home//minwoo//Stock//'
	file_name = 'KRX_foriegn_hoding_' + str(tdate) +'.xlsx'

	df.to_excel(file_dir + file_name,index=False, index_label=None)

	print('외국인 보유량 크롤링 완료', tdate)
	return


if __name__ == '__main__':

	for year in range(2018, 2019):
		for month in range(1, 13):
			for day in range(1, 32):
				tdate = year * 10000 + month * 100 + day * 1 #YYYYMMDD
				if tdate <= 20200206:
					krx_foriegn_hoding(tdate)
