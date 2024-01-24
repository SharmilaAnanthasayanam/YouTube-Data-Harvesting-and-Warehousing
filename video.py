from googleapiclient.errors import HttpError
import isodate
from cleantext import clean
import comments
from datetime import datetime
import pprint

def video_request(video_id, youtube):
    '''Gets video ID and Youtube api object
    Returns video details dictionary.'''
    try:
        request = youtube.videos().list(
        part ="snippet,contentDetails,statistics",
        id = video_id
        )

        #Fetching details from response
        response = request.execute()
        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']
        content_details = response['items'][0]['contentDetails']
        
        video_name = snippet.get('title',"Not Available")
        video_name = clean(video_name, no_emoji=True)
        video_description  = snippet.get('description', "Not Available")
        video_description = clean(video_description, no_emoji=True)
        tags = snippet.get('tags', "Not Available")
        tags = clean(tags, no_emoji=True)
        video_published_at = snippet.get('publishedAt')
        video_published_at = datetime.fromisoformat(video_published_at)
        video_published_at = video_published_at.strftime("%Y-%m-%d %H:%M:%S")
        view_count = statistics.get('viewCount',0)
        dislike_count = statistics.get('dislikeCount',0)
        like_count = statistics.get('likeCount',0)
        fav_count = statistics.get('favoriteCount',0)
        comment_count = statistics.get('commentCount',0)
        duration = content_details.get('duration')
        parsed_duration = str(isodate.parse_duration(duration))
        raw_thumbnail = snippet.get('thumbnails', "Not Available")
        if raw_thumbnail != "Not Available":
            raw_thumbnail = snippet.get('thumbnails', "Not Available")
        standard = "Not Available"
        if raw_thumbnail != "Not Available":
            standard = raw_thumbnail.get('standard',"Not Available")
        thumbnail = "Not Available"
        if standard != "Not Available":
            thumbnail = standard.get('url', "Not Available")
        caption_status = content_details.get('caption')

        #Calling comments_request function to retrieve comment details of the channel.
        comments_details = comments.comments_request(video_id, youtube)

        video_details = {"video_id": video_id,
                         "video_name": video_name,
                         "video_description": video_description,
                         "tags": tags,
                         "video_published_at": video_published_at,
                         "view_count":view_count,
                         "like_count": like_count,
                         "dislike_count": dislike_count,
                         "fav_count": fav_count,
                         "comment_count": comment_count,
                         "duration": parsed_duration,
                         "thumbnail": thumbnail,
                         "caption_status": caption_status,
                         "comments": comments_details
                         }
        return video_details

    except HttpError as e:
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except IndexError as e:
        return None
    except Exception as e:
        return e