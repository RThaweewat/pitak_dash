"""
Module for fire detection
Author: Thaweewat Rugsujarit
"""
from roboflow import Roboflow


def run_fire(img_folder, predict_fol, current_time: str):
	"""
	:param img_folder: The folder path where the input image is located.
	:param predict_fol: The folder path where the predicted image will be saved.
	:param current_time: The current time in string format.
	:return: None

	This method runs the fire detection model on an input image.
	It uses the Roboflow API to predict if there is fire in the image.
	The input image is specified by the `img_folder` and `current_time`
	parameters. The predicted image is saved in the `predict_fol` folder.
	"""
	rf = Roboflow(api_key="U3NW9smTBuXptye6R03r")
	project = rf.workspace().project("firedetector")
	model = project.version(1).model

	# infer on a local image
	print(
		model.predict(
			f"{img_folder}\\img_raw_{current_time}.jpg", confidence=30, overlap=30
		).json()
	)

	# visualize your prediction
	model.predict(
		f"{img_folder}\\img_raw_{current_time}.jpg", confidence=30, overlap=30
	).save(f"{predict_fol}\\fire_predict_{current_time}.jpg")

