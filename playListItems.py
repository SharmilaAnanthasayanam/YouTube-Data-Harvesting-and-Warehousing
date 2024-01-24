from googleapiclient.errors import HttpError
import video


def playlistItems_request(playlist_id, youtube, video_id_tracker):
    '''Gets playlist_id, youtube api object, video id tracker
    Returns Playlist Item list.'''
    try:
        #Sending Request
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlist_id
        )

        ##Fetching details from response
        response = request.execute()
        items = response.get("items")
        playlist_Items = []
        for item in range(len(items)):
            content_details = items[item].get("contentDetails", "Not Available")
            video_id = content_details.get("videoId", "Not Available")
            if video_id not in video_id_tracker:
                video_id_tracker.append(video_id)
                #Calling video_function function to retrieve video and comment details of the channel.
                video_details = video.video_request(video_id, youtube)
                if video_details:
                    playlist_Items.append(video_details)
        return playlist_Items
        
    except HttpError as e:
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e
    