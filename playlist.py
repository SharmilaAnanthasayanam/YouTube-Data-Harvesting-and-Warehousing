from googleapiclient.errors import HttpError
import playListItems
from cleantext import clean

def playlist_request(channel_id, youtube):

    try:
        request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        )
        response = request.execute()
        items = response.get('items')
        playlist_details = []
        for item in range(len(items)):
            playlist_dict={}
            playlist_dict["playlist_id"] = items[item].get("id", "Not Available")
            snippet = items[item].get('snippet', "Not Available")
            playlist_dict["playlist_name"] = snippet.get("title", "Not Available")
            playlist_dict["playlist_name"] = clean(playlist_dict["playlist_name"], no_emoji=True)
            video_ids = playListItems.playlistItems_request(items[item].get("id"), youtube)
            playlist_dict["video_ids"] = video_ids
            playlist_details.append(playlist_dict)
        return(playlist_details)
    except HttpError as e:
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e



