import pytesseract # this is tesseract module
import matplotlib.pyplot as plt
import cv2 # this is opencv module
import glob
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\tnaguib\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
def calculate_predicted_accuracy(actual_list, predicted_list):
	for actual_plate, predict_plate in zip(actual_list, predicted_list):
		accuracy = "0 %"
		num_matches = 0
		if actual_plate == predict_plate:
			accuracy = "100 %"
		else:
			if len(actual_plate) == len(predict_plate):
				for a, p in zip(actual_plate, predict_plate):
					if a == p:
						num_matches += 1
				accuracy = str(round((num_matches / len(actual_plate)), 2) * 100)
				accuracy += "%"
		print("	 ", actual_plate, "\t\t\t", predict_plate, "\t\t ", accuracy)
        
# specify path to the license plate images folder as shown below
path_for_license_plates = os.getcwd() + "src/modules/models/plates/**/*.jpg"
list_license_plates = []
predicted_license_plates = []

for path_to_license_plate in glob.glob(path_for_license_plates, recursive = True):
	
	license_plate_file = path_to_license_plate.split("/")[-1]
	license_plate, _ = os.path.splitext(license_plate_file)
	'''
	Here we append the actual license plate to a list
	'''
	list_license_plates.append(license_plate)
	
	'''
	Read each license plate image file using openCV
	'''
	img = cv2.imread(path_to_license_plate)
	
	'''
	We then pass each license plate image file
	to the Tesseract OCR engine using the Python library
	wrapper for it. We get back predicted_result for
	license plate. We append the predicted_result in a
	list and compare it with the original the license plate
	'''
	predicted_result = pytesseract.image_to_string(img, lang ='eng',
	config ='--oem 3 --psm 6 -c tessedit_char_whitelist = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
	
	filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
	predicted_license_plates.append(filter_predicted_result)
print("Actual License Plate", "\t", "Predicted License Plate", "\t", "Accuracy")
print("--------------------", "\t", "-----------------------", "\t", "--------")

		
calculate_predicted_accuracy(list_license_plates, predicted_license_plates)
print(len(list_license_plates))
print(len(predicted_license_plates))
# Read the license plate file and display it
test_license_plate = cv2.imread("src\modules\models\plates\plate5.jpg")
plt.imshow(test_license_plate)
plt.axis('off')
plt.title('LETITGO1 license plate')
resize_test_license_plate = cv2.resize(
	test_license_plate, None, fx = 2, fy = 2,
	interpolation = cv2.INTER_CUBIC)
grayscale_resize_test_license_plate = cv2.cvtColor(
	resize_test_license_plate, cv2.COLOR_BGR2GRAY)
gaussian_blur_license_plate = cv2.GaussianBlur(
	grayscale_resize_test_license_plate, (5, 3),cv2.BORDER_DEFAULT)
new_predicted_result = pytesseract.image_to_string(gaussian_blur_license_plate, lang ='eng',
config ='--oem 3 -l eng --psm 6 tessedit_char_whitelist = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
filter_new_predicted_result = "".join(new_predicted_result.split()).replace(":", "").replace("-", "")
print(filter_new_predicted_result)
cv2.imshow('plate',gaussian_blur_license_plate)
cv2.waitKey(0)


