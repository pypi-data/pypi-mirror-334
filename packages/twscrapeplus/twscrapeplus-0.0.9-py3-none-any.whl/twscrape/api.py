from contextlib import aclosing
from typing import Literal
from pathlib import Path

from httpx import Response

from .accounts_pool import AccountsPool
from .logger import set_log_level
from .models import Tweet, User, parse_trends, parse_tweet, parse_tweets, parse_user, parse_users
from .queue_client import QueueClient
from .utils import encode_params, find_obj, get_by_path
from .ext_account import ExtAccount

# OP_{NAME} – {NAME} should be same as second part of GQL ID (required to auto-update script)
OP_SearchTimeline = "U3QTLwGF8sZCHDuWIMSAmg/SearchTimeline"
OP_UserByRestId = "5vdJ5sWkbSRDiiNZvwc2Yg/UserByRestId"
OP_UserByScreenName = "32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName"
OP_TweetDetail = "Ez6kRPyXbqNlhBwcNMpU-Q/TweetDetail"
OP_Followers = "OGScL-RC4DFMsRGOCjPR6g/Followers"
OP_Following = "o5eNLkJb03ayTQa97Cpp7w/Following"
OP_Retweeters = "niCJ2QyTuAgZWv01E7mqJQ/Retweeters"
OP_UserTweets = "Y9WM4Id6UcGFE8Z-hbnixw/UserTweets"
OP_UserTweetsAndReplies = "pZXwh96YGRqmBbbxu7Vk2Q/UserTweetsAndReplies"
OP_ListLatestTweetsTimeline = "H_dAKg97dSn3FOMfrNS8nw/ListLatestTweetsTimeline"
OP_BlueVerifiedFollowers = "WijS8Cwfqhtk5hDN9q7sgw/BlueVerifiedFollowers"
OP_UserCreatorSubscriptions = "H4p-DZU4gYqcZulycazCZw/UserCreatorSubscriptions"
OP_UserMedia = "ophTtKkfXcUKnXlxh9fU5w/UserMedia"
OP_Bookmarks = "1vFR5f4iSCQZLzjdSsNYwA/Bookmarks"
OP_GenericTimelineById = "5u36Lskx1dfACjC_WHmH3Q/GenericTimelineById"

GQL_URL = "https://x.com/i/api/graphql"
GQL_FEATURES = {  # search values here (view source) https://x.com/
    "articles_preview_enabled": False,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "communities_web_enable_tweet_community_results_fetch": True,
    "creator_subscriptions_quote_tweet_preview_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_media_download_video_enabled": False,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "rweb_video_timestamps_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_awards_web_tipping_enabled": False,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "tweet_with_visibility_results_prefer_gql_media_interstitial_enabled": False,
    "tweetypie_unmention_optimization_enabled": True,
    "verified_phone_label_enabled": False,
    "view_counts_everywhere_api_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "premium_content_api_read_enabled": False,
    "profile_label_improvements_pcf_label_in_post_enabled": False,
    "responsive_web_grok_share_attachment_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": False,
    "responsive_web_grok_image_annotation_enabled": False,
    "responsive_web_grok_analysis_button_from_backend": False,
    "responsive_web_jetfuel_frame": False,
}

KV = dict | None
TrendId = Literal["trending", "news", "sport", "entertainment"] | str


