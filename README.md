# wx2p
基于Tornado web框架, 涉及技术stack:  Redis, Fabric etc.

实现：
  1. 用apscheduler 进行health check(Apscheduler+Requests)
  2. 微信企业号发送异常通知(Celery+Redis)
  3. 企业号可交互command(Fabric)
  4. 定时(apscheduler)调用Elasticsearch API(Nginx access log)查询恶意ip并添加到系统黑名单(Fabric)
