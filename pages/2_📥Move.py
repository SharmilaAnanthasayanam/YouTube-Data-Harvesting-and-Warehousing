import streamlit as st
from pymongo import MongoClient
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

try:
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
        client = MongoClient(con_string)  # Replace with your connection string
        db = client["youtube_db"]
        collection = db["channel_collection"]
        if st.button("Move Data to MongoDB", key="move_data_mongodb", help="Store the retrieved channel details in MongoDB"):
            # Insert channel details into MongoDB
            st.write("Button clicked")
            existing_document = collection.find_one({"channel_id": channel_id})
            
            if channel_details:
                if existing_document == None:
                    # Ensure channel details are available before insertion
                    st.write("Before insert")
                    print(channel_details)
                    collection.insert_one(channel_details)
                    st.success("Channel details successfully moved to MongoDB!",icon="✅")
                else:
                    st.error("Channel ID already exists in the database. Document not inserted.")
            else:
                st.error("No channel details to move.",icon="🚨")

        #Moving data to SQL
        #Connecting to SQL
        password= os.getenv("password")
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password = password,
            database="youtube"
        )
        mycursor = mydb.cursor()
        st.write("click the below button to push your channel details to SQL")
        if st.button("Move Data to SQL", key="move_data_sql", help="Store the retrieved channel details in SQL"):
            Number_of_docs = collection.count_documents({"channel_id": channel_id})
            if Number_of_docs == 0:
                st.write("Document not found in Mongodb")
            else:
                #Getting channel info from mongodb
                
                channel_document = collection.find_one({"channel_id": channel_id})
                channel_name = channel_document.get("channel_name",'')
                channel_published_at = channel_document.get("channel_published_at", '')
                channel_views = channel_document.get("channel_views",0)
                channel_description = channel_document.get("channel_description",'')
                subscription_count = channel_document.get("subscription_count",0)
                video_count = channel_document.get("video_count", 0)

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
                mydb.commit()
                st.write("channel table success")
                playlistids = channel_document.get("playlist_ids")
                # print(len(playlistids))
                for playlist in playlistids:
                    playlist_id = playlist.get("playlist_id",'')
                    playlist_name = playlist.get("playlist_name",'')
                    INSERT_QUERY = """INSERT INTO Playlist(playlist_id, channel_id, playlist_name)Values(%s, %s, %s);"""
                    mycursor.execute(INSERT_QUERY, (
                        playlist_id,
                        channel_id,
                        playlist_name
                    ))
                    mydb.commit()
                    st.write("playlist table success")
                    video_ids = playlist.get("video_ids")
                    # print(len(video_ids))
                    for video in video_ids:
                        video_id = video.get("video_id",'')
                        video_name = video.get("video_name",'')
                        video_description = video.get("video_description",'')
                        video_published_at = video.get("video_published_at",'')
                        view_count = video.get("view_count",0)
                        like_count = video.get("like_count",0)
                        favorite_count = video.get("fav_count",0)
                        duration = video.get("duration",'')
                        thumbnail = video.get("thumbnail",'')
                        tags = video.get("tags",'')
                        caption_status = video.get("caption_status",'')
                        INSERT_QUERY = """INSERT INTO video (video_id, playlist_id, video_name, video_description, video_published_at,
                                            view_count, like_count, favorite_count, duration,thumbnail,tags, caption_status) 
                                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
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
                            caption_status
                            ))
                        mydb.commit()
                        st.write("Video table success")
                        comments = video.get("comments")
                        # print(comments)
                        for comment in comments:
                            comment_id = comment.get("comment_id",'')
                            # video_id = comment.get("video_id",'')
                            comment_text = comment.get("comment_text",'')
                            comment_author = comment.get("comment_author",'')
                            comment_published = comment.get("published_at",'')
                            INSERT_QUERY = """INSERT INTO comments (comment_id, video_id, comment_text, comment_author,comment_published_date) 
                                            VALUES(%s,%s,%s,%s,%s);"""
                            mycursor.execute(INSERT_QUERY, (
                                comment_id,
                                video_id,
                                comment_text,
                                comment_author,
                                comment_published
                            ))
                            mydb.commit()
                            print("comments table success")
            st.success("Channel details successfully moved to SQL!",icon="✅")

            
except Exception as e:
    st.error(e)
    print(e)