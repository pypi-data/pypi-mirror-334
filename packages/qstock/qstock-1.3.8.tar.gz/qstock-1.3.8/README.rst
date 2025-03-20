qstock由“Python金融量化”公众号开发，试图打造成个人量化投研分析开源库，目前包括数据获取（data）、可视化(plot)、选股(stock)和量化回测（backtest）四个模块。其中数据模块（data）数据来源于东方财富网、同花顺、新浪财经等网上公开数据，数据爬虫部分参考了现有金融数据包tushare、akshare和efinance。qstock致力于为用户提供更加简洁和规整化的金融市场数据接口。可视化模块基于plotly.express和pyecharts包，为用户提供基于web的交互图形简单操作接口；选股模块提供了同花顺的技术选股和公众号策略选股，包括RPS、MM趋势、财务指标、资金流模型等，回测模块为大家提供向量化（基于pandas）和基于事件驱动的基本框架和模型。
qstock目前在pypi官网上发布，开源第一版本为1.1.0，目前更新至1.3.7.

读者直接“pip install qstock ”安装，或通过'pip install --upgrade qstock'进行更新。GitHub地址：https://github.com/tkfy920/qstock。

目前部分策略选股和策略回测功能仅供知识星球会员使用，会员可在知识星球置顶帖子上上获取qstock离线安装包。

相关教程：

【qstock开源了】数据篇之行情交易数据(https://mp.weixin.qq.com/s/p1lEsBVhrm5ej3YZl0BhOw)
【qstock数据篇】行业概念板块与资金流(https://mp.weixin.qq.com/s/hj4yuqFDBidAeSRucz6TwQ)
【qstock量化】数据篇之股票基本面数据(https://mp.weixin.qq.com/s/XznS8hFMEa47x1IElZXJaA)
【qstock量化】数据篇之宏观指标和财经新闻文本(https://mp.weixin.qq.com/s/vq7BJUCdHMkcgJYjsErpYQ)
【qstock量化】动态交互数据可视化(https://mp.weixin.qq.com/s/zmY4gsPDQ6xDDpC-fVBUPg)
        
更多干货请关注微信公众号：Python金融量化