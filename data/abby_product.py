import sys
import os
from pathlib import Path

try:
    sys.path.append(str(Path(__file__).parent.parent.absolute()))
except NameError:
    sys.path.append(str(Path(os.getcwd()).parent.absolute()))

from lib.dbwork import aggregate_to_df
from object_detection import crop_hosted_image

# Query abby's products
df = aggregate_to_df(
    "products",
    pipeline=[
        {"$match": {"deleted": False, "sku": {"$regex": "^B\\d+"}, "notBuying": False}},
        {"$project": {"_id": 0, "sku": 1, "description": 1, "imageLink": 1}},
    ],
)
df = df[df["imageLink"].str.len() > 10]

list_abby_images = crop_hosted_image(df["imageLink"].tolist(), "data/abby", save=True)
