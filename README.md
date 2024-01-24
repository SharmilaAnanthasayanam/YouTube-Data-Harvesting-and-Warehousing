# Youtube_Project
YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit

### GOAL:
To create a Streamlit application that allows users to access and analyze data from multiple YouTube channels.

### Tools Used: 
Streamlit, Mongodb Compass, SQL

### Architecture 
![Youtube Project Architecture](https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/6a289104-1e9e-48b9-97ce-0bdb8db04ff9)

#### Page 1: Scrap

Enter a channel ID and click enter.
<img width="914" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/b031cd16-2743-4bf4-8e00-8f66359a7ace">

You can find the channel details below.
<img width="925" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/b585c6e3-682d-4c2f-91ad-5132ac8f9e01">


#### Page 2: Move

Click on Move data to MongoDB button first.

<img width="917" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/5dbdcda9-60ae-4a96-bfd4-097d2f014811">

Then, Cick on Move data to SQL button

<img width="922" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/c39b9186-9e1e-402a-9c0a-2e65744254e1">


#### Page 3: Query

As shown above the following channels which are the top youtube channels for Data Science have been inserted in the database.
* Sentdex
* freecodecamp
* corey shafer
* Joma Tech
* Two minute papers
* StatQuest with Josh Starmer
* Siraj Raval
* Code Basics
* Analytics Vidhya
* Data Science Dojo
* The Coding train
* 3Blue1Brown

Now let's Query the database using the queries listed in the dropdown.

<img width="922" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/afb9d5b8-e1dc-4169-8c28-7c323e86f119">

Selecting - What are the top 10 most viewed videos and their respective channels?

<img width="919" alt="image" src="https://github.com/SharmilaAnanthasayanam/Youtube_Project/assets/112562560/fd30d077-272a-4206-ae08-10e71b0b6a13">

We could see that "Joma Tech" comes first followed by "freecodecamp", "Two minute papers" and "3Blue1Brown".

### Challenges faced and solution applied
* Index Error:
    * Cause: Thrown due to Hidden videos in the playlist
    * Solution: Catched the error and skipped these videos.
* Duplicate Entry Error: Thrown when inserting data to SQL
    * Cause: Same video published in the same playlist and different playlist multiple times
    * Solution: Maintained a video ID tracker list to skip if any video id is duplicated.
* httpError
    * Cause: Channel owner disabled comments.
    * Solution: Catched the error and returned an empty list.
  
### Limitations: 
* Maximum number of Playlists retrieved from api is 5.
* Maximum number of videos retrieved from api is 50.
* Maximum number of comments retrieved from api is 20.













  









