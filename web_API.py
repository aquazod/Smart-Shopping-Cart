import requests
import threading


class API:
	
	def __init__(self):
		#links
		self.Get_Products = 'https://smartcartapplication.azurewebsites.net/Product/ListOfProductsData'

	#Methods
	def GetProducts(self,cartid,userid):
		print("[+] Getting Current Products....")
		req = requests.get('https://smartcartapplback.azurewebsites.net/Product/GetProductCart?cartId=%d&userId=%d' % (cartid,userid))
		status = req.status_code
		print("[+] Status Code:{}".format(status))
		if(str(status) == "200"):
			req_json = req.json()
			n_products = len(req_json)
			NumOfItems = 0
			for i in range(0, n_products):
				NumOfItems += int(req_json[i]['productAmount'])
			print('[+] %d Items In Cart'%NumOfItems)
			print('[+] List Of Products:')
			print('=' * 20)
			for i in range(0, n_products):
				print("\tproductId[%s] , productName[%s] ,  Ammount [%s]" % (req_json[i]['productId'],req_json[i]['productName'],req_json[i]['productAmount']))
			print('=' * 20)
		else:
			print('[!] ListOfProductsData Status : %s'%status)

	def AddProduct(self,cartid,productId):
		r = requests.post('https://smartcartapplback.azurewebsites.net/Product/AddProductCart?cartId=%s&productId=%d' % (str(cartid),productId))
		status = r.status_code
		if(str(status) == "200"):
			print("\n\n######### Product Added  #########\n\n")
		else:
			print('[!] Add Failed Status : %s' % status)

	def DeleteProduct(self,cartid,productId):
		r = requests.delete('https://smartcartapplback.azurewebsites.net/Product/RemoveProductFromCart?cartId=%s&productId=%d' % (str(cartid),productId))
		status = r.status_code
		if(str(status) == "200"):
			print("\n\n######### Product Removed  #########\n\n")
		else:
			print('[!] Remove Product Failed Status : %s' % status)

	def SusbendCart(self):
		r = requests.post(
			'https://smartcartapplback.azurewebsites.net/Product/SetCartOverloaded?cartId=ss1mmctp&isOverloaded=true')
		status = r.status_code
		if (str(status) == "200"):
			print("\n\n######### Alert Sent #########\n\n")
		else:
			print('[!] Alert Failed Status : %s' % status)

	def unsusbendCart(self):
		r = requests.post(
			'https://smartcartapplback.azurewebsites.net/Product/SetCartOverloaded?cartId=ss1mmctp&isOverloaded=false')
		status = r.status_code
		if (str(status) == "200"):
			print("\n\n######### Alert Sent #########\n\n")
		else:
			print('[!] Alert Failed Status : %s' % status)

#how to use
#api=API()
#api.AddProduct(123,5) # coca
#api.AddProduct(123,2) # coca
#api.DeleteProduct(123,2)
#api.GetProducts(123,1)