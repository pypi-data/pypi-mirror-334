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

# twscrape 代理使用指南

twscrape 提供了多层级的代理设置，以满足不同场景的需求。本文档详细说明了代理的设置方式和优先级。

## 代理优先级

在 twscrape 中，代理设置的优先级从高到低为：

1. **方法调用时指定的代理**：优先级最高，会覆盖其他所有代理设置
2. **API 级别的代理**：在创建 API 实例时设置，会覆盖账号级别的代理
3. **环境变量代理**：通过 `TWS_PROXY` 环境变量设置，适用于全局配置
4. **账号级别的代理**：在添加账号时为每个账号单独设置的代理

如果所有级别都未设置代理，则不使用代理进行连接。

## 设置方式

### 1. 方法调用时指定代理

某些方法支持在调用时直接指定代理，这将覆盖所有其他代理设置：

```python
# 暂未实现此功能
```

### 2. API 级别代理

在创建 API 实例时设置代理：

```python
from twscrape import API

# 创建 API 实例时设置代理
api = API(proxy="http://user:pass@proxy.example.com:8080")

# 使用 API 的所有方法都将使用此代理
user = await api.user_by_login("twitter")
```

### 3. 环境变量代理

设置 `TWS_PROXY` 环境变量：

```bash
# Linux/Mac
export TWS_PROXY="socks5://user:pass@proxy.example.com:1080"

# Windows
set TWS_PROXY=socks5://user:pass@proxy.example.com:1080
```

在代码中：

```python
import os
os.environ["TWS_PROXY"] = "socks5://user:pass@proxy.example.com:1080"

from twscrape import API
api = API()  # 将使用环境变量中的代理
```

### 4. 账号级别代理

为特定账号设置代理：

```python
from twscrape import API

api = API()
await api.pool.add_account(
    username="myaccount",
    password="mypassword",
    email="my@email.com",
    email_password="emailpass",
    proxy="http://user:pass@proxy.example.com:8080"
)
```

## 扩展功能中的代理使用

扩展功能 (`ext_account.py`) 现在也完全支持多层级代理设置，与原生 twscrape 方法行为一致：

### 直接使用 ExtAccount

```python
from twscrape.accounts_pool import AccountsPool
from twscrape.ext_account import ExtAccount

# 初始化账号池
pool = AccountsPool()

# 获取账号
account = await pool.get_for_queue("example")

# 创建 ExtAccount 实例，设置 API 级别代理
ext_acc = ExtAccount(account, proxy="http://api_proxy:8080")

# 发送推文
result = await ext_acc.tweet("测试推文")
```

### 通过 API 类使用扩展功能

```python
from twscrape import API

# 创建 API 实例，设置代理
api = API(proxy="http://api_proxy:8080")

# 使用扩展功能
await api.send_tweet("测试推文")  # 将使用 API 级别的代理
await api.send_dm("测试私信", [1234567890])
```

## 代理类型

twscrape 支持多种代理类型：

- HTTP 代理：`http://user:pass@host:port`
- HTTPS 代理：`https://user:pass@host:port`
- SOCKS5 代理：`socks5://user:pass@host:port`

## 优先级验证示例

```python
import os
from twscrape import API
from twscrape.ext_account import ExtAccount

# 设置不同级别的代理
os.environ["TWS_PROXY"] = "http://env_proxy:8080"

api = API(proxy="http://api_proxy:8080")

# 添加账号，设置账号级别代理
await api.pool.add_account(
    username="user",
    password="pass",
    email="email",
    email_password="email_pass",
    proxy="http://account_proxy:8080"
)

# 获取账号
account = await api.pool.get_for_queue("test")

# 优先级顺序：
# 1. 方法级别代理：暂不支持
# 2. API 级别代理：http://api_proxy:8080 (将使用此代理)
# 3. 环境变量代理：http://env_proxy:8080
# 4. 账号级别代理：http://account_proxy:8080

# 使用 API 的扩展方法
await api.send_tweet("测试推文")  # 使用 API 级别代理

# 直接使用 ExtAccount，但不传递代理参数
ext_acc = ExtAccount(account)  # 只使用账号级别代理

# 直接使用 ExtAccount，传递自定义代理
ext_acc = ExtAccount(account, proxy="http://custom_proxy:8080")  # 使用自定义代理
```

