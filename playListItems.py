from googleapiclient.errors import HttpError
import video


def playlistItems_request(playlist_id, youtube):
    try:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=1000,
            playlistId=playlist_id
        )
        response = request.execute()
        items = response.get("items")
        playlist_Items = []
        for item in range(len(items)):
            content_details = items[item].get("contentDetails", "Not Available")
            video_id = content_details.get("videoId", "Not Available")
            video_details = video.video_request(video_id, youtube)
            playlist_Items.append(video_details)
        return playlist_Items
        
    except HttpError as e:
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e
    