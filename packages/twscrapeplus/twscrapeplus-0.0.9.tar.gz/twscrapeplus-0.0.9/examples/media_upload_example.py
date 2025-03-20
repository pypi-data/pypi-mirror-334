#!/usr/bin/env python
"""
媒体上传示例程序 - 展示如何使用扩展的媒体上传功能
"""

import asyncio
import os
import argparse
from twscrape import API
from twscrape.accounts_pool import AccountsPool
from twscrape.ext_account import ExtAccount
from twscrape.logger import set_log_level

async def upload_and_tweet(api, media_path, alt_text=None, tweet_text=None):
    """使用API发送带有媒体的推文"""
    if not os.path.exists(media_path):
        print(f"错误: 找不到媒体文件 {media_path}")
        return
    
    if not tweet_text:
        tweet_text = f"测试推文，上传媒体文件: {os.path.basename(media_path)}"
    
    print(f"正在发送带有媒体的推文: {tweet_text}")
    print(f"媒体文件: {media_path}")
    
    # 准备媒体参数
    media_params = [{"media": media_path}]
    if alt_text:
        media_params[0]["alt"] = alt_text
        print(f"媒体描述文本: {alt_text}")
    
    # 发送推文
    result = await api.send_tweet(tweet_text, media=media_params)
    
    # 处理结果
    if "error" in result:
        print(f"发送失败: {result['error']}")
        if "details" in result:
            print(f"详细信息: {result['details']}")
    else:
        print("推文发送成功!")
        try:
            if "data" in result and "create_tweet" in result["data"]:
                tweet_id = result["data"]["create_tweet"]["tweet"]["rest_id"]
                print(f"推文ID: {tweet_id}")
        except:
            print("无法获取推文ID")
    
    return result

async def upload_and_dm(api, receiver_id, media_path, dm_text=None):
    """使用API发送带有媒体的私信"""
    if not os.path.exists(media_path):
        print(f"错误: 找不到媒体文件 {media_path}")
        return
    
    if not dm_text:
        dm_text = f"测试私信，上传媒体文件: {os.path.basename(media_path)}"
    
    print(f"正在发送带有媒体的私信: {dm_text}")
    print(f"媒体文件: {media_path}")
    print(f"接收者ID: {receiver_id}")
    
    # 发送私信
    result = await api.send_dm(dm_text, [receiver_id], media=media_path)
    
    # 处理结果
    if "error" in result:
        print(f"发送失败: {result['error']}")
        if "details" in result:
            print(f"详细信息: {result['details']}")
    else:
        print("私信发送成功!")
    
    return result

async def direct_upload_example(pool_db_path, media_path, alt_text=None):
    """直接使用ExtAccount类上传媒体的示例"""
    # 初始化账号池
    pool = AccountsPool(db_file=pool_db_path)
    
    # 获取账号
    account = await pool.get_for_queue("media_upload_test")
    if not account:
        print("错误: 没有可用的账号")
        return None
    
    try:
        # 创建ExtAccount实例
        ext_acc = ExtAccount(account, debug=1)
        
        # 直接上传媒体
        print(f"正在直接上传媒体文件: {media_path}")
        media_id = await ext_acc._upload_media(media_path)
        
        if not media_id:
            print("媒体上传失败")
            return None
        
        print(f"媒体上传成功! ID: {media_id}")
        
        # 添加描述文本(如果提供)
        if alt_text:
            print(f"正在添加媒体描述文本: {alt_text}")
            alt_result = await ext_acc._add_alt_text(media_id, alt_text)
            print(f"描述文本添加结果: {alt_result.status_code}")
        
        return media_id
    
    finally:
        # 解锁账号
        await pool.unlock(account.username, "media_upload_test")

async def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="媒体上传示例程序")
    parser.add_argument("--db", default="accounts.db", help="账号数据库文件路径")
    parser.add_argument("--media", required=True, help="要上传的媒体文件路径")
    parser.add_argument("--alt", help="媒体描述文本")
    parser.add_argument("--text", help="推文文本")
    parser.add_argument("--dm", help="发送私信的接收者ID")
    parser.add_argument("--direct", action="store_true", help="直接使用ExtAccount上传而不发推文")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        set_log_level("DEBUG")
    
    # 确认文件存在
    if not os.path.exists(args.media):
        print(f"错误: 媒体文件不存在: {args.media}")
        return
    
    # 直接上传测试
    if args.direct:
        await direct_upload_example(args.db, args.media, args.alt)
        return
    
    # 初始化API
    api = API(args.db, debug=args.debug)
    
    # 检查账号登录状态
    accounts = await api.pool.get_all()
    active_accounts = [acc for acc in accounts if acc.active]
    
    if not active_accounts:
        print("错误: 没有已登录的账号")
        return
    
    print(f"找到 {len(active_accounts)} 个活跃账号")
    
    if args.dm:
        # 发送私信
        try:
            receiver_id = int(args.dm)
            await upload_and_dm(api, receiver_id, args.media, args.text)
        except ValueError:
            print(f"错误: 无效的接收者ID: {args.dm}")
    else:
        # 发送推文
        await upload_and_tweet(api, args.media, args.alt, args.text)

if __name__ == "__main__":
    asyncio.run(main()) 