import os
import json
import time
import random
import threading
from pathlib import Path
from datetime import datetime

from DrissionPage import Chromium, ChromiumOptions, SessionOptions

# 获取当前脚本所在的目录
CURRENT_DIRECTORY = Path(__file__).resolve().parent
# print("当前程序运行路径:", CURRENT_DIRECTORY)

# CACHE_DIR = CURRENT_DIRECTORY / 'CACHE'

# 文件夹不存在的时候创建文件夹
# for _dir in [CACHE_DIR, ]:
#     if not _dir.exists():
#         _dir.mkdir(parents=True, exist_ok=True)

DATA_PACKET_ATTRIBUTES = {
    'tab_id': '产生这个请求的标签页的 id',
    'frameId': '产生这个请求的框架 id',
    'target': '产生这个请求的监听目标',
    'url': '数据包请求网址',
    'method': '请求类型',
    'is_failed': '是否连接失败',
    'resourceType': '资源类型',
    'request': '请求信息的对象',
    'response': '响应信息的对象',
    'fail_info': '连接失败信息的对象'
}

REQUEST_ATTRIBUTES = {
    'url': '请求的网址',
    'method': '请求类型',
    'headers': '以大小写不敏感字典返回 headers 数据',
    'cookies': '返回发送的 cookies',
    'postData': 'post 类型的请求所提交的数据，json 以dict格式返回'
}

RESPONSE_ATTRIBUTES = {
    'url': '请求的网址',
    'headers': '以大小写不敏感字典返回 headers 数据',
    'body': '如果是 json 格式，自动进行转换，如果是图片格式，进行 base64 转换，其他格式直接返回文本',
    'raw_body': '未被处理的 body 文本',
    'status': '请求状态',
    'statusText': '请求状态文本'
}

REQUEST_ERROR_ATTRIBUTES = {
    'errorText': '错误信息文本',
    'canceled': '是否取消',
    'blockedReason': '拦截原因',
    'corsErrorStatus': 'cors 错误状态'
}


