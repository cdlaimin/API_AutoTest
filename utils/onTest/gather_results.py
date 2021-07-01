from datetime import datetime


def gather_results(session, exitstatus):
    """
    统计测试结果
    :param session: pytest session 对象
    :param exitstatus:  执行结束的状态码
    :return:
    """
    # 用例总数
    total = session.testscollected
    # 测试耗时
    time = datetime.now() - session.config.getoption('start_time')
    # 获取统计报告
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')
    passed = len(reporter.stats.get('passed', []))
    failed = len(reporter.stats.get('failed', []))
    error = len(reporter.stats.get('error', []))
    skipped = len(reporter.stats.get('skipped', []))
    passrate = '%.2f' % (round(((passed + skipped) / total) * 100)) + '%'
    build_number = session.config.getoption('build_number')
    job_name = session.config.getoption('job_name')
    if exitstatus == 0:
        result = "通过"
    elif exitstatus == 1 or exitstatus == 3:
        result = "失败"
    elif exitstatus == 2:
        result = "中断"
    elif exitstatus == 4:
        result = "错误"
    elif exitstatus == 5:
        result = "无可用的用例"
    else:
        result = "未知"
    return job_name, build_number, total, result, passrate, time, passed, failed, skipped, error



