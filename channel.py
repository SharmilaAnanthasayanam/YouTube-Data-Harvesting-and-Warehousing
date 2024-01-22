from urllib.error import HTTPError
import playlist
from cleantext import clean
from datetime import datetime


def channel_request (channel_id, youtube):
    try:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id= channel_id
        )
        response = request.execute()
        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']

        channel_name = snippet.get('title',"Not Available")
        channel_name = clean(channel_name, no_emoji=True)
        channel_id = response['items'][0]['id']
        channel_published_at = snippet.get('publishedAt')
        channel_published_at = datetime.fromisoformat(channel_published_at)
        channel_published_at = channel_published_at.strftime("%Y-%m-%d %H:%M:%S")
        subscription_count = statistics.get('subscriberCount', "Not Available")
        channel_views = statistics.get('viewCount', "Not Available")
        channel_description = snippet.get('description', "Not Available")
        channel_description = clean(channel_description, no_emoji=True)
        video_count = statistics.get('videoCount', "Not Available")
        playlist_ids = playlist.playlist_request(channel_id, youtube)

        channel_details = {"channel_id":channel_id,
                        "channel_name":channel_name,
                        "channel_published_at": channel_published_at,
                        "subscription_count": subscription_count,
                        "channel_views":channel_views,
                        "channel_description" : channel_description,
                        "video_count": video_count,
                        "playlist_ids": playlist_ids
                        }
        return channel_details
    except HTTPError as e:
        return f"{e.status_code}, {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e


