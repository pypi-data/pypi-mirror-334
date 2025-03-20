# twscrape 媒体上传功能指南

twscrape 的扩展功能现在支持媒体上传，允许用户在发送推文和私信时附加图片、GIF和视频等媒体文件。本文档详细说明了媒体上传功能的使用方法和注意事项。

## 功能概述

- 支持上传图片、GIF和视频
- 支持为媒体添加描述文本(Alt Text)
- 兼容Twitter API的媒体类型和大小限制
- 支持在推文和私信中附加媒体
- 自动分块上传大文件
- 完全支持代理设置，确保媒体上传请求通过指定代理

## 媒体大小限制

twscrape 遵循 Twitter API 的媒体大小限制：

- 图片: 最大 5MB
- GIF: 最大 15MB
- 视频: 最大 530MB

超出大小限制的文件将无法上传。

## 使用方法

### 1. 通过 API 类发送带媒体的推文

```python
from twscrape import API

async def send_tweet_with_media():
    api = API()
    
    # 准备媒体参数
    media_params = [
        {
            "media": "path/to/image.jpg",  # 媒体文件路径
            "alt": "图片描述文本"          # 可选的描述文本
        }
    ]
    
    # 发送带媒体的推文
    result = await api.send_tweet("带图片的测试推文", media=media_params)
    print(result)
```

### 2. 通过 API 类发送带媒体的私信

```python
from twscrape import API

async def send_dm_with_media():
    api = API()
    
    # 发送私信
    receiver_id = 1234567890  # 接收者用户ID
    result = await api.send_dm("带图片的测试私信", [receiver_id], media="path/to/image.jpg")
    print(result)
```

### 3. 直接使用 ExtAccount 类上传媒体

对于需要更精细控制的情况，可以直接使用 ExtAccount 类的媒体上传功能：

```python
from twscrape.accounts_pool import AccountsPool
from twscrape.ext_account import ExtAccount

async def upload_media_directly():
    # 初始化账号池
    pool = AccountsPool()
    
    # 获取账号
    account = await pool.get_for_queue("media_upload")
    if not account:
        return
    
    try:
        # 创建ExtAccount实例
        ext_acc = ExtAccount(account, debug=1)
        
        # 上传媒体
        media_id = await ext_acc._upload_media("path/to/image.jpg")
        
        if media_id:
            # 添加描述文本(可选)
            await ext_acc._add_alt_text(media_id, "图片描述文本")
            
            # 使用已上传的媒体ID发送推文
            tweet_result = await ext_acc.tweet("带有已上传媒体的推文", media=[
                {"media": media_id, "tagged_users": []}
            ])
            print(tweet_result)
    finally:
        # 解锁账号
        await pool.unlock(account.username, "media_upload")
```

## 代理支持

媒体上传功能完全支持代理设置，与其他API请求保持一致的代理优先级：

1. 在API方法调用时指定的代理（例如 `api = API(proxy="http://proxy.example.com:8080")`）
2. 账号级别的代理（在添加账号时设置，例如 `await api.pool.add_account(..., proxy="http://proxy.example.com:8080")`）
3. 环境变量中的代理设置（`TWS_PROXY`）

媒体上传请求将按照上述优先级使用代理，确保与其他API请求保持一致的网络行为。

### 媒体上传代理设置示例

```python
from twscrape import API

# 方法1：API级别代理
api = API(proxy="http://proxy.example.com:8080", debug=True)

# 方法2：账号级别代理
await api.pool.add_account("username", "password", "email", "email_pwd", 
                          proxy="http://proxy.example.com:8080")

# 方法3：环境变量（在脚本运行前设置）
# export TWS_PROXY="http://proxy.example.com:8080"
```

## 命令行工具示例

twscrape 附带了一个媒体上传示例程序，可以用于测试媒体上传功能：

```bash
# 发送带媒体的推文
python -m twscrape.examples.media_upload_example --media path/to/image.jpg --text "测试推文" --alt "图片描述"

# 发送带媒体的私信
python -m twscrape.examples.media_upload_example --media path/to/image.jpg --dm 1234567890 --text "测试私信"

# 直接上传媒体(不发送推文)
python -m twscrape.examples.media_upload_example --media path/to/image.jpg --direct
```

运行 `python -m twscrape.examples.media_upload_example --help` 查看所有可用选项。

## 支持的媒体类型

- 图片: JPEG、PNG、WebP
- GIF: 动图或静态GIF
- 视频: MP4、MOV (推荐使用H.264编码的MP4)

## 错误处理和调试

媒体上传过程可能会遇到各种错误，以下是一些常见问题和解决方案：

1. **网络问题**: 
   - 确保您的网络连接稳定
   - 如果使用代理，确保代理服务器工作正常且能访问Twitter API
   - 启用debug模式（`api = API(debug=True)`）以查看详细的请求和响应信息

2. **文件相关问题**:
   - 确保文件路径正确且文件存在
   - 检查文件大小是否超过Twitter的限制
   - 确保文件格式被Twitter支持

3. **账号权限问题**:
   - 确保使用的Twitter账号没有被限制或封禁
   - 某些新账号可能暂时无法使用媒体上传功能

4. **调试方法**:
   ```python
   # 启用调试模式
   api = API(debug=True)
   
   # 或启用ExtAccount的调试模式
   ext_acc = ExtAccount(account, debug=1)
   ```

5. **常见错误代码**:
   - 400错误通常表示请求格式错误或参数问题
   - 401错误通常表示身份验证失败
   - 403错误通常表示权限问题
   - 429错误通常表示请求频率超限

错误处理示例：

```python
result = await api.send_dm("测试", [receiver_id], media="path/to/image.jpg")
if "error" in result:
    print(f"发送失败: {result['error']}")
    if "details" in result:
        print(f"详情: {result['details']}")
else:
    print("发送成功!")
```

## 注意事项

1. **代理支持**: 媒体上传功能完全支持代理设置，与其他API请求保持一致的代理优先级。

2. **错误处理**: 媒体上传过程中可能出现各种错误，如网络问题、文件过大或格式不支持等。API会返回包含错误信息的字典，格式为：

   ```python
   {"error": "错误信息", "details": "详细信息"}
   ```

3. **上传进度**: 媒体上传是分块进行的，日志中会显示上传进度信息。可以通过设置debug=1来查看更多日志信息。

4. **多媒体上传**: 目前推文可以附加多个媒体文件，但私信仅支持单个媒体文件。

5. **媒体处理**: 上传后，Twitter服务器可能需要时间处理媒体文件，特别是视频文件。ExtAccount类会等待处理完成。

## 高级定制

媒体上传功能可以进一步扩展，例如：

- 实现批量媒体上传
- 添加媒体处理功能(如调整大小、裁剪等)
- 实现更复杂的媒体上传策略

如有需要，可以修改 `_upload_media` 方法来实现这些功能。

## 兼容性说明

媒体上传功能与Twitter API的更改密切相关。如果Twitter更改其上传API，可能需要更新twscrape的实现。请确保使用最新版本的twscrape以获得最佳兼容性。 