import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
os.chdir("/var/www/data_scripts/scripts")

def download_part(url, start, end, part_num, pbar):
    headers = {'Range': f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)
    
    with open(f"part_{part_num}.csv", "wb") as f:
        f.write(response.content)
    
    # Обновляем прогресс
    pbar.update(1)

def download_file(url, num_parts=4):
    # Если файл уже существует, удаляем его
    if os.path.exists("expired.csv"):
        os.remove("expired.csv")
    
    # Получаем размер файла
    response = requests.head(url)
    file_size = int(response.headers['Content-Length'])
    
    # Определяем диапазоны для скачивания
    part_size = file_size // num_parts
    
    # Создаем прогресс-бар для логирования
    with tqdm(total=num_parts, desc="Downloading", unit="part") as pbar:
        with ThreadPoolExecutor(max_workers=num_parts) as executor:
            futures = []
            for i in range(num_parts):
                start = i * part_size
                end = start + part_size - 1 if i < num_parts - 1 else file_size
                futures.append(executor.submit(download_part, url, start, end, i, pbar))
            
            # Ожидаем завершения всех задач
            for future in futures:
                future.result()

    # Объединяем части в один файл
    with open("expired.csv", "wb") as f_out:
        for i in range(num_parts):
            with open(f"part_{i}.csv", "rb") as f_in:
                f_out.write(f_in.read())
            os.remove(f"part_{i}.csv")

url = 'https://expired.ru/lists/expired.csv'
download_file(url)
