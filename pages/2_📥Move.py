'''This module provides option to move the channel details fetched from Scrap section to Mongodb and SQL Databases.'''
import streamlit as st
from pymongo import MongoClient
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

try:
    #Page Configuration
    st.set_page_config(
        page_title= "Move"
    )
    #Getting the channel details from session state
    channel_details = st.session_state["data"]
    channel_id = st.session_state["channel_id"]

    if channel_id == "":
        st.write("Enter your channel id in Scrap Section")

    if channel_details != "Enter your channel id in Scrap section":
        st.write("click the below button to push your channel details to Mongodb")
        # Connect to MongoDB'
        con_string = os.getenv("connectionstring")
        client = MongoClient(con_string)  
        db = client["youtube_db"]
        collection = db["channel_collection"]
        if st.button("Move Data to MongoDB", key="move_data_mongodb", help="Store the retrieved channel details in MongoDB"):
            # Check if the document already exist in Mongodb
            existing_document = collection.find_one({"channel_id": channel_id})
            if channel_details:
                if existing_document == None: # If document does not exist in Mongodb
                    collection.insert_one(channel_details) #Insert channel details into MongoDB
                    st.success("Channel details successfully moved to MongoDB!",icon="✅")
                else: # If document already exist in Mongodb
                    collection.replace_one(existing_document, channel_details) #Replace the document with new document
                    st.success("Updated the Channel details successfully",icon="✅")
            else:
                st.error("No channel details to move.",icon="🚨")

        #Moving data to SQL
        password= os.getenv("password") #Connecting to SQL
        mydb = mysql.connector.connect( 
            host="localhost",
            user="root",
            password = password,
            database="youtube"
        )
        mycursor = mydb.cursor()
        mydb.start_transaction()
        st.write("click the below button to push your channel details to SQL")
        if st.button("Move Data to SQL", key="move_data_sql", help="Store the retrieved channel details in SQL"):
            #Fetching count of the current channel document
            Number_of_docs = collection.count_documents({"channel_id": channel_id}) 

            #Checking if the channel already exist in SQL db
            mycursor.execute("SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id = %s)", (channel_id,))
            result = mycursor.fetchone()[0]

            if Number_of_docs == 0:
                st.write("Document not found in Mongodb")
            elif result:
                st.warning("Channel already exists in SQL database",icon="⚠️")
            else:
                #Getting channel info from mongodb
                channel_document = collection.find_one({"channel_id": channel_id})
                channel_name = channel_document.get("channel_name",'')
                channel_published_at = channel_document.get("channel_published_at", '')
                channel_views = channel_document.get("channel_views",0)
                channel_description = channel_document.get("channel_description",'')
                subscription_count = channel_document.get("subscription_count",0)
                video_count = channel_document.get("video_count", 0)

                #Inserting the fetched channel data to channel table in SQL
                INSERT_QUERY = """INSERT INTO Channel (channel_id, channel_name, channel_published_at, channel_views, subscription_count, channel_description, video_count)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);"""
                mycursor.execute(INSERT_QUERY, (
                    channel_id,
                    channel_name,
                    channel_published_at, 
                    channel_views,
                    subscription_count,
                    channel_description,
                    video_count
                ))

                #Getting the playlist Ids of the channel
                playlistids = channel_document.get("playlist_ids")

                #Looping through the playlists for fetching data
                for playlist in playlistids:
                    playlist_id = playlist.get("playlist_id",'')
                    playlist_name = playlist.get("playlist_name",'')

                    #Inserting the fetched playlist data to playlist Table in SQL
                    INSERT_QUERY = """INSERT INTO Playlist(playlist_id, channel_id, playlist_name)Values(%s, %s, %s);"""
                    mycursor.execute(INSERT_QUERY, (
                        playlist_id,
                        channel_id,
                        playlist_name
                    ))

                    #Getting the video data of the playlist
                    video_ids = playlist.get("video_ids")
                    #Looping through the videos for fetching data
                    for video in video_ids:
                        video_id = video.get("video_id",'')
                        video_name = video.get("video_name",'')
                        video_description = video.get("video_description",'')
                        video_published_at = video.get("video_published_at",None)
                        view_count = video.get("view_count",0)
                        like_count = video.get("like_count",0)
                        dislike_count = video.get("dislike_count",0)
                        favorite_count = video.get("fav_count",0)
                        duration = video.get("duration",'')
                        thumbnail = video.get("thumbnail",'')
                        tags = video.get("tags",'')
                        caption_status = video.get("caption_status",'')

                        #Inserting the fetched video data to Video Table in SQL
                        INSERT_QUERY = """INSERT INTO video (video_id, playlist_id, video_name, video_description, video_published_at,
                                            view_count, like_count, favorite_count, duration,thumbnail,tags, caption_status, dislike_count) 
                                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                        mycursor.execute(INSERT_QUERY, (
                            video_id,
                            playlist_id,
                            video_name,
                            video_description,
                            video_published_at,
                            view_count,
                            like_count,
                            favorite_count,
                            duration,
                            thumbnail,
                            tags,
                            caption_status,
                            dislike_count
                            ))
                        
                        #Getting the comments data of the playlist
                        comments = video.get("comments")

                        #Looping through the comments for fetching data
                        for comment in comments:
                            comment_id = comment.get("comment_id",'')
                            comment_text = comment.get("comment_text",'')
                            comment_author = comment.get("comment_author",'')
                            comment_published = comment.get("published_at",None)

                            #Inserting the fetched comments data to comments Table in SQL
                            INSERT_QUERY = """INSERT INTO comments (comment_id, video_id, comment_text, comment_author,comment_published_date) 
                                            VALUES(%s,%s,%s,%s,%s);"""
                            mycursor.execute(INSERT_QUERY, (
                                comment_id,
                                video_id,
                                comment_text,
                                comment_author,
                                comment_published
                            ))
                #Commiting the changes in db        
                mydb.commit()
                st.success("Channel details successfully moved to SQL!",icon="✅") 

except Exception as e:
    st.error(e)
    print(e)