import calendar
import datetime
import os
import subprocess
import time
import pyautogui
import pyperclip
import win32com.client as win32


def get_first_and_last_day(plus_minus_days=0):
    """默认返回当天(当天加减n天）和本月第一天及本月最后一天的日期列表"""
    try:
        today = datetime.date.today() + datetime.timedelta(days=plus_minus_days)
        year = today.year
        month = today.month
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(year, month)[1])
        return [today, first_day, last_day]
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def get_file_create_access_modified_date(file_path):
    """获取文件创建时间、访问时间、修改时间列表"""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    try:
        timestamp = os.stat(file_path)
        modified_time = datetime.datetime.fromtimestamp(timestamp.st_mtime)  # 获取文件最后修改时间
        access_time = datetime.datetime.fromtimestamp(timestamp.st_atime)  # 获取文件最后访问时间
        create_time = datetime.datetime.fromtimestamp(timestamp.st_ctime)  # 获取文件创建时间
        return [create_time, access_time, modified_time]
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing file {file_path}: {e}")
        return []


def get_equality(file_path01, file_path02, hours_num=1):
    """判断文件1和文件2的最后修改时间是否在最近hours_num小时"""
    if not os.path.exists(file_path01) or not os.path.exists(file_path02):
        return 'file not exists'
    erp = get_file_create_access_modified_date(file_path01)[2]
    hd = get_file_create_access_modified_date(file_path02)[2]
    th = (datetime.datetime.now() + datetime.timedelta(hours=-hours_num))
    if erp >= th and hd >= th:
        return 'equality'
    else:
        return 'not equality'


def picture_point(picture_path, confidence=0.85, times=60):
    """返回图片位置信息Box(left,top,width,height),默认匹配度为0.85，默认尝试60次"""
    if not os.path.isfile(picture_path):
        return f'File does not exist or is not a file: {picture_path}'
    for cnt in range(times):
        try:
            time.sleep(1)
            return pyautogui.locateOnScreen(picture_path, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            print(f"Retrying after 1 second... {times - cnt} times left")
            continue
    return 'Picture not Found on screen'


def click_point(img_path, match=0.85, times=60, left=0, top=0):
    """若图片存在则返回图片坐标位置，否则返回图片文件不存在或路径错误
    默认点击图片中心位置，否则点击参数指定位置
    img_path: 图片路径、match: 匹配度、times: 重试次数、left: 右偏移量、top: 下偏移量
    """
    if not os.path.isfile(img_path):
        return f'File does not exist or file path is error: {img_path}'
    try:
        loc = picture_point(img_path, match, times)
        if left != 0 and top != 0:
            pyautogui.click(loc.left + left, loc.top + top)
        else:
            pyautogui.click(loc.left + loc.width // 2, loc.top + loc.height // 2)
        return loc
    except Exception as e:
        print(f"Error occurred: {e}")


def wx_search_user(wx_name, img_dir):
    """搜索用户、点击搜索到的用户并切换到用户界面。img_path: 图片目录、username: 微信用户名"""
    for i in ['C:\\Program Files', 'D:\\Program Files', 'C:\\Program Files (x86)']:
        try:
            subprocess.Popen(fr'{i}\Tencent\WeChat\WeChat.exe')
            break
        except WindowsError:
            print(f'程序不在{i}\\Tencent\\WeChat\\WeChat.exe中')
    loc_user = click_point(f'{img_dir}\\wx_name.png')  # 【search.png】搜索框图片名
    pyperclip.copy(wx_name)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.click(loc_user.left + 77, loc_user.top + 98)


def send_msg_text(ps):
    """param ps: {'user': '微信用户名', 'msg': '要发送的文本内容','img_path':'图片所在目录'}"""
    wx_search_user(ps['user'], fr'{ps["img_path"]}')  # 搜索用户并切换到用户界面
    # 点击文本输入框、输入需要发送的文本内容并点击发送按钮
    click_point(f'{ps["img_path"]}\\msg.png')
    pyperclip.copy(ps['msg'])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    pyautogui.press('enter')
    # 点击【关闭】按钮
    click_point(f'{ps["img_path"]}\\close.png')


def send_msg_file(ps):
    """param ps: {'user': '微信用户名', 'filename': r'待发送文件完整路径','img_path':'图片所在目录'}"""
    wx_search_user(ps['user'], fr'{ps["img_path"]}')  # 搜索用户并切换到用户界面
    time.sleep(2)
    rst = click_point(f'{ps["img_path"]}\\filebtn.png')  # 点击发送文件【图片按钮】
    try:
        if rst.startswith('File does not exist'):
            return
    except AttributeError:
        pass
    time.sleep(2)
    pyperclip.copy(ps['filename'])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    pyautogui.press('enter')
    click_point(fr'{ps["img_path"]}\sendbtn.png')  # 点击【发送】按钮
    click_point(fr'{ps["img_path"]}\close.png')  # 点击【关闭】按钮


def wait_appear_or_disappear(img_path, times=60, match=0.85, option=True):
    """等待元素出现或消失,默认等待60秒
    img_path: 图片路径、times:等待时间(s)、match: 匹配度、switch: True为等待元素出现，False为等待元素消失
    """
    for i in range(times):
        time.sleep(1)
        if option:
            try:
                pyautogui.locateOnScreen(fr'{img_path}', confidence=match)
                break
            except pyautogui.ImageNotFoundException as e:
                continue
        else:
            try:
                pyautogui.locateOnScreen(fr'{img_path}', confidence=match)
                continue
            except pyautogui.ImageNotFoundException as e:
                break


def execute_macro(args):
    """param:{'file_path': r'带宏excel文件路径', 'sheet_name': '工作表名', 'macro_name': '宏名称'}"""
    # 参数验证
    required_keys = ['file_path', 'sheet_name', 'macro_name']
    if not all(key in args for key in required_keys):
        raise ValueError("缺少必需的参数: {}".format(", ".join(required_keys)))
    excel = win32.gencache.EnsureDispatch("Excel.Application")  # 创建Excel应用程序对象
    excel.Visible = True  # 设置可见，默认不可见False
    # 打开已存在的Excel文件
    try:
        workbook = excel.Workbooks.Open(args['file_path'], UpdateLinks=True)  # 更新链接
        worksheet = workbook.Worksheets(args['sheet_name'])  # 获取工作表对象
        worksheet.Activate()
        excel.Run(args['macro_name'])  # 调用VBA函数
        workbook.Close(SaveChanges=True)  # 关闭并保存Excel文件
    except Exception as e:
        print("执行宏时出错：", str(e))
    finally:
        if excel is not None:
            excel.Quit()  # 退出Excel应用程序


def run_macro(macro_name):
    excel = win32.gencache.EnsureDispatch("Excel.Application")  # 创建Excel应用程序对象
    excel.Visible = True  # 设置可见，默认不可见False
    try:
        excel.Run(macro_name)  # 调用VBA函数
    except Exception as e:
        print("执行宏时出错：", str(e))


if __name__ == '__main__':
    pass
