import asyncio
import hashlib
import logging
import math
import mimetypes
import platform
import orjson
import json
import random
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from string import ascii_letters
from uuid import uuid1, getnode
from urllib.parse import urlencode
from typing import Any, Dict, List, Tuple, Optional, Union

from httpx import AsyncClient, Response

from .account import Account
from .utils import utc

# 媒体上传的常量
MAX_IMAGE_SIZE = 5_242_880  # ~5 MB
MAX_GIF_SIZE = 15_728_640  # ~15 MB
MAX_VIDEO_SIZE = 536_870_912  # ~530 MB
UPLOAD_CHUNK_SIZE = 4 * 1024 * 1024  # 4MB chunks
MEDIA_UPLOAD_SUCCEED = 'succeeded'
MEDIA_UPLOAD_FAIL = 'failed'

# 模拟twitter-api-client中的必要常量和工具函数
class Operation:
    default_features = {
        # 从twitter-api-client/constants.py同步的default_features
        'c9s_tweet_anatomy_moderator_badge_enabled': True,
        'responsive_web_home_pinned_timelines_enabled': True,
        'blue_business_profile_image_shape_enabled': True,
        'creator_subscriptions_tweet_preview_api_enabled': True,
        'freedom_of_speech_not_reach_fetch_enabled': True,
        'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
        'graphql_timeline_v2_bookmark_timeline': True,
        'hidden_profile_likes_enabled': True,
        'highlights_tweets_tab_ui_enabled': True,
        'interactive_text_enabled': True,
        'longform_notetweets_consumption_enabled': True,
        'longform_notetweets_inline_media_enabled': True,
        'longform_notetweets_rich_text_read_enabled': True,
        'longform_notetweets_richtext_consumption_enabled': True,
        'profile_foundations_tweet_stats_enabled': True,
        'profile_foundations_tweet_stats_tweet_frequency': True,
        'responsive_web_birdwatch_note_limit_enabled': True,
        'responsive_web_edit_tweet_api_enabled': True,
        'responsive_web_enhance_cards_enabled': False,
        'responsive_web_graphql_exclude_directive_enabled': True,
        'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
        'responsive_web_graphql_timeline_navigation_enabled': True,
        'responsive_web_media_download_video_enabled': False,
        'responsive_web_text_conversations_enabled': False,
        'responsive_web_twitter_article_data_v2_enabled': True,
        'responsive_web_twitter_article_tweet_consumption_enabled': False,
        'responsive_web_twitter_blue_verified_badge_is_enabled': True,
        'rweb_lists_timeline_redesign_enabled': True,
        'spaces_2022_h2_clipping': True,
        'spaces_2022_h2_spaces_communities': True,
        'standardized_nudges_misinfo': True,
        'subscriptions_verification_info_verified_since_enabled': True,
        'tweet_awards_web_tipping_enabled': False,
        'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
        'tweetypie_unmention_optimization_enabled': True,
        'verified_phone_label_enabled': False,
        'vibe_api_enabled': True,
        'view_counts_everywhere_api_enabled': True
    }
    
    # 从twitter-api-client/constants.py同步的GraphQL操作ID
    # Account Operations
    useSendMessageMutation = ('MaxK2PKX1F9Z-9SwqwavTw', 'useSendMessageMutation')
    CreateTweet = ('7TKRKCPuAGsmYde0CudbVg', 'CreateTweet')
    DeleteTweet = ('VaenaVgh5q5ih7kvyVjgtg', 'DeleteTweet')
    CreateScheduledTweet = ('LCVzRQGxOaGnOnYH01NQXg', 'CreateScheduledTweet')
    DeleteScheduledTweet = ('CTOVqej0JBXAZSwkp1US0g', 'DeleteScheduledTweet')
    CreateRetweet = ('ojPdsZsimiJrUGLR1sjUtA', 'CreateRetweet')
    DeleteRetweet = ('iQtK4dl5hBmXewYZuEOKVw', 'DeleteRetweet')
    FavoriteTweet = ('lI07N6Otwv1PhnEgXILM7A', 'FavoriteTweet')
    UnfavoriteTweet = ('ZYKSe-w7KEslx3JhSIk5LA', 'UnfavoriteTweet')
    CreateBookmark = ('aoDbu3RHznuiSkQ9aNM67Q', 'CreateBookmark')
    DeleteBookmark = ('Wlmlj2-xzyS1GN3a6cj-mQ', 'DeleteBookmark')
    Pin = ('sLVLhk0bGj3MVFEKTdax1w', 'Pin')
    Unpin = ('MvGift6qYI65UTDyAQU17g', 'Unpin')
    FollowUser = ('LPGv0smB-4D9DlRDkMsmdw', 'FollowUser')
    UnfollowUser = ('QOyVFEHb0gVNmTDgJGi-OQ', 'UnfollowUser')
    BlockUser = ('ax0taHTQFtBFpEc-5f4iRw', 'BlockUser')
    UnblockUser = ('PM6JnXScGbKmR5nNoEjT9Q', 'UnblockUser')
    MuteUser = ('pMW94Iu5H6r7ZKtJSFL6VQ', 'MuteUser')
    UnmuteUser = ('Hvx1Km66g20CilgWZ3LoXg', 'UnmuteUser')
    CreateList = ('hQAsnViq2BrMLbPuQ9umDA', 'CreateList')
    UpdateList = ('4dCEFWtxEbhnSLcJdJ6PNg', 'UpdateList')
    ListsPinMany = ('2X4Vqu6XLneR-XZnGK5MAw', 'ListsPinMany')
    ListPinOne = ('2pYlo-kjdXoNOZJoLzI6KA', 'ListPinOne')
    ListUnpinOne = ('c4ce-hzx6V4heV5IzdeBkA', 'ListUnpinOne')
    ListAddMember = ('P8tyfv2_0HzofrB5f6_ugw', 'ListAddMember')
    ListRemoveMember = ('DBZowzFN492FFkBPBptCwg', 'ListRemoveMember')
    DeleteList = ('UnN9Th1BDbeLjpgjGSpL3Q', 'DeleteList')
    EditListBanner = ('Uk0ZwKSMYng56aQdeJD1yw', 'EditListBanner')
    DeleteListBanner = ('-bOKetDVCMl20qXn7YDXIA', 'DeleteListBanner')
    TopicFollow = ('ElqSLWFmsPL4NlZI5e1Grg', 'TopicFollow')
    TopicUnfollow = ('srwjU6JM_ZKTj_QMfUGNcw', 'TopicUnfollow')
    HomeLatestTimeline = ('zhX91JE87mWvfprhYE97xA', 'HomeLatestTimeline')
    HomeTimeline = ('HCosKfLNW1AcOo3la3mMgg', 'HomeTimeline')
    Bookmarks = ('tmd4ifV8RHltzn8ymGg1aw', 'Bookmarks')
    EnableFollowerNotifications = ('MlFaFxL1NpSEOnnLjQ4Mpw', 'EnableFollowerNotifications') 
    DisableFollowerNotifications = ('9xRlIZGO0GdlLx0FqtEjEw', 'DisableFollowerNotifications')
    DMMessageDeleteMutation = ('BJ6DtxA2llfjnRoRjaiIiw', 'DMMessageDeleteMutation')
    UpdatePinnedLists = ('2X4Vqu6XLneR-XZnGK5MAw', 'UpdatePinnedLists')
    CreateDraftTweet = ('cH9HZWz_EW9gnswvA4ZRiQ', 'CreateDraftTweet')
    DeleteDraftTweet = ('bkh9G3FGgTldS9iTKWWYYw', 'DeleteDraftTweet')
    FetchDraftTweets = ('ZkqIq_xRhiUme0PBJNpRtg', 'FetchDraftTweets')
    FetchScheduledTweets = ('ITtjAzvlZni2wWXwf295Qg', 'FetchScheduledTweets')
    
    # 定义与twitter-api-client/constants.py中相同的default_variables
    default_variables = {
        'count': 1000,
        'withSafetyModeUserFields': True,
        'includePromotedContent': True,
        'withQuickPromoteEligibilityTweetFields': True,
        'withVoice': True,
        'withV2Timeline': True,
        'withDownvotePerspective': False,
        'withBirdwatchNotes': True,
        'withCommunity': True,
        'withSuperFollowsUserFields': True,
        'withReactionsMetadata': False,
        'withReactionsPerspective': False,
        'withSuperFollowsTweetFields': True,
        'isMetatagsQuery': False,
        'withReplays': True,
        'withClientEventToken': False,
        'withAttachments': True,
        'withConversationQueryHighlights': True,
        'withMessageQueryHighlights': True,
        'withMessages': True,
    }

