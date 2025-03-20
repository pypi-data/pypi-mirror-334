import asyncio
import os
from twscrape.accounts_pool import AccountsPool
from twscrape.ext_account import ExtAccount

async def main():
    # 初始化AccountsPool
    pool = AccountsPool(db_file="accounts.db")
    
    # 设置API级别的代理 - 将覆盖账号级别的代理
    api_proxy = os.getenv("API_PROXY", "http://api_proxy_example:8080")
    
    # 获取一个可用的账号
    acc = await pool.get_for_queue("example")
    if not acc:
        print("没有可用的账号")
        return
    
    # 创建ExtAccount实例 - 传递API级别的代理设置
    ext_acc = ExtAccount(acc, debug=1, proxy=api_proxy)
    print(f"使用代理: {api_proxy}")
    
    # 如果你不想使用API级别的代理，只使用账号级别的代理:
    # ext_acc = ExtAccount(acc, debug=1)
    # print(f"使用账号代理: {acc.proxy}")
    
    try:
        # 发送推文示例
        tweet_result = await ext_acc.tweet("这是一条通过扩展API发送的测试推文 #测试")
        print(f"发送推文结果: {tweet_result}")
        
        # 如果推文发送成功，获取推文ID并执行其他操作
        if "data" in tweet_result and "create_tweet" in tweet_result["data"]:
            tweet_id = tweet_result["data"]["create_tweet"]["tweet"]["rest_id"]
            print(f"推文ID: {tweet_id}")
            
            # 点赞自己的推文
            like_result = await ext_acc.like(tweet_id)
            print(f"点赞结果: {like_result}")
            
            # 稍后取消点赞
            await asyncio.sleep(2)
            unlike_result = await ext_acc.unlike(tweet_id)
            print(f"取消点赞结果: {unlike_result}")
            
            # 删除推文
            await asyncio.sleep(2)
            delete_result = await ext_acc.untweet(tweet_id)
            print(f"删除推文结果: {delete_result}")
    
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 解锁账号，让其他任务可以使用
        await pool.unlock(acc.username, "example")

if __name__ == "__main__":
    asyncio.run(main()) 