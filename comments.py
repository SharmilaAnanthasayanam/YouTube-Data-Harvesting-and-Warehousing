from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime
from cleantext import clean


def comments_request(video_id, youtube):
    '''Gets video ID and youtube api object
    Returns comments details list'''
    try:
        #Sending request
        request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId = video_id
        )

        #Fetching details from response
        response = request.execute()
        items = response.get("items", "Not Available")
        comments = []
        for item in items:
            comments_dict = {}
            comment_id = item.get("id", "Not Available")
            raw_snippet = item.get("snippet", "Not Available")
            toplevelcomment = "Not Available"
            if raw_snippet != "Not Available":
                toplevelcomment = raw_snippet.get("topLevelComment", "Not Available")
            if toplevelcomment != "Not Available":
                snippet = toplevelcomment.get("snippet", "Not Available")
            if comment_id != "Not Available"  or snippet != "Not Available":
                comment_text = snippet.get("textDisplay", "Not Available")
                comment_text = clean(comment_text, no_emoji=True)
                comment_author = snippet.get("authorDisplayName", "Not Available")
                comment_published = snippet.get("publishedAt")
                comments_dict["comment_id"] = comment_id 
                comments_dict["comment_text"] = comment_text
                comments_dict["comment_author"] = comment_author
                comments_dict["published_at"] = comment_published
                comments_dict["published_at"] = datetime.fromisoformat(comments_dict["published_at"])
                comments_dict["published_at"] = comments_dict["published_at"].strftime("%Y-%m-%d %H:%M:%S")
                comments.append(comments_dict)
        return comments

    except HttpError as e:
        reason_permission = "One or more of the requested comment threads cannot be retrieved due to insufficient permissions. The request might not be properly authorized."
        reason_disabled = "The video identified by the <code><a href=\"/youtube/v3/docs/commentThreads/list#videoId\">videoId</a></code> parameter has disabled comments."
        if e.reason == reason_permission or e.reason == reason_disabled:
            return []
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e




