import json

import requests
from urllib3.exceptions import InsecureRequestWarning

from conf import settings
from libs.logger import logger



def send_dingtalk(*args):
    """
    发送结果到钉钉群
    :return:
    """
    config = settings.NOTIFICATION_CONFIG.get('dingtalk')
    ip = config.get('ip')
    port = config.get('port')
    title = config.get('title')
    text = config.get('text')
    token = config.get('token')
    job_name, build_number, total, result, passrate, time, passed, failed, skiped, error = args

    time = time.seconds
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    host = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
    headers = {"Content-Type": "application/json; charset=UTF-8"}

    report_url = f"http://{ip}:{port}/job/{job_name}/{build_number}/allure/"

    msg_body = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"{title}",
            "text": f"### {title} [点击查看报告]({report_url})\n\n" +
                    f"> {text}" + "\n\n" +
                    f"> 测试结果:**{result}** \t 用例总数:**{total}** \t 通过率:**{passrate}** \n\n" +
                    f"> 测试耗时:   **{h}小时 {m}分 {s}秒** \n\n"
                    f">> 通过用例: {passed}\n\n" +
                    f">> 失败用例: {failed}\n\n" +
                    f">> 跳过用例: {skiped}\n\n" +
                    f">> 错误用例: {error}\n\n"
        },
        "at": {
            "atMobiles": [],
            "isAtAll": True
        }
    }
    try:
        # 屏蔽发送消息时的告警
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=host, data=json.dumps(msg_body), headers=headers, verify=False)
    except Exception as e:
        logger.error(f'钉钉-测试结果发送失败：{e}')
    else:
        logger.info('钉钉-测试结果已发送：' + response.text)


def send_wechat(*args):
    """
    发送结果到企业微信
    :return:
    """
    config = settings.NOTIFICATION_CONFIG.get('wechat')
    ip = config.get('ip')
    port = config.get('port')
    title = config.get('title')
    text = config.get('text')
    token = config.get('token')
    job_name, build_number, total, result, passrate, time, passed, failed, skiped, error = args

    time = time.seconds
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    host = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={token}"
    headers = {"Content-Type": "application/json; charset=UTF-8"}

    report_url = f"http://{ip}:{port}/job/{job_name}/{build_number}/allure/"

    msg_body = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"### {title} [点击查看报告]({report_url})\n\n" +
                       f"> {text}" + "\n\n" +
                       f">  测试结果:  **{result}** \n  通过率:  **{passrate}** \n   测试耗时:  **{h}小时 {m}分 {s}秒** \n\n" +
                       f"> 用例总数:**{total}** \n\n" +
                       f"> -通过用例: {passed}\n" +
                       f"> -失败用例: {failed}\n" +
                       f"> -跳过用例: {skiped}\n" +
                       f"> -错误用例: {error}\n",
        },
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=host, data=json.dumps(msg_body), headers=headers, verify=False)
    except Exception as e:
        logger.error(f'企业微信-测试结果发送失败：{e}')
    else:
        logger.info('企业微信-测试结果已发送：' + response.text)


if __name__ == '__main__':
    print(settings.NOTIFICATION_CONFIG.get('wechat'))