class BaseWebClient:
    """
    BaseWebClient 类提供了用于网络爬虫和自动化任务的基础功能。
    它包括了目录初始化、网页标签管理和一些实用工具方法，如模仿人类行为的随机延迟功能。

    属性:
        current_directory (Path): 脚本所在的目录。
        cache_dir (Path): 用于存储缓存文件的目录。
        tab_id_file_path (Path): 存储当前浏览器标签ID的文件路径。
    """

    def __init__(self, base_dir=None, configs_file=None, cache_dir=None, is_tab=True, log_function=print, wx_thread=None, debug=False):
        self.base_dir = Path(base_dir or Path(os.getcwd()))
        self.configs_file = configs_file or self.base_dir / 'web.configs'
        self.configs = self.read_configs()
        self.log_function = log_function
        self.wx_thread = wx_thread
        self.debug = debug
        self.infos = []
        self.errors = []
        self.listen_thread = None
        self.is_listening = False
        self.page = self.get_web_page()
        if is_tab:
            self.tab = self.get_tab()
        else:
            self.tab = None
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = self.base_dir / 'cache'
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def read_configs(self):
        """
        从文件中读取设置

        返回:
            dist: 读取到的设置，如果文件不存在则或者读取失败返回空字典
        """
        try:
            if os.path.exists(self.configs_file):
                with open(self.configs_file, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                return obj
        except Exception as e:
            print('读取设置错误', e)

        return {}

    def save_configs(self):
        """
        保存设置文件
        """
        try:
            with open(self.configs_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print('保存设置错误', e)

    def random_sleep(self, start=1, end=3, info=''):
        """
        在指定的时间范围内随机暂停，以模仿人类行为避免被反爬机制检测。

        参数:
            start (int): 最短休眠时间。
            end (int): 最长休眠时间。
            debug (bool): 如果为True，则打印休眠时间。
            info (str): 休眠前打印的额外信息。
        """
        sleep_time = random.randint(start, end)
        print(f'{info}随机延迟：{sleep_time} 秒......')
        time.sleep(sleep_time)

    def read_tab_id(self):
        """
        读取 tab_id
        """
        if 'tab' in self.configs and 'tab_id' in self.configs['tab']:
            return self.configs['tab']['tab_id']

    def save_tab_id(self, tab_id):
        """
        保存 tab_id
        """
        self.configs['tab'] = {
            'tab_id': tab_id
        }
        self.save_configs()

    def get_tab(self):
        """
        根据保存的标签ID获取或创建浏览器中的新标签页。

        参数:
            page (WebPage): 管理标签页的WebPage对象。

        返回:
            Tab: 检索到的或新创建的浏览器标签页。
        """
        # http://drissionpage.cn/browser_control/browser_object

        tab_id = self.read_tab_id()
        tab_ids = [tab.tab_id for tab in self.page.get_tabs()]

        if tab_id and tab_id in tab_ids:
            tab = self.page.get_tab(tab_id)
            print(f'正在使用 {tab.title} {tab}')
        else:
            tab = self.page.new_tab()  # 新建标签页，获取标签页对象
            self.save_tab_id(tab.tab_id)
            print(f'新建Tab {tab.title} {tab}')

        # 激活使用的标签
        self.page.activate_tab(tab)

        if self.debug:
            print('WebPage当前模式', tab.mode)

        return tab

    def get_web_page(self):
        # from DrissionPage import ChromiumPage
        # from DrissionPage import WebPage, ChromiumOptions, SessionOptions

        # http://drissionpage.cn/browser_control/connect_browser

        co = ChromiumOptions()  # 使用指定 ini 文件 ini_path=r'./config1.ini'
        # 设置用户文件夹路径。用户文件夹用于存储当前登陆浏览器的账号在使用浏览器时留下的痕迹，包括设置选项等。
        # 一般来说用户文件夹的名称是 User Data。对于默认情况下的 Windows 中的 Chrome 浏览器来说，此文件夹位于 %USERPROFILE%\AppData\Local\Google\Chrome\User Data\，
        # 也就是当前系统登陆的用户目录的 AppData 内。实际情况可能有变，实际路径请在浏览器输入 chrome://version/，查阅其中的个人资料路径或者叫用户配置路径。
        # 若要使用独立的用户信息，可以将 User Data 目录整个复制到自定的其他位置，然后在代码中使用 set_user_data_path() 方法，参数填入自定义位置路径，这样便可使用独立的用户文件夹信息。
        # co.set_user_data_path(path)
        # 使用系统用户设置
        # co.use_system_user_path()  # 使用浏览器默认用户文件夹，浏览器已经打开的时候不能使用

        so = SessionOptions()  # 使用指定 ini 文件 ini_path=r'./config1.ini'

        # 当同时传入ChromiumOptions和SessionOptions时，两者都有的属性以ChromiumOptions为准。如timeout和download_path
        page = Chromium(addr_or_opts=co, session_options=so)  # 通过配置信息创建
        # page = WebPage(chromium_options='http://127.0.0.1:9222', session_or_options=so)  # 输入地址访问的时候只能访问本机

        # page.quit()  # 彻底关闭内置的Session对象和Driver对象，并关闭浏览器（如已打开）

        # print('所有标签页id组成的列表', page.tabs)

        # 标签管理
        # http://drissionpage.cn/browser_control/browser_object
        # tab = page.get_tab(1)
        # print(tab.rect.window_state)  # 获取窗口状态
        # print(tab.rect.window_location)  # 获取窗口位置
        # print(tab.rect.window_size)  # 获取窗口大小

        # tab.set.window.size(500, 500)  # 设置窗口大小
        # tab.set.window.location(500, 500)  # 设置窗口位置
        # tab.set.window.max()  # 窗口最大化

        # page.get('https://www.baidu.com')
        # print(f'{page.title} cookies', page.cookies())
        # print(f'{page} headers', so.headers)

        return page

    def change_mode(self, mode: str = 's', go: bool = False, copy_cookies: bool = True):
        """
        切换模式

        如copy_cookies为True，切换时会把当前模式的cookies复制到目标模式
        切换后，如果go是True，调用相应的get函数使访问的页面同步
        :param mode: 模式字符串，接收's'或'd'
        :param go: 是否跳转到原模式的 url
        :param copy_cookies: 是否复制 cookies 到目标模式
        :return: None
        """
        mode = str(mode).lower()

        if mode not in ['s', 'd']:
            raise ValueError(f'不能切换到"{mode}"模式，只支持"s"或"d"模式')

        if mode == self.tab.mode:
            return

        self.tab.change_mode(mode=mode, go=go, copy_cookies=copy_cookies)

    def get(self, url, show_errmsg=False, retry=None, interval=None, timeout=None, **kwargs):
        """
        跳转到一个url

        http://drissionpage.cn/browser_control/visit

        :param url: 目标url
        :param show_errmsg: 是否显示和抛出异常
        :param retry: 重试次数，为None时使用页面对象retry_times属性值
        :param interval: 重试间隔（秒），为None时使用页面对象retry_interval属性值
        :param timeout: 连接超时时间（秒），为None时使用页面对象timeouts.page_load属性值
        :param kwargs: 连接参数，s模式专用
        :return: url是否可用，d模式返回None时表示不确定
        """
        if self.tab.get(url, show_errmsg=show_errmsg, retry=retry, interval=interval, timeout=timeout, **kwargs):
            return self.tab

    def get_html(self, url, show_errmsg=False, retry=None, interval=None, timeout=None, **kwargs):
        """
        打开 url获取 html

        # http://drissionpage.cn/browser_control/get_page_info

        :param url: 目标url
        :param show_errmsg: 是否显示和抛出异常
        :param retry: 重试次数，为None时使用页面对象retry_times属性值
        :param interval: 重试间隔（秒），为None时使用页面对象retry_interval属性值
        :param timeout: 连接超时时间（秒），为None时使用页面对象timeouts.page_load属性值
        :param kwargs: 连接参数，s模式专用
        :return: url是否可用，d模式返回None时表示不确定
        """
        if self.tab.get(url, show_errmsg=show_errmsg, retry=retry, interval=interval, timeout=timeout, **kwargs):
            return self.tab.html  # raw_data

    def get_json(self, url, show_errmsg=False, retry=None, interval=None, timeout=None, **kwargs):
        """
        打开url获取json

        http://drissionpage.cn/browser_control/get_page_info

        :param url: 目标url
        :param show_errmsg: 是否显示和抛出异常
        :param retry: 重试次数，为None时使用页面对象retry_times属性值
        :param interval: 重试间隔（秒），为None时使用页面对象retry_interval属性值
        :param timeout: 连接超时时间（秒），为None时使用页面对象timeouts.page_load属性值
        :param kwargs: 连接参数，s模式专用
        :return: url是否可用，d模式返回None时表示不确定
        """
        if self.tab.get(url, show_errmsg=show_errmsg, retry=retry, interval=interval, timeout=timeout, **kwargs):
            return self.tab.json

    def get_screenshot(self, path=None, name=None, as_bytes=None, as_base64=None,
                       full_page=False, left_top=None, right_bottom=None):
        """
        网页截图，可对整个网页、可见网页、指定范围截图

        https://drissionpage.cn/browser_control/screen
        """
        self.tab.get_screenshot(path=path, name=name, as_bytes=as_bytes, as_base64=as_base64,
                                full_page=full_page, left_top=left_top, right_bottom=right_bottom)

    def run_listen_thread(self, targets=None, is_regex=None, method=None, res_type=True, handle_listen_packet=None):
        """
        开始监听进程，并支持传递参数给 start_listen

        https://drissionpage.cn/browser_control/listener

        此方法用于启动监听器，可以设置获取的目标特征
        可选择多个特征，符合条件的数据包将被获取
        如果监听未停止时调用此方法，已抓取的队列将被清除

        注意：
        当 targets 不为 None，is_regex 会自动设为 False
        即如要使用正则，每次设置 targets 时需显式指定 is_regex=True

        参数:
        - targets (str, list, tuple, set): 默认值为 None。要匹配的数据包 URL 特征。可以用列表指定多个，为 True 时获取所有
        - is_regex (bool): 默认值为 None。设置的 target 是否为正则表达式，为 None 时保持原来设置
        - method (str, list, tuple, set): 默认值为 None。设置监听的请求类型，可指定多个，默认为 ('GET', 'POST')，为 True 时监听所有，为 None 时保持原来设置
        - res_type (str, list, tuple, set): 默认值为 True。设置监听的 ResourceType 类型，可指定多个，为 True 时监听所有，为 None 时保持原来设置
        - handle_listen_packet 处理从网络流量中捕获的数据包
        """
        if self.tab is None:
            self.tab = self.get_tab()

        # 创建线程并传递参数
        self.listen_thread = threading.Thread(
            target=self.start_listen,
            args=(targets, is_regex, method, res_type, handle_listen_packet)
        )
        self.listen_thread.start()
        self.is_listening = True

    def stop_listen_thread(self):
        """
        开始监听进程

        注意：我们在结束进程的时候，会等到有新消息到监听才会彻底停止
        """
        self.is_listening = False
        if self.listen_thread.is_alive():
            self.listen_thread.join()

    def start_listen(self, targets=None, is_regex=None, method=None, res_type=True, handle_listen_packet=None):
        """
        开始监听网络流量，并根据预定义的标准（例如图像文件、API响应）处理捕获的数据
        """
        # 从 DrissionPage._units.listener 模块导入 Listener

        # 启动监听
        self.tab.listen.start(targets=targets, is_regex=is_regex, method=method, res_type=res_type)

        for packet in self.tab.listen.steps():

            if not self.is_listening:
                print("停止监听")
                self.tab.listen.stop()
                break

            # 跳过内容为空的链接
            if not packet.response.raw_body:
                continue

            if handle_listen_packet is None:
                self.handle_listen_packet(packet)
            else:
                handle_listen_packet(packet)

    def handle_listen_packet(self, packet):
        """
        处理从网络流量中捕获的数据包，按需求重写

        参数:
            packet (NetworkPacket): 捕获的包含数据的网络数据包。
        """

        # print('-' * 50)
        # print(packet.resourceType, packet.url)

        # if packet.resourceType in ['XHR']:
        #     ...
        # elif packet.resourceType == 'Image':
        #     ...

        for k, v in DATA_PACKET_ATTRIBUTES.items():
            if k == 'request':  # 请求信息的对象
                print('请求信息的对象:')
                # for k, v in REQUEST_ATTRIBUTES.items():
                #     print(f'\t\t{v}: {getattr(packet.request, k)}')
            elif k == 'response':  # 响应信息的对象
                print('响应信息的对象:')
                # if packet.response.url:
                #     for k, v in RESPONSE_ATTRIBUTES.items():
                #         print(f'\t\t{v}: {getattr(packet.response, k)}')
            elif k == 'fail_info':  # 连接失败信息的对象
                if packet.is_failed:
                    print('连接失败信息的对象:')
                    # for k, v in REQUEST_ERROR_ATTRIBUTES.items():
                    #     print(f'\t\t{v}: {getattr(packet.fail_info, k)}')
            else:
                print(f'{v}: {getattr(packet, k)}')


def 简单例子():
    web = BaseWebClient(debug=True)
    r = web.get('https://www.mi.com/')
    # tab.cookies_to_session()  # 复制浏览器当前页面的 cookies 到 Session 对象
    # tab.cookies_to_browser()  # 把 Session 对象的 cookies 复制到浏览器
    # tab.close()  # 关闭当前标签页和Session
    from DrissionPage._units.setter import MixTabSetter

    print(web.tab.html)
    # print(web.get_html('https://suggest.taobao.com/sug?code=utf-8&q=%E5%95%86%E5%93%81%E5%85%B3%E9%94%AE%E5%AD%97&callback=cb'))
    # print(web.get_json('https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key=%E5%85%B3%E9%94%AE%E5%AD%97&bk_length=600'))


def 监听网络数据的例子():
    listener = BaseWebClient(debug=True)
    listener.run_listen_thread(targets='baidu.com', is_regex=None, method=None, res_type=True, handle_listen_packet=None)
    print('我们在进程中运行网络处理')
    # 运行一段时间后停止监听
    time.sleep(30)
    listener.stop_listen_thread()


if __name__ == '__main__':
    ...
    # 简单例子()
    监听网络数据的例子()
