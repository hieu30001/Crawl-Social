
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import datetime
import csv
import pandas as pd
import subprocess


class FanpageFbSpiderPipeline:
    def process_item(self, item, spider):
        # Lưu dữ liệu vào file CSV
        data_to_write = item.get('likes')  # Thay thế bằng cách lấy dữ liệu của bạn
        if data_to_write:
            self.append_to_csv('output_fanpage.csv', data_to_write)
        return item

    def append_to_csv(self, file_path, data):
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['data_field']  # Thay thế bằng tên trường thích hợp của bạn
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Nếu file CSV trống, ghi header
            if csvfile.tell() == 0:
                writer.writeheader()

            # Ghi dữ liệu
            writer.writerow({'data_field': data})


class GroupFbSpiderPipeline:
    def process_item(self, item, spider):
        # Lưu dữ liệu vào file CSV
        data_to_write = item.get('members')  # Thay thế bằng cách lấy dữ liệu của bạn
        if data_to_write:
            self.append_to_csv('output_group.csv', data_to_write)
        return item

    def append_to_csv(self, file_path, data):
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['data_field']  # Thay thế bằng tên trường thích hợp của bạn
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Nếu file CSV trống, ghi header
            if csvfile.tell() == 0:
                writer.writeheader()

            # Ghi dữ liệu
            writer.writerow({'data_field': data})
            


def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl('fanpage_fb_spider')
    process.crawl('group_fb_spider')
    process.crawl('tiktok_spider')
    process.crawl('youtube_spider')
    process.start()
    file_python1 = 'spiders\instagram_spider.py'
    subprocess.run(['python', file_python1])
    


def merge_csv_files():
    # Đọc dữ liệu từ hai file CSV
    fanpage_data = pd.read_csv('output_fanpage.csv')
    group_data = pd.read_csv('output_group.csv')
    tiktok_data = pd.read_csv('output_tiktok.csv')
    youtube_data = pd.read_csv('output_youtube.csv')
    instagram_data = pd.read_csv('output_instagram.csv')

    end_time = datetime.datetime.now()
    end_time1 = pd.Series(['End Time: ' + str(end_time)])

    # tách số lượng subricer
    split_fanpage = str(fanpage_data).split()
    number_follower_fanpage = split_fanpage[2]

    split_group = str(group_data).split()
    number_follower_group = split_group[2]
    
    split_tiktok = str(tiktok_data).split()
    number_follower_tiktok = split_tiktok[2]

    split_youtube = str(youtube_data).split()
    number_follower_youtube = split_youtube[2]  

    split_instagram = str(instagram_data).split()
    number_follower_instagram = split_instagram[2]  

    #tổng lượt follower
    sum_follower_social = int(number_follower_fanpage) + int(number_follower_group) + int(number_follower_tiktok) + int(number_follower_youtube) + int(number_follower_instagram) 
    
    #phần trăm kpi đạt đượt
    per_kpi = float(sum_follower_social*100 / 50000)

    # Kết hợp dữ liệu bằng cách nối theo dòng
    merged_data = pd.concat(['\n \n \n' + end_time1, '\n FANPAGE FACEBOOK: \t' + fanpage_data, 'GROUP FACEBOOK: \t' + group_data, '\n TIKTOK: \t' + tiktok_data, '\n YOUTUBE: \t' + youtube_data, 'INSTAGRAM: \t' + instagram_data + '\n \n SUM FOLLOWER: ' + str(sum_follower_social) + '\n \n PER KPI: ' + str(per_kpi) + '%' ], axis=0, ignore_index=True)




    # Ghi dữ liệu kết hợp vào file CSV mới
    output_file = 'output.csv'

    # Kiểm tra xem file đã tồn tại chưa
    try:
        # Nếu đã tồn tại, mở file ở chế độ append
        existing_data = pd.read_csv(output_file)
        merged_data.to_csv(output_file, index=False, mode='a', header=False, encoding='utf-8')
    except FileNotFoundError:
        # Nếu chưa tồn tại, tạo file mới và ghi dữ liệu vào đó
        merged_data.to_csv(output_file, index=False, mode='w', header=False, encoding='utf-8')


    print(merged_data)

    
if __name__ == "__main__":
    start_time = datetime.datetime.now()

    # Chạy spiders
    run_spiders()

    # Kết hợp dữ liệu từ hai file CSV
    merge_csv_files()

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time

    # In ra thời gian chạy
    print(f"Thời gian chạy: {elapsed_time}")




