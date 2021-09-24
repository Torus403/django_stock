# Copyright (c) 2021-2022 Jack Mcnish All Rights Reserved

from django.shortcuts import render, redirect  
from .models import Stock
from django.contrib import messages
from .forms import StockForm

def home(request):
	import requests
	import json
	import yfinance as yf

	if request.method == "POST":
		ticker = request.POST['ticker']
		try:
			tickerdata = yf.Ticker(ticker)
			api = json.dumps(tickerdata.info, indent=4)
			api = json.loads(api) 
		except Exception as e:
			api = "Error..." # error handling doesnt work!!!!!!! make it so that is api is empty then disp Error
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json
	import yfinance as yf




	if request.method == "POST":
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:

			try:
				tickerdata = yf.Ticker(str(ticker_item))
				api = json.dumps(tickerdata.info, indent=4)
				api = json.loads(api)
				output.append(api) 
			except Exception as e:
				api = "Error..." # error handling doesnt work!!!!!!! make it so that is api is empty then disp Error


		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})



def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect(delete_stock)




def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})