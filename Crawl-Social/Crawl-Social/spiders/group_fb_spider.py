import csv
import scrapy
from scrapy_splash import SplashRequest

class GroupFbSpiderSpider(scrapy.Spider):
    name = "group_fb_spider"
    allowed_domains = ["www.facebook.com"]
    start_urls = ["https://www.facebook.com/groups/nghienquiz"]

    lua_script = '''
        function main(splash, args)

        assert(splash:go(args.url))
        assert(splash:wait(3))

        email = assert(splash:select('#m_login_email'))
        email:focus()
        email:send_text("buivihieu3@gmail.com")
        assert(splash:wait(1))

        password = assert(splash:select("#m_login_password"))
        password:focus()
        password:send_text("0973094120")
        assert(splash:wait(1))

        btnLogin = assert(splash:select("*[name='login']"))
        btnLogin:mouse_click()
        assert(splash:wait(3))
        
        assert(splash:go("https://www.facebook.com/groups/nghienquiz"))
        assert(splash:wait(3))

        btnCover = assert(splash:select("i[data-testid='cover_photo_arrow']"))
        btnCover:mouse_click()
        assert(splash:wait(3))

        contentValue = splash:evaljs("document.evaluate('/html/body/div[1]/div/div[4]/div/div/div[3]/div[1]/div/div[3]/div/div[1]/h3', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText")
        print(contentValue)
        assert(splash:wait(3))
        return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            members = contentValue,
        }
        end
    '''

    def start_requests(self):
        url = "https://www.facebook.com"
        yield SplashRequest(url=url, callback=self.parse, endpoint="execute", args={
            'lua_source': self.lua_script
        })

    
    def parse(self, response):
        if 'members' in response.data:
            members_value = response.data['members']

            # Ghi vào file CSV
            with open('output_group.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['group_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Ghi header
                writer.writeheader()

                # Ghi dữ liệu
                writer.writerow({'group_value': members_value})

            self.log("Dữ liệu đã được lưu vào output.csv")
        else:
            self.log("Không tìm thấy dữ liệu")
        yield {'data': 'data_from_second_spider'}
