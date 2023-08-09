"""
Module for smoke detection
Author: Thaweewat Rugsujarit
"""

from roboflow import Roboflow


def run_smoke(img_folder, predict_fol, current_time: str):
    """
    This method is used to run smoke detection on an image.

    :param img_folder: The folder path where the image is located.
    :param predict_fol: The folder path where the predicted image will be saved.
    :param current_time: The current timestamp used to generate unique file names.

    :return: None. The method directly performs the smoke detection and saves the predicted image.
    """
    rf = Roboflow(api_key="U3NW9smTBuXptye6R03r")
    project = rf.workspace().project("smoke100-uwe4t")
    model = project.version(5).model

    # infer on a local image
    print(
        model.predict(
            f"{img_folder}\\img_raw_{current_time}.jpg", confidence=30, overlap=30
        ).json()
    )

    # visualize your prediction
    model.predict(
        f"{img_folder}\\img_raw_{current_time}.jpg", confidence=30, overlap=30
    ).save(f"{predict_fol}\\smoke_predict_{current_time}.jpg")
