一、用例编写之JSON

1、json文件中，区分请求方式。get方法，请求参数的key用'params'，其他请求用'data'

2、json文件中，预期结果的key，一定要是响应中存在的key

3、json文件中，预期结果的value，可以是str、int、dict。如果是dict，则预期应该首先判断其类型和长度，value中的其他子value当作普通子串在响应文本中校验

4、json预期结果，如果是异常用例校验，需要在预期中知名状态码具体是多少，否则按成功状态码进行校验