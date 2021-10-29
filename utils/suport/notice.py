import json
import time

import requests
from loguru import logger
from urllib3.exceptions import InsecureRequestWarning

from conf import NOTICE_TEMP, HOST


def send_dingtalk(*args):
    """
    发送结果到钉钉群
    :return:
    """
    config = NOTICE_TEMP.get('dingtalk')
    title = config.get('title')
    text = config.get('text')
    job_name, build_number, total, result, passrate, time, passed, failed, skiped, error, token = args

    time = time.seconds
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    host = HOST['ding_robot'] + token
    headers = {"Content-Type": "application/json; charset=UTF-8"}

    report_url = f"{HOST['jenkins']}"

    msg_body = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"{title}",
            "text": f"### {title}  [点击查看报告]({report_url})\n\n" +
                    f"> {text}" + "\n\n" +
                    f"> 测试结果:**{result}** \t 用例总数:**{total}** \t 通过率:**{passrate}** \n\n" +
                    f"> 测试耗时:**{h}小时 {m}分 {s}秒** \n\n"
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
    config = NOTICE_TEMP.get('wechat')
    title = config.get('title')
    text = config.get('text')
    job_name, build_number, total, result, passrate, time, passed, failed, skiped, error, token = args

    time = 60
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    host = HOST['wechat_robot'] + token
    headers = {"Content-Type": "application/json; charset=UTF-8"}

    report_url = HOST['jenkins'].format(job_name, build_number)

    msg_body = {
        "msgtype": "markdown",
        "markdown": {
            "content":
                f"### {title} [点击查看报告]({report_url})\n\n\n" +
                f" {text}" + "\n\n" +
                f"测试结果:**{result}**  通过率:**{passrate}**  \n测试耗时:**{h}小时 {m}分 {s}秒** \n\n\n" +
                f"用例总数:**{total}** \n\n" +
                f" - 通过用例: {passed}\n" +
                f" - 失败用例: {failed}\n" +
                f" - 跳过用例: {skiped}\n" +
                f" - 错误用例: {error}\n",
        },
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=host, data=json.dumps(msg_body), headers=headers, verify=False)
    except Exception as e:
        logger.error(f'企业微信-测试结果发送失败：{e}')
    else:
        logger.info('企业微信-测试结果已发送：' + response.text)


def send_upload_result_to_wechat(**kwargs):
    config = NOTICE_TEMP.get('wechat')
    token = config.get('token')

    total = kwargs.get('total')
    success = kwargs.get('success')
    fail = kwargs.get('fail')
    msg = kwargs.get('msg')

    text = ""

    if msg:
        text = '\n\n'.join(list(msg))

    host = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={token}"
    headers = {"Content-Type": "application/json; charset=UTF-8"}

    msg_body = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"### 用例同步结果:\n\n\n" +
                       (f"{text} \n\n\n" if text else "无异常信息\n\n\n") +
                       f"同步总数: {total} \t 成功: {len(success)} \t 失败: {len(fail)}"
        },
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=host, data=json.dumps(msg_body), headers=headers, verify=False)
    except Exception as e:
        logger.error(f'企业微信-同步结果发送失败：{e}')
    else:
        logger.info('企业微信-同步结果已发送：' + response.text)


if __name__ == '__main__':
    a = time.time()
    send_wechat(1, 2, 2, 3, 4, a, 6, 7, 8, 9)
