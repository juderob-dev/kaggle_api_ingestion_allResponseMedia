

BASE_URL = "https://www.kaggle.com/api/v1"

OWNER_SLUG = "datasnaek"
DATASET_SLUG = "youtube-new"
DATASET = f"{OWNER_SLUG}/{DATASET_SLUG}"

DATASET_VERSION = 115

CSV_FILE_NAME = "GBvideos.csv"
JSON_FILE_NAME = "GB_category_id.json"

DOWNLOAD_URL = (
    f"{BASE_URL}/datasets/download/{OWNER_SLUG}/{DATASET_SLUG}"
    f"?datasetVersionNumber={DATASET_VERSION}"
)
