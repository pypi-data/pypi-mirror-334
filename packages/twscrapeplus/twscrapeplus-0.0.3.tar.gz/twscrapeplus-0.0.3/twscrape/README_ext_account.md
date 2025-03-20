# Twitter API 扩展功能

本扩展模块 (`ext_account.py`) 为twscrape库添加了来自twitter-api-client的额外API功能，使您可以执行更多Twitter API操作，如发送推文、点赞、关注等。

## 功能特点

- 完全兼容twscrape的账号管理系统
- 提供丰富的Twitter API操作
- 支持异步调用
- 与twscrape的现有功能无缝集成

## 安装

本扩展已包含在twscrape库中，无需额外安装。

## 基本用法

```python
import asyncio
from twscrape.accounts_pool import AccountsPool
from twscrape.ext_account import ExtAccount

async def main():
    # 初始化AccountsPool
    pool = AccountsPool(db_file="accounts.db")
    
    # 获取一个可用的账号
    acc = await pool.get_for_queue("example")
    if not acc:
        print("没有可用的账号")
        return
    
    # 创建ExtAccount实例
    ext_acc = ExtAccount(acc, debug=1)
    
    # 发送推文
    result = await ext_acc.tweet("这是一条测试推文 #测试")
    print(result)
    
    # 完成后解锁账号
    await pool.unlock(acc.username, "example")

if __name__ == "__main__":
    asyncio.run(main())
```

## 支持的操作

扩展API支持以下操作:

### 推文操作

- `tweet(text, media=None, **kwargs)` - 发送推文
- `reply(text, tweet_id)` - 回复推文
- `quote(text, tweet_id)` - 引用推文
- `retweet(tweet_id)` - 转发推文
- `unretweet(tweet_id)` - 取消转发
- `like(tweet_id)` - 点赞推文
- `unlike(tweet_id)` - 取消点赞
- `bookmark(tweet_id)` - 收藏推文
- `unbookmark(tweet_id)` - 取消收藏
- `pin(tweet_id)` - 置顶推文
- `unpin(tweet_id)` - 取消置顶
- `untweet(tweet_id)` - 删除推文
- `create_poll(text, choices, poll_duration)` - 创建投票

### 用户互动

- `follow(user_id)` - 关注用户
- `unfollow(user_id)` - 取消关注
- `mute(user_id)` - 静音用户
- `unmute(user_id)` - 取消静音
- `block(user_id)` - 拉黑用户
- `unblock(user_id)` - 取消拉黑
- `enable_follower_notifications(user_id)` - 开启用户通知
- `disable_follower_notifications(user_id)` - 关闭用户通知

### 列表操作

- `create_list(name, description, private)` - 创建列表
- `update_list(list_id, name, description, private)` - 更新列表
- `update_pinned_lists(list_ids)` - 更新已置顶列表
- `pin_list(list_id)` - 置顶列表
- `unpin_list(list_id)` - 取消置顶列表
- `add_list_member(list_id, user_id)` - 向列表添加成员
- `remove_list_member(list_id, user_id)` - 从列表移除成员
- `delete_list(list_id)` - 删除列表
- `update_list_banner(list_id, media)` - 更新列表横幅
- `delete_list_banner(list_id)` - 删除列表横幅

### 话题操作

- `follow_topic(topic_id)` - 关注话题
- `unfollow_topic(topic_id)` - 取消关注话题

### 私信操作

- `dm(text, receivers, media='')` - 发送私信
- `dm_inbox()` - 获取私信收件箱
- `dm_history(conversation_ids=None)` - 获取私信历史
- `dm_delete(conversation_id=None, message_id=None)` - 删除私信

### 其他操作

- `update_profile_image(media)` - 更新个人资料图片
- `update_profile_banner(media)` - 更新个人资料横幅
- `update_profile_info(**kwargs)` - 更新个人资料信息
- `update_search_settings(settings)` - 更新搜索设置
- `update_settings(settings)` - 更新设置
- `change_password(old, new)` - 修改密码

## 定时发布

```python
# 安排推文在特定时间发送
await ext_acc.schedule_tweet("定时推文", "2023-12-31 23:59")

# 安排回复在特定时间发送
await ext_acc.schedule_reply("定时回复", "2023-12-31 23:59", tweet_id)

# 获取已安排的推文
scheduled = await ext_acc.scheduled_tweets()

# 取消已安排的推文
await ext_acc.unschedule_tweet(tweet_id)
```

## 调试模式

在创建ExtAccount实例时，可以启用调试模式查看更多日志信息：

```python
# 启用调试模式
ext_acc = ExtAccount(acc, debug=1)
```

## 注意事项

1. 部分高级功能可能受到Twitter API限制，使用前请确认您的账号有相应权限
2. 过于频繁的API请求可能导致账号被限制，请合理控制请求频率
3. 媒体上传功能需要完善，暂不完全支持，使用时请注意

## 与原生twscrape功能结合

ExtAccount可以与twscrape的现有功能结合使用，例如搜索推文后对结果进行操作：

```python
import asyncio
from twscrape import AccountsPool, API
from twscrape.ext_account import ExtAccount
from twscrape.logger import set_log_level

async def main():
    set_log_level("DEBUG")
    pool = AccountsPool("accounts.db")
    api = API(pool)
    
    # 添加/登录账号（如果需要）
    # await pool.add_account("username", "password", "email", "email_password")
    # await pool.login_all()
    
    # 使用原生API搜索推文
    async for tweet in api.search("python", limit=10):
        print(f"Found tweet: {tweet.id} - {tweet.rawContent}")
        
        # 获取一个账号进行操作
        acc = await pool.get_for_queue("like_tweets")
        if acc:
            try:
                # 创建扩展账号
                ext_acc = ExtAccount(acc)
                
                # 点赞找到的推文
                result = await ext_acc.like(tweet.id)
                print(f"Liked tweet {tweet.id}: {result}")
                
            finally:
                # 释放账号
                await pool.unlock(acc.username, "like_tweets")

if __name__ == "__main__":
    asyncio.run(main())
```

## 贡献

欢迎提交问题报告和功能请求。如果您想贡献代码，请提交Pull Request。 