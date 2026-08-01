import os
import sys

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app import app

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data


with app.app_context():

    print("Starting ETL...")

    data = extract_data()

    transformed = transform_data(data)

    load_data(transformed)

    print("ETL Finished Successfully")