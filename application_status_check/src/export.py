import csv
import json
from datetime import datetime


def export_csv(cell_data_list: list, output_dir: str):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'{output_dir}/tennis_data_{current_time}.csv'
    with open(file_name, "w", encoding="UTF8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cell_data_list[0].keys())
        writer.writeheader()
        writer.writerows(cell_data_list)


def export_json(cell_data_list: list, output_dir: str):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'{output_dir}/appliation_{current_time}.json'
    with open(file_name, "w", encoding="UTF8", newline="") as file:
        json.dump(cell_data_list, file)