class API:
    # Note: kv is variables, ft is features from original GQL request
    pool: AccountsPool

    def __init__(
        self,
        pool: AccountsPool | str | None = None,
        debug=False,
        proxy: str | None = None,
        raise_when_no_account=False,
    ):
        if isinstance(pool, AccountsPool):
            self.pool = pool
        elif isinstance(pool, str):
            self.pool = AccountsPool(db_file=pool, raise_when_no_account=raise_when_no_account)
        else:
            self.pool = AccountsPool(raise_when_no_account=raise_when_no_account)

        self.proxy = proxy
        self.debug = debug
        if self.debug:
            set_log_level("DEBUG")

    # general helpers

    def _is_end(self, rep: Response, q: str, res: list, cur: str | None, cnt: int, lim: int):
        new_count = len(res)
        new_total = cnt + new_count

        is_res = new_count > 0
        is_cur = cur is not None
        is_lim = lim > 0 and new_total >= lim

        return rep if is_res else None, new_total, is_cur and not is_lim

    def _get_cursor(self, obj: dict, cursor_type="Bottom") -> str | None:
        if cur := find_obj(obj, lambda x: x.get("cursorType") == cursor_type):
            return cur.get("value")
        return None

    # gql helpers

    async def _gql_items(
        self, op: str, kv: dict, ft: dict | None = None, limit=-1, cursor_type="Bottom"
    ):
        queue, cur, cnt, active = op.split("/")[-1], None, 0, True
        kv, ft = {**kv}, {**GQL_FEATURES, **(ft or {})}

        async with QueueClient(self.pool, queue, self.debug, proxy=self.proxy) as client:
            while active:
                params = {"variables": kv, "features": ft}
                if cur is not None:
                    params["variables"]["cursor"] = cur
                if queue in ("SearchTimeline", "ListLatestTweetsTimeline"):
                    params["fieldToggles"] = {"withArticleRichContentState": False}
                if queue in ("UserMedia",):
                    params["fieldToggles"] = {"withArticlePlainText": False}

                rep = await client.get(f"{GQL_URL}/{op}", params=encode_params(params))
                if rep is None:
                    return

                obj = rep.json()
                els = get_by_path(obj, "entries") or []
                els = [
                    x
                    for x in els
                    if not (
                        x["entryId"].startswith("cursor-")
                        or x["entryId"].startswith("messageprompt-")
                    )
                ]
                cur = self._get_cursor(obj, cursor_type)

                rep, cnt, active = self._is_end(rep, queue, els, cur, cnt, limit)
                if rep is None:
                    return

                yield rep

    async def _gql_item(self, op: str, kv: dict, ft: dict | None = None):
        ft = ft or {}
        queue = op.split("/")[-1]
        async with QueueClient(self.pool, queue, self.debug, proxy=self.proxy) as client:
            params = {"variables": {**kv}, "features": {**GQL_FEATURES, **ft}}
            return await client.get(f"{GQL_URL}/{op}", params=encode_params(params))

    # search

    async def search_raw(self, q: str, limit=-1, kv: KV = None):
        op = OP_SearchTimeline
        kv = {
            "rawQuery": q,
            "count": 20,
            "product": "Latest",
            "querySource": "typed_query",
            **(kv or {}),
        }
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def search(self, q: str, limit=-1, kv: KV = None):
        async with aclosing(self.search_raw(q, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    yield x

    async def search_user(self, q: str, limit=-1, kv: KV = None):
        kv = {"product": "People", **(kv or {})}
        async with aclosing(self.search_raw(q, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # user_by_id

    async def user_by_id_raw(self, uid: int, kv: KV = None):
        op = OP_UserByRestId
        kv = {"userId": str(uid), "withSafetyModeUserFields": True, **(kv or {})}
        ft = {
            "hidden_profile_likes_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "responsive_web_twitter_article_notes_tab_enabled": False,
            "subscriptions_feature_can_gift_premium": False,
            "profile_label_improvements_pcf_label_in_post_enabled": False,
        }
        return await self._gql_item(op, kv, ft)

    async def user_by_id(self, uid: int, kv: KV = None) -> User | None:
        rep = await self.user_by_id_raw(uid, kv=kv)
        return parse_user(rep) if rep else None

    # user_by_login

    async def user_by_login_raw(self, login: str, kv: KV = None):
        op = OP_UserByScreenName
        kv = {"screen_name": login, "withSafetyModeUserFields": True, **(kv or {})}
        ft = {
            "highlights_tweets_tab_ui_enabled": True,
            "hidden_profile_likes_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "subscriptions_verification_info_is_identity_verified_enabled": False,
            "responsive_web_twitter_article_notes_tab_enabled": False,
            "subscriptions_feature_can_gift_premium": False,
            "profile_label_improvements_pcf_label_in_post_enabled": False,
        }
        return await self._gql_item(op, kv, ft)

    async def user_by_login(self, login: str, kv: KV = None) -> User | None:
        rep = await self.user_by_login_raw(login, kv=kv)
        return parse_user(rep) if rep else None

    # tweet_details

    async def tweet_details_raw(self, twid: int, kv: KV = None):
        op = OP_TweetDetail
        kv = {
            "focalTweetId": str(twid),
            "with_rux_injections": True,
            "includePromotedContent": True,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withBirdwatchNotes": True,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }
        return await self._gql_item(op, kv)

    async def tweet_details(self, twid: int, kv: KV = None) -> Tweet | None:
        rep = await self.tweet_details_raw(twid, kv=kv)
        return parse_tweet(rep, twid) if rep else None

    # tweet_replies
    # note: uses same op as tweet_details, see: https://github.com/vladkens/twscrape/issues/104

    async def tweet_replies_raw(self, twid: int, limit=-1, kv: KV = None):
        op = OP_TweetDetail
        kv = {
            "focalTweetId": str(twid),
            "referrer": "tweet",
            "with_rux_injections": True,
            "includePromotedContent": True,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withBirdwatchNotes": True,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }
        async with aclosing(
            self._gql_items(op, kv, limit=limit, cursor_type="ShowMoreThreads")
        ) as gen:
            async for x in gen:
                yield x

    async def tweet_replies(self, twid: int, limit=-1, kv: KV = None):
        async with aclosing(self.tweet_replies_raw(twid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    if x.inReplyToTweetId == twid:
                        yield x

    # followers

    async def followers_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_Followers
        kv = {"userId": str(uid), "count": 20, "includePromotedContent": False, **(kv or {})}
        ft = {"responsive_web_twitter_article_notes_tab_enabled": False}
        async with aclosing(self._gql_items(op, kv, limit=limit, ft=ft)) as gen:
            async for x in gen:
                yield x

    async def followers(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.followers_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # verified_followers

    async def verified_followers_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_BlueVerifiedFollowers
        kv = {"userId": str(uid), "count": 20, "includePromotedContent": False, **(kv or {})}
        ft = {
            "responsive_web_twitter_article_notes_tab_enabled": True,
        }
        async with aclosing(self._gql_items(op, kv, limit=limit, ft=ft)) as gen:
            async for x in gen:
                yield x

    async def verified_followers(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.verified_followers_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # following

    async def following_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_Following
        kv = {"userId": str(uid), "count": 20, "includePromotedContent": False, **(kv or {})}
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def following(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.following_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # subscriptions

    async def subscriptions_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_UserCreatorSubscriptions
        kv = {"userId": str(uid), "count": 20, "includePromotedContent": False, **(kv or {})}
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def subscriptions(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.subscriptions_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # retweeters

    async def retweeters_raw(self, twid: int, limit=-1, kv: KV = None):
        op = OP_Retweeters
        kv = {"tweetId": str(twid), "count": 20, "includePromotedContent": True, **(kv or {})}
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def retweeters(self, twid: int, limit=-1, kv: KV = None):
        async with aclosing(self.retweeters_raw(twid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_users(rep.json(), limit):
                    yield x

    # user_tweets

    async def user_tweets_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_UserTweets
        kv = {
            "userId": str(uid),
            "count": 40,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def user_tweets(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.user_tweets_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    yield x

    # user_tweets_and_replies

    async def user_tweets_and_replies_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_UserTweetsAndReplies
        kv = {
            "userId": str(uid),
            "count": 40,
            "includePromotedContent": True,
            "withCommunity": True,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def user_tweets_and_replies(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.user_tweets_and_replies_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    yield x

    # user_media

    async def user_media_raw(self, uid: int, limit=-1, kv: KV = None):
        op = OP_UserMedia
        kv = {
            "userId": str(uid),
            "count": 40,
            "includePromotedContent": False,
            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }

        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def user_media(self, uid: int, limit=-1, kv: KV = None):
        async with aclosing(self.user_media_raw(uid, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep, limit):
                    # sometimes some tweets without media, so skip them
                    media_count = (
                        len(x.media.photos) + len(x.media.videos) + len(x.media.animated)
                        if x.media
                        else 0
                    )

                    if media_count > 0:
                        yield x

    # list_timeline

    async def list_timeline_raw(self, list_id: int, limit=-1, kv: KV = None):
        op = OP_ListLatestTweetsTimeline
        kv = {"listId": str(list_id), "count": 20, **(kv or {})}
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def list_timeline(self, list_id: int, limit=-1, kv: KV = None):
        async with aclosing(self.list_timeline_raw(list_id, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep, limit):
                    yield x

    # trends

    async def trends_raw(self, trend_id: TrendId, limit=-1, kv: KV = None):
        map = {
            "trending": "VGltZWxpbmU6DAC2CwABAAAACHRyZW5kaW5nAAA",
            "news": "VGltZWxpbmU6DAC2CwABAAAABG5ld3MAAA",
            "sport": "VGltZWxpbmU6DAC2CwABAAAABnNwb3J0cwAA",
            "entertainment": "VGltZWxpbmU6DAC2CwABAAAADWVudGVydGFpbm1lbnQAAA",
        }
        trend_id = map.get(trend_id, trend_id)

        op = OP_GenericTimelineById
        kv = {
            "timelineId": trend_id,
            "count": 20,
            "withQuickPromoteEligibilityTweetFields": True,
            **(kv or {}),
        }
        async with aclosing(self._gql_items(op, kv, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def trends(self, trend_id: TrendId, limit=-1, kv: KV = None):
        async with aclosing(self.trends_raw(trend_id, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_trends(rep, limit):
                    yield x

    async def search_trend(self, q: str, limit=-1, kv: KV = None):
        kv = {
            "querySource": "trend_click",
            **(kv or {}),
        }
        async with aclosing(self.search_raw(q, limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    yield x

    # Get current user bookmarks

    async def bookmarks_raw(self, limit=-1, kv: KV = None):
        op = OP_Bookmarks
        kv = {
            "count": 20,
            "includePromotedContent": False,
            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "withVoice": True,
            "withV2Timeline": True,
            **(kv or {}),
        }
        ft = {
            "graphql_timeline_v2_bookmark_timeline": True,
        }
        async with aclosing(self._gql_items(op, kv, ft, limit=limit)) as gen:
            async for x in gen:
                yield x

    async def bookmarks(self, limit=-1, kv: KV = None):
        async with aclosing(self.bookmarks_raw(limit=limit, kv=kv)) as gen:
            async for rep in gen:
                for x in parse_tweets(rep.json(), limit):
                    yield x

    async def _get_ext_account(self, queue="default_ext"):
        """获取一个账号并创建 ExtAccount 实例"""
        account = await self.pool.get_for_queue(queue)
        if not account:
            return None
        return ExtAccount(account, debug=self.debug, proxy=self.proxy)

    async def _with_ext_account(self, queue, callback):
        """使用ExtAccount执行操作并自动管理账号锁定和释放"""
        account = await self.pool.get_for_queue(queue)
        if not account:
            return None
        
        try:
            # 只有在API实例显式设置了代理时，才传递API代理
            proxy = self.proxy if self.proxy is not None else None
            ext_acc = ExtAccount(account, debug=self.debug, proxy=proxy)
            return await callback(ext_acc)
        finally:
            await self.pool.unlock(account.username, queue)

    # 发送私信
    async def send_dm(self, text: str, receivers: list[int], media: str = '', queue="send_dm"):
        """
        发送私信到指定用户
        
        Args:
            text: 私信文本内容
            receivers: 接收者ID列表
            media: 可选的媒体文件路径，传递给dm方法
            queue: 使用的账号队列名称
        
        Returns:
            API响应
        """
        if self.debug:
            set_log_level("DEBUG")
            print(f"DEBUG: 准备发送私信，API级别代理设置: {self.proxy}")
            
        account = await self.pool.get_for_queue(queue)
        if not account:
            error_msg = "无可用账号，无法执行发送私信操作"
            print(f"ERROR: {error_msg}")
            return {"error": error_msg}
        
        try:
            if self.debug:
                print(f"DEBUG: 获取到账号 {account.username}, 账号级代理设置: {account.proxy}")
                
            # 只有在API实例显式设置了代理时，才传递API代理
            proxy = self.proxy if self.proxy is not None else None
            ext_acc = ExtAccount(account, debug=self.debug, proxy=proxy)
            
            # 验证媒体文件是否存在
            if media and not Path(media).exists():
                error_msg = f"媒体文件不存在: {media}"
                print(f"ERROR: {error_msg}")
                return {"error": error_msg}
                
            # 调用dm方法发送私信
            result = await ext_acc.dm(text, receivers, media)
            
            if self.debug:
                print(f"DEBUG: 私信发送结果: {result}")
                
            return result
            
        except Exception as e:
            error_msg = f"发送私信操作异常: {str(e)}"
            import traceback
            print(f"ERROR: {error_msg}\n{traceback.format_exc()}")
            return {"error": error_msg}
            
        finally:
            await self.pool.unlock(account.username, queue)

    # 发送推文
    async def send_tweet(self, text: str, *, media=None, **kwargs):
        """发送推文"""
        async def _send(ext_acc):
            return await ext_acc.tweet(text, media=media, **kwargs)
        
        return await self._with_ext_account("send_tweet", _send)

    # 点赞
    async def like_tweet(self, tweet_id: int):
        """点赞推文"""
        async def _like(ext_acc):
            return await ext_acc.like(tweet_id)
        
        return await self._with_ext_account("like_tweet", _like)

    # 取消点赞
    async def unlike_tweet(self, tweet_id: int):
        """取消点赞"""
        async def _unlike(ext_acc):
            return await ext_acc.unlike(tweet_id)
        
        return await self._with_ext_account("unlike_tweet", _unlike)

    # 转发
    async def retweet(self, tweet_id: int):
        """转发推文"""
        async def _retweet(ext_acc):
            return await ext_acc.retweet(tweet_id)
        
        return await self._with_ext_account("retweet", _retweet)

    # 取消转发
    async def unretweet(self, tweet_id: int):
        """取消转发推文"""
        async def _unretweet(ext_acc):
            return await ext_acc.unretweet(tweet_id)
        
        return await self._with_ext_account("unretweet", _unretweet)

    # 书签操作
    async def bookmark_tweet(self, tweet_id: int):
        """将推文加入书签"""
        async def _bookmark(ext_acc):
            return await ext_acc.bookmark(tweet_id)
        
        return await self._with_ext_account("bookmark", _bookmark)

    async def unbookmark_tweet(self, tweet_id: int):
        """将推文从书签中移除"""
        async def _unbookmark(ext_acc):
            return await ext_acc.unbookmark(tweet_id)
        
        return await self._with_ext_account("unbookmark", _unbookmark)

    # 置顶推文操作
    async def pin_tweet(self, tweet_id: int):
        """置顶推文"""
        async def _pin(ext_acc):
            return await ext_acc.pin(tweet_id)
        
        return await self._with_ext_account("pin_tweet", _pin)

    async def unpin_tweet(self, tweet_id: int):
        """取消置顶推文"""
        async def _unpin(ext_acc):
            return await ext_acc.unpin(tweet_id)
        
        return await self._with_ext_account("unpin_tweet", _unpin)

    # 用户操作
    async def follow_user(self, user_id: int):
        """关注用户"""
        async def _follow(ext_acc):
            return await ext_acc.follow(user_id)
        
        return await self._with_ext_account("follow", _follow)

    async def unfollow_user(self, user_id: int):
        """取消关注用户"""
        async def _unfollow(ext_acc):
            return await ext_acc.unfollow(user_id)
        
        return await self._with_ext_account("unfollow", _unfollow)

    async def mute_user(self, user_id: int):
        """将用户静音"""
        async def _mute(ext_acc):
            return await ext_acc.mute(user_id)
        
        return await self._with_ext_account("mute_user", _mute)

    async def unmute_user(self, user_id: int):
        """取消用户静音"""
        async def _unmute(ext_acc):
            return await ext_acc.unmute(user_id)
        
        return await self._with_ext_account("unmute_user", _unmute)

    async def block_user(self, user_id: int):
        """屏蔽用户"""
        async def _block(ext_acc):
            return await ext_acc.block(user_id)
        
        return await self._with_ext_account("block_user", _block)

    async def unblock_user(self, user_id: int):
        """取消屏蔽用户"""
        async def _unblock(ext_acc):
            return await ext_acc.unblock(user_id)
        
        return await self._with_ext_account("unblock_user", _unblock)

    # 列表操作
    async def create_list(self, name: str, description: str, private: bool = False):
        """创建列表"""
        async def _create_list(ext_acc):
            return await ext_acc.create_list(name, description, private)
        
        return await self._with_ext_account("list_operation", _create_list)

    async def update_list(self, list_id: int, name: str, description: str, private: bool):
        """更新列表"""
        async def _update_list(ext_acc):
            return await ext_acc.update_list(list_id, name, description, private)
        
        return await self._with_ext_account("list_operation", _update_list)

    async def delete_list(self, list_id: int):
        """删除列表"""
        async def _delete_list(ext_acc):
            return await ext_acc.delete_list(list_id)
        
        return await self._with_ext_account("list_operation", _delete_list)

    async def add_list_member(self, list_id: int, user_id: int):
        """添加用户到列表"""
        async def _add_member(ext_acc):
            return await ext_acc.add_list_member(list_id, user_id)
        
        return await self._with_ext_account("list_operation", _add_member)

    async def remove_list_member(self, list_id: int, user_id: int):
        """从列表中移除用户"""
        async def _remove_member(ext_acc):
            return await ext_acc.remove_list_member(list_id, user_id)
        
        return await self._with_ext_account("list_operation", _remove_member)

    # 话题操作
    async def follow_topic(self, topic_id: int):
        """关注话题"""
        async def _follow_topic(ext_acc):
            return await ext_acc.follow_topic(topic_id)
        
        return await self._with_ext_account("topic_operation", _follow_topic)

    async def unfollow_topic(self, topic_id: int):
        """取消关注话题"""
        async def _unfollow_topic(ext_acc):
            return await ext_acc.unfollow_topic(topic_id)
        
        return await self._with_ext_account("topic_operation", _unfollow_topic)

    # 草稿和定时推文操作
    async def get_draft_tweets(self, ascending: bool = True):
        """获取草稿推文"""
        async def _get_drafts(ext_acc):
            return await ext_acc.draft_tweets(ascending)
        
        return await self._with_ext_account("tweet_drafts", _get_drafts)

    async def delete_draft_tweet(self, tweet_id: int):
        """删除草稿推文"""
        async def _delete_draft(ext_acc):
            return await ext_acc.delete_draft_tweet(tweet_id)
        
        return await self._with_ext_account("tweet_drafts", _delete_draft)

    async def get_scheduled_tweets(self, ascending: bool = True):
        """获取已安排的定时推文"""
        async def _get_scheduled(ext_acc):
            return await ext_acc.scheduled_tweets(ascending)
        
        return await self._with_ext_account("scheduled_tweets", _get_scheduled)

    async def schedule_tweet(self, text: str, date: str | int, media=None):
        """安排定时发送推文"""
        async def _schedule(ext_acc):
            return await ext_acc.schedule_tweet(text, date, media=media)
        
        return await self._with_ext_account("scheduled_tweets", _schedule)

    async def delete_scheduled_tweet(self, tweet_id: int):
        """删除已安排的定时推文"""
        async def _delete_scheduled(ext_acc):
            return await ext_acc.unschedule_tweet(tweet_id)
        
        return await self._with_ext_account("scheduled_tweets", _delete_scheduled)

    # 回复操作
    async def reply_to_tweet(self, text: str, tweet_id: int):
        """回复推文"""
        async def _reply(ext_acc):
            return await ext_acc.reply(text, tweet_id)
        
        return await self._with_ext_account("reply_tweet", _reply)

    async def quote_tweet(self, text: str, tweet_id: int):
        """引用推文"""
        async def _quote(ext_acc):
            return await ext_acc.quote(text, tweet_id)
        
        return await self._with_ext_account("quote_tweet", _quote)
