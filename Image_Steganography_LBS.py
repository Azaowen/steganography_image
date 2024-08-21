#!/usr/bin/env python3
from PIL import Image

"""
 Convert encoding data into 8-bit binary
 form using ASCII value of characters

 Hàm này thực hiện đổi thông điệp sang ASCII 
 và từ ASCII đổi sang nhị phân
"""
def genData(data): 

		#Create an empty list to store the binary values
		#Tạo mảng chứa mã nhị phân của chuỗi
		newd = [] 

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd 


"""
 Pixels are modified according to the
 8-bit binary data and finally returned

 Hàm này thực hiện đổi các pixel theo nhị phân
 trả về kết quả là một mảng pixel đã chèn thông điệp
"""
def modPix(pix, data):

	# An array store message of binary
	# Mảng chứa mã nhị phân của message
	datalist = genData(data) 
	# Leng of message
	# Độ dài của message (Số lượng phần tử của mảng datalist)
	lendata = len(datalist)
	#Tạo iterator từ ảnh
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		# Lấy lần lượt 3 pixel
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		"""
		Pixel value should be made
		odd for 1 and even for 0

		Thực hiện thay đổi chẵn lẻ theo bit của thông điệp
		Bit 1 là lẻ, bit 0 là chẵn
		"""
		for j in range(0, 8):
			"""
			If bit in message is 0
			Decrease by 1 to make it odd
			Or else Decrease/increase by 1 to make it even 

			Nếu bit thông điệp là 0 và giá trị pixel là lẻ
			Thì giảm giá trị pixel xuống thành chẵn
			Hoặc tăng giảm thành lẻ
			"""
			if (datalist[i][j] == '0' and pix[j]% 2 != 0): 
				pix[j] -= 1			
						   
			elif (datalist[i][j] == '1' and pix[j] % 2 == 0): 
				# Avoid overflow the limits 0 or 255
				# Đoạn này nhằm tránh tăng giảm quá giới hạn của pixel 0 và 255
				if(pix[j] != 0):							  
					pix[j] -= 1
				else:
					pix[j] += 1
	
					
				
		"""
		Eighth pixel of every set tells
		whether to stop ot read further.
		0 means keep reading; 1 means the message is over.
		
		Phần này thực hiện xác định điểm cuối 
		của thông điệp tại cuối mỗi bit thứ 8.
		chẵn thì vẫn còn; lẻ thì kết thúc 
		"""
		if (i == lendata - 1): 		# Nếu như đang ở vị trí cuối của message
			if (pix[-1] % 2 == 0): 	# Nếu pixel là số chẵn
				if(pix[-1] != 0): 	# Nếu pixel khác 0
					pix[-1] -= 1 	# Giá trị pixel giảm 1
				else:
					pix[-1] += 1	# Hoặc =0 thì tăng 1 

		else:						# Còn nếu chưa ở vị trí cuối
			if (pix[-1] % 2 != 0):	# Nếu pixel là số lẻ
				pix[-1] -= 1		# Thì giảm đi 1 

		#Đổi pix thành tuple 
		pix = tuple(pix)

		# return 3 pixel after encoding
		# Trả về 3 giá trị sau khi đã mã hóa
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		# Thay thế pixel tại tọa độ x y với màu là pixel nhận vào
		newimg.putpixel((x, y), pixel)
		# Reach the image width limit 
		# Nếu đạt tới giới hạn chiều rộng ảnh 
		if (x == w - 1): 
			x = 0
			y += 1
		else:
			x += 1



# Encode data into image
# Hàm mã hóa dữ liệu thành ảnh
def encode():
	img = input("Đường dẫn tới ảnh (bao gồm đuôi mở rộng ảnh) : ")
	image = Image.open(img, 'r')

	data = input("Nhập thông điệp : ")
	if (len(data) == 0):
		raise ValueError('Không có thông điệp')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input("Nhập tên cho ảnh mới (bao gồm đuôi mở rộng ảnh) : ") 
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
# Giải mã từ ảnh
def decode():
	img = input("Nhập ảnh cần giải mã : ")
	image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		# Tạo string chứa thông điệp nhị phân
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

# Main Function
def main():
	a = int(input(":: Welcome to Steganography ::\n"
						"1. Mã hóa\n2. Giải mã\n"))
	if (a == 1):
		encode()

	elif (a == 2):
		print("Thông điệp : " + decode())
	else:
		raise Exception("Dữ liệu không hợp lệ!")


if __name__ == '__main__' :
	main()