# 日志记录设置
def get_logger():
    logger = logging.getLogger("ext_account")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def get_headers(client):
    """获取标准请求头"""
    headers = {}
    if hasattr(client, 'headers'):
        headers = dict(client.headers)
    return headers

def find_key(data, key):
    """在嵌套字典中递归查找键"""
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_key(v, key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result = find_key(item, key)
                if result is not None:
                    return result
    return None

class ExtAccount:
    """扩展Account类，添加twitter-api-client中Account类的功能"""
    
    def __init__(self, account: Account, debug: int = 0, proxy: str | None = None):
        self.account = account
        self.debug = debug
        self.proxy = proxy  # API级别的代理设置
        self.gql_api = 'https://twitter.com/i/api/graphql'
        self.v1_api = 'https://api.twitter.com/1.1'
        self.v2_api = 'https://twitter.com/i/api/2'
        self.logger = get_logger()
        self.rate_limits = {}
        
    async def init_client(self):
        """初始化并返回HTTP客户端"""
        if self.debug:
            self.logger.debug(f"初始化HTTP客户端，API级别代理: {self.proxy}, 账号级别代理: {self.account.proxy}")
        
        import httpx
        import warnings
        
        # 忽略SSL验证警告
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        
        client = self.account.make_client(proxy=self.proxy)
        client.verify = False
        
        # 增加超时设置，解决上传媒体时的超时问题
        client.timeout = httpx.Timeout(connect=60.0, read=180.0, write=180.0, pool=60.0)
        
        # 确保关键头信息存在
        client.headers.update({
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
            "authority": "upload.twitter.com",
            "accept": "*/*",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/"
        })
        
        if self.debug and hasattr(client, '_transport'):
            self.logger.debug(f"客户端已配置的代理: {client._transport._proxy}")
            
        return client
    
    async def gql(self, method: str, operation: tuple, variables: dict, features: dict = Operation.default_features) -> dict:
        """执行GraphQL API请求"""
        client = await self.init_client()
        qid, op = operation
        params = {
            'queryId': qid,
            'features': features,
            'variables': Operation.default_variables | variables
        }
        if method == 'POST':
            data = {'json': params}
        else:
            data = {'params': {k: orjson.dumps(v).decode() for k, v in params.items()}}
        
        try:
            r = await client.request(
                method=method,
                url=f'{self.gql_api}/{qid}/{op}',
                headers=get_headers(client),
                **data
            )
            
            self.rate_limits[op] = {k: int(v) for k, v in r.headers.items() if 'rate-limit' in k}
            if self.debug:
                self.logger.debug(f"Status: {r.status_code}")
                self.logger.debug(f"Headers: {r.headers}")
                self.logger.debug(f"Response: {r.text}")
            
            # 检查响应状态和内容
            if r.status_code != 200:
                self.logger.error(f"GraphQL请求失败: {r.status_code} - {r.text}")
                return {"error": f"请求失败: {r.status_code}", "details": r.text}
            
            if not r.text.strip():
                self.logger.error("GraphQL返回空响应")
                return {"error": "空响应"}
            
            return r.json()
        except Exception as e:
            self.logger.error(f"GraphQL请求异常: {str(e)}")
            return {"error": f"请求异常: {str(e)}"}

    async def v1(self, path: str, params: dict) -> dict:
        """执行Twitter API v1请求"""
        client = await self.init_client()
        headers = get_headers(client)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        
        r = await client.post(f'{self.v1_api}/{path}', headers=headers, data=urlencode(params))
        if self.debug:
            self.logger.debug(f"Status: {r.status_code}")
            self.logger.debug(f"Headers: {r.headers}")
            self.logger.debug(f"Response: {r.text}")
            
        return r.json()
    
    async def create_poll(self, text: str, choices: list[str], poll_duration: int) -> dict:
        """创建投票"""
        client = await self.init_client()
        options = {
            "twitter:card": "poll4choice_text_only",
            "twitter:api:api:endpoint": "1",
            "twitter:long:duration_minutes": poll_duration  # max: 10080
        }
        
        for i, c in enumerate(choices):
            options[f"twitter:string:choice{i + 1}_label"] = c

        headers = get_headers(client)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = 'https://caps.twitter.com/v2/cards/create.json'
        
        r = await client.post(url, headers=headers, params={'card_data': orjson.dumps(options).decode()})
        card_uri = r.json()['card_uri']
        r = await self.tweet(text, poll_params={'card_uri': card_uri})
        
        return r

    async def dm(self, text: str, receivers: list[int], media: str = '') -> dict:
        """发送私信"""
        try:
            variables = {
                "message": {},
                "requestId": str(uuid1(getnode())),
                "target": {"participant_ids": receivers},
            }
            
            if media:
                self.logger.info(f"私信需要上传媒体: {media}")
                
                # 确保媒体文件存在
                if not Path(media).exists():
                    error_msg = f"媒体文件不存在: {media}"
                    self.logger.error(error_msg)
                    return {"error": error_msg}
                
                # 上传媒体文件
                media_id = await self._upload_media(media, is_dm=True)
                
                if not media_id:
                    error_msg = "媒体上传失败，无法发送带附件的私信"
                    self.logger.error(error_msg)
                    return {"error": error_msg}
                
                self.logger.info(f"媒体上传成功，media_id: {media_id}，继续发送私信")
                variables['message']['media'] = {'id': media_id, 'text': text}
            else:
                self.logger.info("发送纯文本私信")
                variables['message']['text'] = {'text': text}
            
            self.logger.info(f"发送私信到用户IDs: {receivers}")
            
            # 使用GraphQL API发送私信
            try:
                res = await self.gql('POST', Operation.useSendMessageMutation, variables)
                
                if self.debug:
                    self.logger.debug(f"私信发送响应: {res}")
                
                if 'error' in res:
                    self.logger.error(f"发送私信失败: {res['error']}")
                    return res
                
                if find_key(res, 'dm_validation_failure_type'):
                    error_msg = f"发送私信验证失败: {find_key(res, 'dm_validation_failure_type')}"
                    self.logger.error(error_msg)
                    return {"error": error_msg, "details": res}
                
                self.logger.info("私信发送成功")
                return res
                
            except Exception as e:
                error_msg = f"发送私信请求过程中发生异常: {str(e)}"
                self.logger.error(error_msg)
                import traceback
                self.logger.error(traceback.format_exc())
                return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"发送私信过程中发生异常: {str(e)}"
            self.logger.error(error_msg)
            import traceback
            self.logger.error(traceback.format_exc())
            return {"error": error_msg}

    async def tweet(self, text: str, *, media: any = None, **kwargs) -> dict:
        """发送推文"""
        variables = {
            'tweet_text': text,
            'dark_request': False,
            'media': {
                'media_entities': [],
                'possibly_sensitive': False,
            },
            'semantic_annotation_ids': [],
        }

        if reply_params := kwargs.get('reply_params', {}):
            variables |= reply_params
        if quote_params := kwargs.get('quote_params', {}):
            variables |= quote_params
        if poll_params := kwargs.get('poll_params', {}):
            variables |= poll_params

        draft = kwargs.get('draft')
        schedule = kwargs.get('schedule')

        if draft or schedule:
            variables = {
                'post_tweet_request': {
                    'auto_populate_reply_metadata': False,
                    'status': text,
                    'exclude_reply_user_ids': [],
                    'media_ids': [],
                },
            }
            
            if media:
                for m in media:
                    media_id = await self._upload_media(m['media'])
                    variables['post_tweet_request']['media_ids'].append(media_id)
                    if alt := m.get('alt'):
                        await self._add_alt_text(media_id, alt)

            if schedule:
                variables['execute_at'] = (
                    datetime.strptime(schedule, "%Y-%m-%d %H:%M").timestamp()
                    if isinstance(schedule, str)
                    else schedule
                )
                return await self.gql('POST', Operation.CreateScheduledTweet, variables)

            return await self.gql('POST', Operation.CreateDraftTweet, variables)

        # 常规推文
        if media:
            for m in media:
                media_id = await self._upload_media(m['media'])
                variables['media']['media_entities'].append({
                    'media_id': media_id,
                    'tagged_users': m.get('tagged_users', [])
                })
                if alt := m.get('alt'):
                    await self._add_alt_text(media_id, alt)

        return await self.gql('POST', Operation.CreateTweet, variables)

    async def schedule_tweet(self, text: str, date: int | str, *, media: list = None) -> dict:
        """安排推文发送时间"""
        variables = {
            'post_tweet_request': {
                'auto_populate_reply_metadata': False,
                'status': text,
                'exclude_reply_user_ids': [],
                'media_ids': [],
            },
            'execute_at': (
                datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp()
                if isinstance(date, str)
                else date
            ),
        }
        
        if media:
            for m in media:
                media_id = await self._upload_media(m['media'])
                variables['post_tweet_request']['media_ids'].append(media_id)
                if alt := m.get('alt'):
                    await self._add_alt_text(media_id, alt)
                    
        return await self.gql('POST', Operation.CreateScheduledTweet, variables)

    async def schedule_reply(self, text: str, date: int | str, tweet_id: int, *, media: list = None) -> dict:
        """安排回复发送时间"""
        variables = {
            'post_tweet_request': {
                'auto_populate_reply_metadata': True,
                'in_reply_to_status_id': tweet_id,
                'status': text,
                'exclude_reply_user_ids': [],
                'media_ids': [],
            },
            'execute_at': (
                datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp()
                if isinstance(date, str)
                else date
            ),
        }
        
        if media:
            for m in media:
                media_id = await self._upload_media(m['media'])
                variables['post_tweet_request']['media_ids'].append(media_id)
                if alt := m.get('alt'):
                    await self._add_alt_text(media_id, alt)
                    
        return await self.gql('POST', Operation.CreateScheduledTweet, variables)

    async def unschedule_tweet(self, tweet_id: int) -> dict:
        """取消已安排的推文"""
        variables = {'scheduled_tweet_id': tweet_id}
        return await self.gql('POST', Operation.DeleteScheduledTweet, variables)

    async def untweet(self, tweet_id: int) -> dict:
        """删除推文"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.DeleteTweet, variables)

    async def reply(self, text: str, tweet_id: int) -> dict:
        """回复推文"""
        variables = {
            'tweet_text': text,
            'reply': {
                'in_reply_to_tweet_id': tweet_id,
                'exclude_reply_user_ids': [],
            },
            'batch_compose': 'BatchSubsequent',
            'dark_request': False,
            'media': {
                'media_entities': [],
                'possibly_sensitive': False,
            },
            'semantic_annotation_ids': [],
        }
        return await self.gql('POST', Operation.CreateTweet, variables)

    async def quote(self, text: str, tweet_id: int) -> dict:
        """引用推文"""
        variables = {
            'tweet_text': text,
            'attachment_url': f'https://twitter.com/i/status/{tweet_id}',
            'dark_request': False,
            'media': {
                'media_entities': [],
                'possibly_sensitive': False,
            },
            'semantic_annotation_ids': [],
        }
        return await self.gql('POST', Operation.CreateTweet, variables)
    
    async def retweet(self, tweet_id: int) -> dict:
        """转发推文"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.CreateRetweet, variables)
    
    async def unretweet(self, tweet_id: int) -> dict:
        """取消转发"""
        variables = {'source_tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.DeleteRetweet, variables)
    
    async def like(self, tweet_id: int) -> dict:
        """点赞推文"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.FavoriteTweet, variables)
    
    async def unlike(self, tweet_id: int) -> dict:
        """取消点赞"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.UnfavoriteTweet, variables)
    
    async def bookmark(self, tweet_id: int) -> dict:
        """收藏推文"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.CreateBookmark, variables)
    
    async def unbookmark(self, tweet_id: int) -> dict:
        """取消收藏"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.DeleteBookmark, variables)
    
    async def pin(self, tweet_id: int) -> dict:
        """置顶推文"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.Pin, variables)
    
    async def unpin(self, tweet_id: int) -> dict:
        """取消置顶"""
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql('POST', Operation.Unpin, variables)
    
    async def follow(self, user_id: int) -> dict:
        """关注用户"""
        variables = {'user_id': str(user_id), 'dark_request': False}
        return await self.gql('POST', Operation.FollowUser, variables)
    
    async def unfollow(self, user_id: int) -> dict:
        """取消关注"""
        variables = {'user_id': str(user_id), 'dark_request': False}
        return await self.gql('POST', Operation.UnfollowUser, variables)
    
    async def mute(self, user_id: int) -> dict:
        """静音用户"""
        variables = {'user_id': str(user_id)}
        return await self.gql('POST', Operation.MuteUser, variables)
    
    async def unmute(self, user_id: int) -> dict:
        """取消静音"""
        variables = {'user_id': str(user_id)}
        return await self.gql('POST', Operation.UnmuteUser, variables)
    
    async def enable_follower_notifications(self, user_id: int) -> dict:
        """开启用户通知"""
        variables = {'id': str(user_id), 'notification_types': ['1', '2', '3', '5', '6'], 'dark_request': False}
        return await self.gql('POST', Operation.EnableFollowerNotifications, variables)
    
    async def disable_follower_notifications(self, user_id: int) -> dict:
        """关闭用户通知"""
        variables = {'id': str(user_id), 'dark_request': False}
        return await self.gql('POST', Operation.DisableFollowerNotifications, variables)
    
    async def block(self, user_id: int) -> dict:
        """拉黑用户"""
        variables = {'user_id': str(user_id)}
        return await self.gql('POST', Operation.BlockUser, variables)
    
    async def unblock(self, user_id: int) -> dict:
        """取消拉黑"""
        variables = {'user_id': str(user_id)}
        return await self.gql('POST', Operation.UnblockUser, variables)
    
    async def create_list(self, name: str, description: str, private: bool) -> dict:
        """创建列表"""
        variables = {'name': name, 'description': description, 'is_private': private}
        return await self.gql('POST', Operation.CreateList, variables)
    
    async def update_list(self, list_id: int, name: str, description: str, private: bool) -> dict:
        """更新列表"""
        variables = {'id': str(list_id), 'name': name, 'description': description, 'is_private': private}
        return await self.gql('POST', Operation.UpdateList, variables)
    
    async def update_pinned_lists(self, list_ids: list[int]) -> dict:
        """更新已置顶列表"""
        variables = {'list_ids': [str(i) for i in list_ids], 'display_location': 'Top'}
        return await self.gql('POST', Operation.UpdatePinnedLists, variables)
    
    async def pin_list(self, list_id: int) -> dict:
        """置顶列表"""
        return await self.update_pinned_lists([list_id])
    
    async def unpin_list(self, list_id: int) -> dict:
        """取消置顶列表"""
        return await self.update_pinned_lists([])
    
    async def add_list_member(self, list_id: int, user_id: int) -> dict:
        """向列表添加成员"""
        variables = {'list_id': str(list_id), 'user_id': str(user_id)}
        return await self.gql('POST', Operation.ListAddMember, variables)
    
    async def remove_list_member(self, list_id: int, user_id: int) -> dict:
        """从列表移除成员"""
        variables = {'list_id': str(list_id), 'user_id': str(user_id)}
        return await self.gql('POST', Operation.ListRemoveMember, variables)
    
    async def delete_list(self, list_id: int) -> dict:
        """删除列表"""
        variables = {'list_id': str(list_id)}
        return await self.gql('POST', Operation.DeleteList, variables)
    
    async def update_list_banner(self, list_id: int, media: str) -> dict:
        """更新列表横幅"""
        media_id = await self._upload_media(media)
        variables = {'list_id': str(list_id), 'media_id': str(media_id)}
        return await self.gql('POST', Operation.EditListBanner, variables)
    
    async def delete_list_banner(self, list_id: int) -> dict:
        """删除列表横幅"""
        variables = {'list_id': str(list_id)}
        return await self.gql('POST', Operation.DeleteListBanner, variables)
    
    async def follow_topic(self, topic_id: int) -> dict:
        """关注话题"""
        variables = {'topicId': str(topic_id)}
        return await self.gql('POST', Operation.TopicFollow, variables)
    
    async def unfollow_topic(self, topic_id: int) -> dict:
        """取消关注话题"""
        variables = {'topicId': str(topic_id)}
        return await self.gql('POST', Operation.TopicUnfollow, variables)
    
    async def update_profile_image(self, media: str) -> Response:
        """更新个人资料图片"""
        client = await self.init_client()
        media_id = await self._upload_media(media, is_profile=True)
        
        url = f"{self.v1_api}/account/update_profile_image.json"
        params = {"media_id": media_id}
        
        r = await client.post(url, headers=get_headers(client), data=urlencode(params))
        if self.debug:
            self.logger.debug(f"Status: {r.status_code}")
            self.logger.debug(f"Response: {r.text}")
            
        return r
    
    async def update_profile_banner(self, media: str) -> Response:
        """更新个人资料横幅"""
        client = await self.init_client()
        media_id = await self._upload_media(media, is_profile=True)
        
        url = f"{self.v1_api}/account/update_profile_banner.json"
        params = {"media_id": media_id}
        
        r = await client.post(url, headers=get_headers(client), data=urlencode(params))
        if self.debug:
            self.logger.debug(f"Status: {r.status_code}")
            self.logger.debug(f"Response: {r.text}")
            
        return r
    
    async def update_profile_info(self, **kwargs) -> Response:
        """更新个人资料信息"""
        client = await self.init_client()
        url = f"{self.v1_api}/account/update_profile.json"
        
        r = await client.post(url, headers=get_headers(client), data=urlencode(kwargs))
        if self.debug:
            self.logger.debug(f"Status: {r.status_code}")
            self.logger.debug(f"Response: {r.text}")
            
        return r
    
    async def update_search_settings(self, settings: dict) -> Response:
        """更新搜索设置"""
        client = await self.init_client()
        url = f"{self.v1_api}/strato/column/Search/config.json"
        
        default = {"use_latest_endpoint": True, "ranked_timeline": True}
        params = default | settings
        
        r = await client.post(url, headers=get_headers(client), data=urlencode(params))
        if self.debug:
            self.logger.debug(f"Status: {r.status_code}")
            self.logger.debug(f"Response: {r.text}")
            
        return r
    
    async def update_settings(self, settings: dict) -> dict:
        """更新设置"""
        return await self.v1("account/settings.json", settings)
    
    async def change_password(self, old: str, new: str) -> dict:
        """修改密码"""
        client = await self.init_client()
        flow_token = (
            await client.get(
                "https://twitter.com/i/api/1.1/account/password_strength_verification.json"
            )
        ).json()["flow_token"]
        
        params = {
            "flow_token": flow_token,
            "password": old,
            "password_new": new,
            "password_conf": new,
        }
        
        url = "https://twitter.com/i/api/1.1/account/password_change.json"
        res = await client.post(url, data=urlencode(params), headers=get_headers(client))
        
        return res.json()
    
    async def _upload_media(self, filename: str, is_dm: bool = False, is_profile=False) -> int | None:
        """
        异步上传媒体文件至Twitter服务器
        参考: https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/uploading-media/media-best-practices
        
        Args:
            filename: 要上传的媒体文件路径
            is_dm: 是否用于私信
            is_profile: 是否用于个人资料
            
        Returns:
            媒体ID (如成功)或None (如失败)
        """
        def check_media(category: str, size: int) -> None:
            """检查媒体尺寸是否符合Twitter限制"""
            fmt = lambda x: f'{(x / 1e6):.2f} MB'
            msg = lambda x: f'无法上传 {fmt(size)} 大小的{category}，最大允许大小为 {fmt(x)}'
            if category == 'image' and size > MAX_IMAGE_SIZE:
                raise Exception(msg(MAX_IMAGE_SIZE))
            if category == 'gif' and size > MAX_GIF_SIZE:
                raise Exception(msg(MAX_GIF_SIZE))
            if category == 'video' and size > MAX_VIDEO_SIZE:
                raise Exception(msg(MAX_VIDEO_SIZE))

        # 设置上传URL
        url = 'https://upload.twitter.com/i/media/upload.json'

        # 获取文件信息
        file = Path(filename)
        if not file.exists():
            self.logger.error(f"文件不存在: {filename}")
            return None
            
        total_bytes = file.stat().st_size
        
        try:
            # 获取客户端和标头
            self.logger.info(f"准备上传媒体，文件: {filename}, 大小: {total_bytes} 字节")
            if self.debug:
                self.logger.debug(f"使用代理上传媒体: API级别代理={self.proxy}, 账号级别代理={self.account.proxy}")
                
            client = await self.init_client()
            headers = get_headers(client)

            # 记录当前客户端的代理配置
            if self.debug and hasattr(client, '_transport'):
                self.logger.debug(f"上传客户端实际使用的代理: {client._transport._proxy}")

            # 确定媒体类型和类别
            upload_type = 'dm' if is_dm else 'tweet'
            media_type = mimetypes.guess_type(file)[0]
            if not media_type:
                # 尝试根据扩展名猜测类型
                ext = file.suffix.lower()
                if ext in ['.jpg', '.jpeg']:
                    media_type = 'image/jpeg'
                elif ext == '.png':
                    media_type = 'image/png'
                elif ext == '.gif':
                    media_type = 'image/gif'
                elif ext in ['.mp4', '.mov']:
                    media_type = 'video/mp4'
                else:
                    self.logger.error(f"无法确定文件类型: {filename}")
                    return None
                    
            media_category = f'{upload_type}_gif' if 'gif' in media_type else f'{upload_type}_{media_type.split("/")[0]}'
            self.logger.info(f"媒体分类: {media_category}, 类型: {media_type}")

            # 检查媒体尺寸限制
            media_type_simple = media_category.split('_')[1]
            self.logger.debug(f"检查媒体尺寸限制，类型: {media_type_simple}, 大小: {total_bytes}")
            check_media(media_type_simple, total_bytes)

            # INIT - 初始化上传
            self.logger.info(f"初始化上传: {file.name} ({media_type}, {total_bytes} 字节)")
            params = {
                'command': 'INIT', 
                'media_type': media_type, 
                'total_bytes': total_bytes,
                'media_category': media_category
            }
            try:
                r = await client.post(url=url, headers=headers, params=params)
                
                if self.debug:
                    self.logger.debug(f"INIT 请求 URL: {r.request.url}")
                    self.logger.debug(f"INIT 响应状态: {r.status_code}")
                    self.logger.debug(f"INIT 响应内容: {r.text}")
                
                if r.status_code >= 400:
                    self.logger.error(f"初始化上传失败: 状态码={r.status_code}, 响应={r.text}")
                    return None

                media_id = r.json()['media_id']
                self.logger.info(f"获取到media_id: {media_id}")
            except Exception as e:
                self.logger.error(f"初始化上传过程中发生异常: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())
                return None

            # APPEND - 分块上传文件
            self.logger.info(f"开始分块上传 {file.name}")
            with open(file, 'rb') as fp:
                segment_index = 0
                bytes_sent = 0
                
                while chunk := fp.read(UPLOAD_CHUNK_SIZE):
                    bytes_sent += len(chunk)
                    progress = int(bytes_sent / total_bytes * 100)
                    self.logger.info(f"上传进度: {progress}% ({bytes_sent}/{total_bytes})")
                    
                    params = {
                        'command': 'APPEND', 
                        'media_id': media_id, 
                        'segment_index': segment_index
                    }
                    
                    # 尝试方法1: 使用自定义构建的multipart请求 (twitter-api-client方式)
                    try:
                        pad = ''.join(random.choices(ascii_letters, k=16)).encode('utf-8')
                        boundary = b'------WebKitFormBoundary' + pad
                        data = b''.join([
                            boundary,
                            b'\r\nContent-Disposition: form-data; name="media"; filename="blob"',
                            b'\r\nContent-Type: application/octet-stream',
                            b'\r\n\r\n',
                            chunk,
                            b'\r\n',
                            boundary,
                            b'--\r\n',
                        ])
                        
                        custom_headers = dict(headers)
                        custom_headers['content-type'] = f'multipart/form-data; boundary=----WebKitFormBoundary{pad.decode()}'
                        
                        r = await client.post(
                            url=url, 
                            headers=custom_headers, 
                            params=params, 
                            content=data
                        )
                        
                        if self.debug:
                            self.logger.debug(f"APPEND #{segment_index} (方法1) 响应状态: {r.status_code}")
                        
                        if r.status_code < 200 or r.status_code > 299:
                            self.logger.warning(f"方法1上传分块失败，尝试方法2: {r.status_code}")
                            raise Exception("尝试备用方法")
                            
                    except Exception as e:
                        # 方法1失败，尝试方法2: 使用files参数 (现有方式)
                        try:
                            self.logger.info(f"尝试备用方法上传分块 #{segment_index}")
                            files = {'media': chunk}
                            r = await client.post(url=url, headers=headers, params=params, files=files)
                            
                            if self.debug:
                                self.logger.debug(f"APPEND #{segment_index} (方法2) 响应状态: {r.status_code}")
                            
                            if r.status_code < 200 or r.status_code > 299:
                                self.logger.error(f"上传分块失败: 状态码={r.status_code}, 响应={r.text}")
                                return None
                                
                        except Exception as sub_e:
                            self.logger.error(f"所有上传方法均失败: {str(sub_e)}")
                            import traceback
                            self.logger.error(traceback.format_exc())
                            return None

                    segment_index += 1

            # FINALIZE - 完成上传
            self.logger.info("分块上传完成，开始定稿")
            params = {'command': 'FINALIZE', 'media_id': media_id, 'allow_async': 'true'}
            if is_dm:
                # 为DM添加MD5校验
                file_bytes = Path(filename).read_bytes()
                params |= {'original_md5': hashlib.md5(file_bytes).hexdigest()}
                
            try:
                r = await client.post(url=url, headers=headers, params=params)
                
                if self.debug:
                    self.logger.debug(f"FINALIZE 响应状态: {r.status_code}")
                    self.logger.debug(f"FINALIZE 响应内容: {r.text}")
                
                if r.status_code >= 400:
                    self.logger.error(f"定稿失败: 状态码={r.status_code}, 响应={r.text}")
                    return None

                # 处理媒体处理状态
                response_json = r.json()
                processing_info = response_json.get('processing_info')
                
                while processing_info:
                    state = processing_info['state']
                    self.logger.info(f"媒体处理状态: {state}")
                    
                    if error := processing_info.get("error"):
                        self.logger.error(f"媒体处理错误: {error}")
                        return None
                        
                    if state == MEDIA_UPLOAD_SUCCEED:
                        break
                        
                    if state == MEDIA_UPLOAD_FAIL:
                        self.logger.error(f"媒体处理失败: {response_json}")
                        return None
                        
                    check_after_secs = processing_info.get('check_after_secs', random.randint(1, 5))
                    self.logger.info(f"媒体处理中，{check_after_secs}秒后检查状态...")
                    await asyncio.sleep(check_after_secs)
                    
                    params = {'command': 'STATUS', 'media_id': media_id}
                    r = await client.get(url=url, headers=headers, params=params)
                    
                    if self.debug:
                        self.logger.debug(f"STATUS 响应状态: {r.status_code}")
                        self.logger.debug(f"STATUS 响应内容: {r.text}")
                        
                    if r.status_code >= 400:
                        self.logger.error(f"检查状态失败: 状态码={r.status_code}, 响应={r.text}")
                        return None
                        
                    response_json = r.json()
                    processing_info = response_json.get('processing_info')
            except Exception as e:
                self.logger.error(f"定稿或检查状态过程中发生异常: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())
                return None

            self.logger.info(f"媒体上传成功，ID: {media_id}")
            return media_id
            
        except Exception as e:
            self.logger.error(f"媒体上传过程中发生异常: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None

    async def _add_alt_text(self, media_id: int, text: str) -> Response:
        """添加媒体描述文本(Alt Text)"""
        client = await self.init_client()
        params = {"media_id": str(media_id), "alt_text": {"text": text}}
        url = f"{self.v1_api}/media/metadata/create.json"
        
        headers = get_headers(client)
        headers['content-type'] = 'application/json'  # 确保内容类型正确
        
        r = await client.post(url, headers=headers, json=params)
        
        if self.debug:
            self.logger.debug(f"添加Alt Text结果: {r.status_code} {r.text}")
        
        return r
    
    @property
    def id(self) -> int:
        """获取用户ID"""
        # 模拟实现，实际应从account对象中获取
        return 0
        
    async def home_timeline(self, limit=math.inf) -> list[dict]:
        """获取主页时间线"""
        # 简化实现，应该使用_paginate方法实现
        self.logger.info(f"Home timeline functionality is not fully implemented yet")
        return []
        
    async def home_latest_timeline(self, limit=math.inf) -> list[dict]:
        """获取最新主页时间线"""
        # 简化实现
        self.logger.info(f"Home latest timeline functionality is not fully implemented yet")
        return []
        
    async def bookmarks(self, limit=math.inf) -> list[dict]:
        """获取收藏列表"""
        # 简化实现
        self.logger.info(f"Bookmarks functionality is not fully implemented yet")
        return []
        
    async def dm_inbox(self) -> dict:
        """获取私信收件箱"""
        # 简化实现
        self.logger.info(f"DM inbox functionality is not fully implemented yet")
        return {}
        
    async def dm_history(self, conversation_ids: list[str] = None) -> list[dict]:
        """获取私信历史"""
        # 简化实现
        self.logger.info(f"DM history functionality is not fully implemented yet")
        return []
        
    async def dm_delete(self, *, conversation_id: str = None, message_id: str = None) -> dict:
        """删除私信"""
        # 简化实现
        self.logger.info(f"DM delete functionality is not fully implemented yet")
        return {}
        
    async def scheduled_tweets(self, ascending: bool = True) -> dict:
        """获取已安排的推文"""
        # 简化实现
        self.logger.info(f"Scheduled tweets functionality is not fully implemented yet")
        return {}
        
    async def draft_tweets(self, ascending: bool = True) -> dict:
        """获取草稿推文"""
        # 简化实现
        self.logger.info(f"Draft tweets functionality is not fully implemented yet")
        return {}
        
    async def save_cookies(self, fname: str = None):
        """保存cookies"""
        # 不需要实现，twscrape会自行管理cookies
        self.logger.info(f"Cookie management is handled by twscrape")
        return 