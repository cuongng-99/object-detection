from ultralytics import YOLO
import cv2
import os
from os.path import join

# import re
import time
from download_images import download_images
import glob
from sentence_transformers import SentenceTransformer, util
from PIL import Image

home = os.getcwd()


# import matplotlib.pyplot as plt
start = time.time()

# Load model
model = YOLO(f"{home}/model-runs/detect/train/weights/best.pt")


def get_name_images(folder):
    images = os.listdir(folder)
    return images


# Extract Image Object from input folder
def crop_local_images(input_folder, output_folder):
    images = get_name_images(input_folder)
    i = 0
    for image_name in images:
        source_path = f"{input_folder}/{image_name}"
        image = cv2.imread(source_path)

        resp = model.predict(source=source_path)
        resp = list(resp)[0]
        try:
            boxes = resp.boxes.xyxy[0]
            x1 = int(boxes[0].item())
            y1 = int(boxes[1].item())
            x2 = int(boxes[2].item())
            y2 = int(boxes[3].item())

            crop_image = image[y1:y2, x1:x2]
            # name_result = re.sub(r"\..*$", "", image_name)
            cv2.imwrite(os.path.join(output_folder, f"{i}.jpg"), crop_image)

            num_image_cropped = len(get_name_images(output_folder))
            if num_image_cropped % 50 == 0:
                print(f"Đã thêm {num_image_cropped} ảnh")

        except Exception as e:
            print(f"Lỗi {e}: {image_name}")
        i = i + 1


def detect_similar_local_image(input_folder, output_folder):
    """Để phát hiện vật thể từ các ảnh lưu trữ trên local
    cần truyền vào input folder và output folder"""

    predict_path = f"{home}/{input_folder}"
    result_path = f"{home}/{output_folder}"

    crop_local_images(predict_path, result_path)

    # get images
    files = []
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        files.extend(glob.glob(join(result_path, ext)))
    print("Đã cắt được {} ảnh".format(len(files)))
    files.sort()

    list_images = []
    for filename in files:
        im = Image.open(filename)
        list_images.append(im)

    # load model
    print("Loading CLIP Model...")
    model = SentenceTransformer("clip-ViT-B-32")
    encoded_image = model.encode(
        list_images, batch_size=128, convert_to_tensor=True, show_progress_bar=False
    )

    processed_images = util.paraphrase_mining_embeddings(encoded_image)
    return processed_images


# Extract object from hosted image and save to output folder
def crop_hosted_image(urls, output_folder, save=True):
    list_images = download_images(urls)
    croped_images = []
    i = 0
    for image in list_images:
        resp = model.predict(image)
        resp = list(resp)[0]
        try:
            boxes = resp.boxes.xyxy[0]
            x1 = int(boxes[0].item())
            y1 = int(boxes[1].item())
            x2 = int(boxes[2].item())
            y2 = int(boxes[3].item())

            crop_image = image.crop((x1, y1, x2, y2))
            croped_images.append(crop_image)
            if save:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                crop_image.save(os.path.join(output_folder, f"{i}.jpg"))
                num_image_cropped = len(get_name_images(output_folder))
                if num_image_cropped % 50 == 0:
                    print(f"Đã thêm {num_image_cropped} ảnh")
            i += 1

        except Exception as e:
            print(f"Lỗi {e}: {image}")
    return croped_images


def detect_from_hosted_image(urls_1: list, urls_2: list, save=True):
    """Phát hiện các vật thể giống nhau dựa vào link ảnh
    Lựa chọn lưu ảnh sau khi phát hiện được vật thể hay không"""

    if save:
        list_images_1 = crop_hosted_image(urls_1, "output1", save=True)
        list_images_2 = crop_hosted_image(urls_2, "output2", save=True)
    else:
        list_images_1 = crop_hosted_image(urls_1, "output1", save=False)
        list_images_2 = crop_hosted_image(urls_2, "output2", save=False)

    print("Loading CLIP Model...")
    model = SentenceTransformer("clip-ViT-B-32")
    encoded_image_1 = model.encode(
        list_images_1, batch_size=128, convert_to_tensor=True, show_progress_bar=False
    )
    encoded_image_2 = model.encode(
        list_images_2, batch_size=128, convert_to_tensor=True, show_progress_bar=False
    )

    processed_images = util.detect_from_two_embeddings(
        encoded_image_1, encoded_image_2, threshold=0.8
    )
    return processed_images
