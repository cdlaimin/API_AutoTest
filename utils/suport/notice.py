import json
import time

import requests
from urllib3.exceptions import InsecureRequestWarning

from conf import HOSTS
from utils.suport import logger
from utils.suport.templates import REPORT


def send_wechat(*args):
    """
    发送结果到企业微信
    :return:
    """
    job_name, build_number, total, result, pass_rate, duration, passed, failed, skipped, error, token = args

    # 计算时分秒
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)

    # 报告路径
    host = HOSTS['wechat_robot'] + token
    url = HOSTS['jenkins'].format(job_name, build_number)

    # 报告标题
    title = "自动化测试报告"

    # 准备请求数据
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    body = {
        "msgtype": "markdown",
        "markdown": {
            "content": REPORT.format(title=title, url=url, result=result, pass_rate=pass_rate,
                                     h=h, m=m, s=s, total=total, passed=passed, failed=failed,
                                     skipped=skipped, error=error)
        },
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=host, data=json.dumps(body), headers=headers, verify=False)
    except Exception as e:
        logger.error(f'企业微信-测试结果发送失败：{e}')
    else:
        logger.info('企业微信-测试结果已发送：' + response.text)


def send_upload_result_to_wechat(**kwargs):
    token = kwargs.get('wechat_token')
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
    b = "73d36c76-5e62-43fd-b18d-eb710fcb4c0e"
    send_wechat(1, 2, 2, 3, 4, a, 6, 7, 8, 9, b)
