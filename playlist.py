from googleapiclient.errors import HttpError
import playListItems
from cleantext import clean

def playlist_request(channel_id, youtube):
    '''Gets channel ID as input and return playlist details list.'''
    try:
        #Sending request
        request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        )

        #Fetching details from response
        response = request.execute()
        items = response.get('items')
        playlist_details = []
        video_id_tracker = []
        for item in range(len(items)):
            playlist_dict={}
            playlist_dict["playlist_id"] = items[item].get("id", "Not Available")
            snippet = items[item].get('snippet', "Not Available")
            playlist_dict["playlist_name"] = snippet.get("title", "Not Available")
            playlist_dict["playlist_name"] = clean(playlist_dict["playlist_name"], no_emoji=True)

            #Calling playlistItems_request function to retrieve video and comment details of the channel.
            video_ids = playListItems.playlistItems_request(items[item].get("id"), youtube, video_id_tracker)
            playlist_dict["video_ids"] = video_ids
            playlist_details.append(playlist_dict)
        return(playlist_details)
    
    except HttpError as e:
        return f"{e.status_code} - {e.reason}"
    except KeyError as e:
        return f"{e} Not Found"
    except Exception as e:
        return e



