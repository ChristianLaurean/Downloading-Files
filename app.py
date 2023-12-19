import requests
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_dir():
    current_date_time = datetime.now()
    path = Path.cwd() / 'source'
    path_downloads = path / 'downloads'

    if not path_downloads.exists():
        path_downloads.mkdir()
    path_downloads_date = path_downloads / f'downloads_at={current_date_time.strftime("%Y-%m-%d")}'
    if not path_downloads_date.exists():
        path_downloads_date.mkdir()

    return path_downloads_date

def download_file(path_name, url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(path_name, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

def extract_zip(path_name, path_destination):
    with zipfile.ZipFile(path_name, 'r') as zip_file:
        zip_file.extractall(path_destination)

def move_dir(path_destination, name_file, path_downloads_date):
    shutil.move(
        f'{path_destination}/{name_file}.csv',
        str(path_downloads_date)
    )

def delete_dir_and_file(path_zip, path_dir):
    if path_dir.exists() and path_zip.exists():
        path_zip.unlink()
        shutil.rmtree(path_dir)


def run():
    urls = ["https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip"]
    path_downloads_date = create_dir()
    for url in urls:
        name_file_zip = url.split('/')[3]
        name_file = name_file_zip.split('.')[0]
        path_name_zip = path_downloads_date / name_file_zip
        path_destination = path_downloads_date / name_file
        
        try:
            download_file(path_name_zip, url)
        except requests.HTTPError as err:
            print(f"HTTP Error: {err}")

        extract_zip(path_name_zip, path_destination)
        move_dir(path_destination, name_file, path_downloads_date)
        delete_dir_and_file(path_name_zip, path_destination)

if __name__ == '__main__':
    run()