## 注意事项

1. 确保代理服务器可用且配置正确，否则请求可能会失败
2. 使用 SOCKS5 代理需要安装额外的依赖：`pip install httpx[socks]`
3. 不同代理可能有不同的性能和稳定性，建议测试后选择最适合的方案
4. 频繁使用同一个代理 IP 可能导致 Twitter 的速率限制，建议使用代理池或轮换代理 

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

# twscrape

<div align="center">

[<img src="https://badges.ws/pypi/v/twscrape" alt="version" />](https://pypi.org/project/twscrape)
[<img src="https://badges.ws/pypi/python/twscrape" alt="py versions" />](https://pypi.org/project/twscrape)
[<img src="https://badges.ws/pypi/dm/twscrape" alt="downloads" />](https://pypi.org/project/twscrape)
[<img src="https://badges.ws/github/license/vladkens/twscrape" alt="license" />](https://github.com/vladkens/twscrape/blob/main/LICENSE)
[<img src="https://badges.ws/badge/-/buy%20me%20a%20coffee/ff813f?icon=buymeacoffee&label" alt="donate" />](https://buymeacoffee.com/vladkens)

</div>

Twitter GraphQL API implementation with [SNScrape](https://github.com/JustAnotherArchivist/snscrape) data models.

<div align="center">
  <img src=".github/example.png" alt="example of cli usage" height="400px">
</div>

## Install

```bash
pip install twscrape
```
Or development version:
```bash
pip install git+https://github.com/vladkens/twscrape.git
```

## Features
- Support both Search & GraphQL Twitter API
- Async/Await functions (can run multiple scrapers in parallel at the same time)
- Login flow (with receiving verification code from email)
- Saving/restoring account sessions
- Raw Twitter API responses & SNScrape models
- Automatic account switching to smooth Twitter API rate limits

## Usage

This project requires authorized X/Twitter accounts to work with the API. You have two options:

1. **Create Your Own Account**: While you can register a new account on X/Twitter yourself, it's can be difficult due to strict verification processes and high ban rates.

2. **Use Ready Accounts**: For immediate access, you can get ready-to-use accounts with cookies from [our recommended provider](https://kutt.it/ueeM5f). Cookie-based accounts typically have fewer login issues.

For optimal performance and to avoid IP-based restrictions, we also recommend using proxies from [our provider](https://kutt.it/eb3rXk).

**Disclaimer**: While X/Twitter's Terms of Service discourage using multiple accounts, this is a common practice for data collection and research purposes. Use responsibly and at your own discretion.

```python
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

async def main():
    api = API()  # or API("path-to.db") – default is `accounts.db`

    # ADD ACCOUNTS (for CLI usage see next readme section)

    # Option 1. Adding account with cookies (more stable)
    cookies = "abc=12; ct0=xyz"  # or '{"abc": "12", "ct0": "xyz"}'
    await api.pool.add_account("user3", "pass3", "u3@mail.com", "mail_pass3", cookies=cookies)

    # Option2. Adding account with login / password (less stable)
    # email login / password required to receive the verification code via IMAP protocol
    # (not all email providers are supported, e.g. ProtonMail)
    await api.pool.add_account("user1", "pass1", "u1@example.com", "mail_pass1")
    await api.pool.add_account("user2", "pass2", "u2@example.com", "mail_pass2")
    await api.pool.login_all() # try to login to receive account cookies

    # API USAGE

    # search (latest tab)
    await gather(api.search("elon musk", limit=20))  # list[Tweet]
    # change search tab (product), can be: Top, Latest (default), Media
    await gather(api.search("elon musk", limit=20, kv={"product": "Top"}))

    # tweet info
    tweet_id = 20
    await api.tweet_details(tweet_id)  # Tweet
    await gather(api.retweeters(tweet_id, limit=20))  # list[User]

    # Note: this method have small pagination from X side, like 5 tweets per query
    await gather(api.tweet_replies(tweet_id, limit=20))  # list[Tweet]

    # get user by login
    user_login = "xdevelopers"
    await api.user_by_login(user_login)  # User

    # user info
    user_id = 2244994945
    await api.user_by_id(user_id)  # User
    await gather(api.following(user_id, limit=20))  # list[User]
    await gather(api.followers(user_id, limit=20))  # list[User]
    await gather(api.verified_followers(user_id, limit=20))  # list[User]
    await gather(api.subscriptions(user_id, limit=20))  # list[User]
    await gather(api.user_tweets(user_id, limit=20))  # list[Tweet]
    await gather(api.user_tweets_and_replies(user_id, limit=20))  # list[Tweet]
    await gather(api.user_media(user_id, limit=20))  # list[Tweet]

    # list info
    await gather(api.list_timeline(list_id=123456789))

    # trends
    await gather(api.trends("news"))  # list[Trend]
    await gather(api.trends("sport"))  # list[Trend]
    await gather(api.trends("VGltZWxpbmU6DAC2CwABAAAACHRyZW5kaW5nAAA"))  # list[Trend]

    # NOTE 1: gather is a helper function to receive all data as list, FOR can be used as well:
    async for tweet in api.search("elon musk"):
        print(tweet.id, tweet.user.username, tweet.rawContent)  # tweet is `Tweet` object

    # NOTE 2: all methods have `raw` version (returns `httpx.Response` object):
    async for rep in api.search_raw("elon musk"):
        print(rep.status_code, rep.json())  # rep is `httpx.Response` object

    # change log level, default info
    set_log_level("DEBUG")

    # Tweet & User model can be converted to regular dict or json, e.g.:
    doc = await api.user_by_id(user_id)  # User
    doc.dict()  # -> python dict
    doc.json()  # -> json string

if __name__ == "__main__":
    asyncio.run(main())
```

### Stoping iteration with break

In order to correctly release an account in case of `break` in loop, a special syntax must be used. Otherwise, Python's events loop will release lock on the account sometime in the future. See explanation [here](https://github.com/vladkens/twscrape/issues/27#issuecomment-1623395424).

```python
from contextlib import aclosing

async with aclosing(api.search("elon musk")) as gen:
    async for tweet in gen:
        if tweet.id < 200:
            break
```

## CLI

### Get help on CLI commands

```sh
# show all commands
twscrape

# help on specific comand
twscrape search --help
```

### Add accounts

To add accounts use `add_accounts` command. Command syntax is:
```sh
twscrape add_accounts <file_path> <line_format>
```

Where:
`<line_format>` is format of line if accounts file splited by delimeter. Possible tokens:
- `username` – required
- `password` – required
- `email` – required
- `email_password` – to receive email code (you can use `--manual` mode to get code)
- `cookies` – can be any parsable format (string, json, base64 string, etc)
- `_` – skip column from parse

Tokens should be splited by delimeter, usually "`:`" used.

Example:

I have account files named `order-12345.txt` with format:
```text
username:password:email:email password:user_agent:cookies
```

Command to add accounts will be (user_agent column skiped with `_`):
```sh
twscrape add_accounts ./order-12345.txt username:password:email:email_password:_:cookies
```

### Login accounts

_Note:_ If you added accounts with cookies, login not required.

Run:

```sh
twscrape login_accounts
```

`twscrape` will start login flow for each new account. If X will ask to verify email and you provided `email_password` in `add_account`, then `twscrape` will try to receive verification code by IMAP protocol. After success login account cookies will be saved to db file for future use.

#### Manual email verification

In case your email provider not support IMAP protocol (ProtonMail, Tutanota, etc) or IMAP is disabled in settings, you can enter email verification code manually. To do this run login command with `--manual` flag.

Example:

```sh
twscrape login_accounts --manual
twscrape relogin user1 user2 --manual
twscrape relogin_failed --manual
```

### Get list of accounts and their statuses

```sh
twscrape accounts

# Output:
# username  logged_in  active  last_used            total_req  error_msg
# user1     True       True    2023-05-20 03:20:40  100        None
# user2     True       True    2023-05-20 03:25:45  120        None
# user3     False      False   None                 120        Login error
```

### Re-login accounts

It is possible to re-login specific accounts:

```sh
twscrape relogin user1 user2
```

Or retry login for all failed logins:

```sh
twscrape relogin_failed
```

### Use different accounts file

Useful if using a different set of accounts for different actions

```
twscrape --db test-accounts.db <command>
```

### Search commands

```sh
twscrape search "QUERY" --limit=20
twscrape tweet_details TWEET_ID
twscrape tweet_replies TWEET_ID --limit=20
twscrape retweeters TWEET_ID --limit=20
twscrape user_by_id USER_ID
twscrape user_by_login USERNAME
twscrape user_media USER_ID --limit=20
twscrape following USER_ID --limit=20
twscrape followers USER_ID --limit=20
twscrape verified_followers USER_ID --limit=20
twscrape subscriptions USER_ID --limit=20
twscrape user_tweets USER_ID --limit=20
twscrape user_tweets_and_replies USER_ID --limit=20
twscrape trends sport
```

The default output is in the console (stdout), one document per line. So it can be redirected to the file.

```sh
twscrape search "elon mask lang:es" --limit=20 > data.txt
```

By default, parsed data is returned. The original tweet responses can be retrieved with `--raw` flag.

```sh
twscrape search "elon mask lang:es" --limit=20 --raw
```

### About `limit` param

X API works through pagination, each API method can have different defaults for per page parameter (and this parameter can't be changed by caller). So `limit` param in `twscrape` is the desired number of objects (tweets or users, depending on the method). `twscrape` tries to return NO LESS objects than requested. If the X API returns less or more objects, `twscrape` will return whatever X gives.

## Proxy

There are few options to use proxies.

1. You can add proxy per account

```py
proxy = "http://login:pass@example.com:8080"
await api.pool.add_account("user4", "pass4", "u4@mail.com", "mail_pass4", proxy=proxy)
```

2. You can use global proxy for all accounts

```py
proxy = "http://login:pass@example.com:8080"
api = API(proxy=proxy)
doc = await api.user_by_login("elonmusk")
```

3. Use can set proxy with environemt variable `TWS_RPOXY`:

```sh
TWS_PROXY=socks5://user:pass@127.0.0.1:1080 twscrape user_by_login elonmusk
```

4. You can change proxy any time like:

```py
api.proxy = "socks5://user:pass@127.0.0.1:1080"
doc = await api.user_by_login("elonmusk")  # new proxy will be used
api.proxy = None
doc = await api.user_by_login("elonmusk")  # no proxy used
```

5. Proxy priorities

- `api.proxy` have top priority
- `env.proxy` will be used if `api.proxy` is None
- `acc.proxy` have lowest priotity

So if you want to use proxy PER ACCOUNT, do NOT override proxy with env variable or by passing proxy param to API.

_Note:_ If proxy not working, exception will be raised from API class.

## Environment Variables

- `TWS_PROXY` - global proxy for all accounts (e.g. `socks5://user:pass@127.0.0.1:1080`)
- `TWS_WAIT_EMAIL_CODE` - timeout for email verification code during login (default: `30`, in seconds)
- `TWS_RAISE_WHEN_NO_ACCOUNT` - raise `NoAccountError` exception when no available accounts, instead of waiting (default: `false`, values: `false`/`0`/`true`/`1`)

## Limitations

X/Twitter regularly [updates](https://x.com/elonmusk/status/1675187969420828672) their rate limits. Current basic behavior:
- Request limits reset every 15 minutes for each endpoint individually
- Each account has separate limits for different operations (search, profile views, etc.)

API data limitations:
- `user_tweets` & `user_tweets_and_replies` - can return ~3200 tweets maximum
- Rate limits may vary based on account age and status

## Articles
- [How to still scrape millions of tweets in 2023](https://medium.com/@vladkens/how-to-still-scrape-millions-of-tweets-in-2023-using-twscrape-97f5d3881434)
- [_(Add Article)_](https://github.com/vladkens/twscrape/edit/main/readme.md)

## See also
- [twitter-advanced-search](https://github.com/igorbrigadir/twitter-advanced-search) – guide on search filters
- [twitter-api-client](https://github.com/trevorhobenshield/twitter-api-client) – Implementation of Twitter's v1, v2, and GraphQL APIs
- [snscrape](https://github.com/JustAnotherArchivist/snscrape) – is a scraper for social networking services (SNS)
- [twint](https://github.com/twintproject/twint) – Twitter Intelligence Tool
