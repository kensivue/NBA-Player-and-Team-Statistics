#!/usr/bin/env python
# coding: utf-8

# # Final Project - NBA Player and Team Statistics

# ## Importing the necessary modules

# In[1]:


import requests
import pprint as pprint
import seaborn as sb
import pandas as pd
import csv
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# ## !! These are hyperlinks to the sources needed to run the project !!
# The first source (API) I used which was: [balldontlie-api-link](https://www.balldontlie.io/#introduction) -- 
# The next source is a player CSV file: [player-csv](https://raw.githubusercontent.com/peasant98/TheNBACSV/master/nbaNew.csv) -- 
# The last source is a team CSV file: [team-csv](https://www.kaggle.com/ionaskel/nba-games-stats-from-2014-to-2018)

# In[2]:


playerSingleStat = requests.get("https://www.balldontlie.io/api/v1/stats/?seasons[]=2015").json()
#playerSingleStat
playerIntricateStat = pd.DataFrame(playerSingleStat["data"])
playerIntricateStat


# In[3]:


playerStats = pd.read_csv("https://raw.githubusercontent.com/peasant98/TheNBACSV/master/nbaNew.csv")
playerStats.head()


# In[4]:


playerStats.columns


# In[5]:


teamStats = pd.read_csv("nba.games.stats.csv")
teamStats.columns


# In[6]:


teamStats


# ## Highest Scoring Player
# ### I will be using the player csv module to find these statistics

# In[7]:


# Let's find a player who has scored the most points
mostPoints = playerStats[["PlayerName","PTS"]].sort_values("PTS",ascending=False).head(25) # find the most points
mostPoints.drop_duplicates("PlayerName") # there are duplicate names so we must filter it out using .drop_duplicates
# The highest scoring player is Wilt Chamberlain


# In[8]:


# Let's see Wilt Chamberlain's highest scoring season
playerGrouping = playerStats.groupby("PlayerName") # groupby player name
playerGrouping.get_group("Wilt Chamberlain*")[["SeasonStart","PTS"]].sort_values("PTS",ascending=False) # get Wilt's seasons and points
# Wilt Chamberlain's highest scoring season was in 1962 with 4029 points


# In[9]:


# Visualizing the distribution of Wilt Chamberlain's point scoring career
sb.set_style("whitegrid") # put lines for reference
wiltQuery = playerStats.query("PlayerName == 'Wilt Chamberlain*'") # send a query for his statistics
wiltPoints = sb.catplot(x="SeasonStart",y="PTS",data=wiltQuery,hue="PlayerName",kind="bar",height=10,ci=None).set_xlabels("Season Year").set_ylabels("Points Scored") # create bar plot for his season and points
# Interestingly enough, his lowest points scored in a season was in 1970 which was possibly due to injury.


# In[10]:


# Finding the avg points per season for the top 10 players
avgPointsPerSeason = playerStats.groupby("PlayerName").agg({"PTS":np.mean}).sort_values("PTS",ascending=False).head(10).reset_index() # aggregate mean of points using numpy
avgPointsPerSeason # output the data
# Michael Jordan has the highest points per season over Wilt even though Wilt is the all time scorer. 


# ## Team Statistics

# In[11]:


# Let's filter the data to get specific years so we can be more accurate with our data
nbaYearDate = pd.to_datetime(teamStats["Date"],format="%Y-%m-%d") # Eventhough we have a date already, we only want the year for the data and not all of it. 
teamStats["Season Year"]=nbaYearDate.dt.year # Now we are taking the year itself to filter the seasons
teamStats


# In[12]:


# to make it easier, we can make a new dataframe only for the 2015 year
twentyFifteenSeasonDF = pd.DataFrame(teamStats) # set variable to new dataframe
twentyFifteenSeasonDF


# In[13]:


# Look at the record for each team specifically in the 2015 season
teamRecords = twentyFifteenSeasonDF.groupby("Team")["WINorLOSS"].value_counts(sort=True,ascending=False) # look at the win/loss record for each team
print(teamRecords)


# In[14]:


# Look at who has the most wins and the most losses
twentyFifteenSeasonDF.groupby("WINorLOSS")["Team"].value_counts(sort=True,ascending=False) # Sort the values to see the most wins and most losses of each team


# In[15]:


# We see that Golden State has the best record with 72 wins!! This is also the best record in history as well!! Let's dig deeper to see their statistics. 
teamGroup = twentyFifteenSeasonDF.groupby("Team") # create a new variable with a .groupby method
teamGroup.get_group("GSW") # we want Golden State


# In[16]:


# Let's take a look at the the game with the highest field goals made for GSW (Golden State Warriors)
teamGroup.get_group("GSW")[["Date","FieldGoals","FieldGoalsAttempted"]].sort_values("FieldGoals",ascending=False) # use get_group to get Golden State's statistics
# it looks like there were 52 field goals made out of 95 which is the highest


# In[17]:


# Let's actually look at shot percentage to see which game was the highest shots made per attempt.
fgp = twentyFifteenSeasonDF["FieldGoals"]/twentyFifteenSeasonDF["FieldGoalsAttempted"] # Set a new variable for field goal percentage
twentyFifteenSeasonDF["FGP"]= fgp # Create a new column for these percentages
teamGroup.get_group("GSW")[["Date","FGP"]].sort_values("FGP",ascending=False) # output with the day and FGP


# In[18]:


# Time to visualize the shooting percentages!
GSW = teamGroup.get_group("GSW") # set GSW for the group we want
sb.distplot(GSW["FGP"]).set_xlabel("Field Goal Percentage") # create a distribution plot to see the common shooting percentages
# We can see that in many of their games they shot about 45% or higher. That's amazing!


# ## Building off of the Team Statistics
# ### We will use the csv file to find the players that were on the 2015 roster.

# In[19]:


# First let's use the csv to find players that were on the 2015 Golden State Warriors roster.
seasonGroupingTwentyFifteen = playerStats[playerStats["SeasonStart"] == 2015.0]
seasonGroupingTwentyFifteen.columns


# In[20]:


# Let's try to sort this a little more so we can get the GSW Players from the team name as well as their point scorers individually in the year
GSWPlayers = seasonGroupingTwentyFifteen[["PlayerName","Tm","PTS","SeasonStart"]].sort_values("PTS",ascending=False).loc[seasonGroupingTwentyFifteen["Tm"]=="GSW"]
GSWPlayers
# It looks like Stephen Curry, Klay Thompson, and Draymond were top three scorers for the year


# In[21]:


# Seeing as though Stephen Curry has an outstanding amount of points let's try to find him and his id using the API this time
stephName = "Curry"
stephQuery = requests.get("https://www.balldontlie.io/api/v1/players/?search="+stephName).json()
stephQuery
# We found him! His id is 115


# In[22]:


# Now that we know his id lets find him in the 2015 season using his id
stephID = "115" # set his id to a string value
stephStatsQuery = requests.get("https://www.balldontlie.io/api/v1/stats/?seasons[]=2015&player_ids[]="+stephID).json() # send a request to get his statistics from the API
stephStats= pd.DataFrame(stephStatsQuery["data"]) # create a Data Frame for his statistics
stephStats.columns # look at the columns to identify what we want to see.


# In[23]:


stephGameAndPoints = stephStats[["game","pts"]].sort_values("pts",ascending=False).dropna() # output which game he scored the highest in the season and use dropna to let go of any NaN values
stephGameAndPoints
# Wow! Stephen Curry scored 53 points in one game. 

