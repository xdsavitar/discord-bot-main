import discord
import requests
from discord.ext import commands
import random
import os
import time
import threading
import json
from discord.ext.commands import has_permissions, CheckFailure
import requests
import datetime
import youtube_dl
import mysql.connector
import urllib.request
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from discord import FFmpegPCMAudio
from discord.utils import get
import socket
from datetime import date
uptime = 0
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
loopState = False
client = commands.Bot(command_prefix="-",intents=intents)
memes_count = 0
shitpost_count = 0
floppa_count = 0
open_shop_id = ""
random_line = ""
coin_value = 0
user_coins = 0
sent_message = ""
reaction_shop_id = ""
temp_ticket_id = ""
cat_bot_updates = client.get_channel(636399538650742795)
music_que = []
#await client.process_commands(message)																																	   #		
############################################################################################################################################################################

start = time.time()


try:
	os.makedirs("user_perks")
except:
	pass

try:
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database = "mydatabase"
		)
	cursor = mydb.cursor()

	print("Connection Established To Database")

except:
	print("Database Connection Not Established")





@client.event
async def on_member_join(member):
	member_name = str(member)
	member_id = int(member.id)
	server_id = member.guild.id

	print(member_id)


	search_string = "SELECT * FROM discordusersnew WHERE userID = %s"
	main_search_string = (f"{member_id}",)
	cursor.execute(search_string,main_search_string)
	result = cursor.fetchone()

	if str(result) == "None":
		print(f"{member_name} Is not found in the database")
		member_coin = 0

		sql_string = "INSERT INTO discordusersnew (name,userID,cat_coin,server_id) VALUES(%s,%s,%s,%s)"
		values = (member_name,member_id,member_coin,server_id)
		cursor.execute(sql_string,values)
		mydb.commit()



		print("New User Added To Database")

	if str(result) != "None":
		print("Already Existing User in database Joined The Server!")










@client.command()
async def createwallet(ctx):
	path = "C:/Users/xdSavitar/Desktop/Discord Bot/user_perks"
	search_string = "SELECT * FROM discordusersnew WHERE userID = %s"
	main_search_string = (f"{ctx.message.author.id}",)
	cursor.execute(search_string,main_search_string)
	result = cursor.fetchone()

	member_name = str(ctx.message.author)
	member_id = int(ctx.message.author.id)
	member_coin = 0
	server_id = int(ctx.guild.id)

	if str(result) == "None":
		sql_string = "INSERT INTO discordusersnew (name,userID,cat_coin,server_id) VALUES(%s,%s,%s,%s)"
		values = (member_name,member_id,member_coin,server_id)
		cursor.execute(sql_string,values)
		mydb.commit()
		print("Added New User To DB")

		os.makedirs(f"{path}/{ctx.message.author.id}")

		await ctx.send(f"<@{member_id}> Your wallet has been created")

	elif str(result) != None:
		await ctx.send(f"<@{member_id}> You already have a wallet!")


@client.command()
async def vtime(ctx):
	with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/users/voice_time/{ctx.message.author.id}.txt","r") as read:
		time = read.read()


	embed = discord.Embed(

		title = f"{ctx.message.author}",
		description = "Voice Tracker Stats",
		colour = discord.Colour.blue()

		)
	embed.set_image(url=f"{ctx.message.author.avatar_url}")
	embed.add_field(name="Time spent in voice",value =f"{str(time)}",inline=False)
	await ctx.send(embed=embed)


@has_permissions(administrator=True)
@client.command()
async def perm(ctx,message):
	dirc = "C:/Users/xdSavitar/Desktop/Discord Bot/server_settings"
	split = message.split("$")
	print(split[1])

	if str(split[1]) == "enableVT":
		try:
			os.mkdir(f"{dirc}/{ctx.guild.id}")
			with open(f"{dirc}/{ctx.guild.id}/voiceTrack.txt","w") as write:
				write.write("enabled")
				write.close()
		except:
			with open(f"{dirc}/{ctx.guild.id}/voiceTrack.txt","w") as write:
				write.write("enabled")
				write.close()

	if str(split[1]) == "disableVT":
		try:
			with open(f"{dirc}/{ctx.guild.id}/voiceTrack.txt","w") as write:
				write.write("disabled")
				write.close()
		except:
			print("Rbuh")


@client.event
async def on_voice_state_update(member, before, after):
	
	with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/server_settings/{member.guild.id}/voiceTrack.txt","r") as read:
		state = read.readlines()
		print(state[0])

	
	if str(state[0]) == "enabled":
		tempPath = "C:/Users/xdSavitar/Desktop/Discord Bot/temp"
		voiceTime = "C:/Users/xdSavitar/Desktop/Discord Bot/users/voice_time"
		print(member.id,before.channel,after.channel)
		strong = ""

		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")

		print(current_time)
		print(before.channel,after.channel)

		if (before.channel == None):
			print(f"User Joined The Channel {after.channel}")
			with open(f"{tempPath}/{member.id}.txt","w") as File:
				File.writelines(f"{current_time}")
				File.close()


		elif (before.channel != None):
			print("usr has left the channel")

			if os.path.isfile(f"{tempPath}/{member.id}.txt") == True:

				with open(f"{tempPath}/{member.id}.txt") as Read:
					r = Read.readlines()
					for_split = [r[0]]

					for char in for_split:
						strong += char

					start = str(strong)
					end = str(now.strftime("%H:%M:%S"))

					start_dt = datetime.datetime.strptime(start, '%H:%M:%S')
					end_dt = datetime.datetime.strptime(end, '%H:%M:%S')
					diff = (end_dt - start_dt)

					print(diff)

					
					if os.path.isfile(f"{voiceTime}/{member.id}.txt") == False:
						with open(f"{voiceTime}/{member.id}.txt","w") as write:
							write.write(str(diff))

					
					else:
						with open(f"{voiceTime}/{member.id}.txt","r") as wX:
							time_current = wX.readlines()
							string = ""
							for char in time_current:
								string += char


							t1 = datetime.datetime.strptime(string, '%H:%M:%S')
							t2 = datetime.datetime.strptime(str(diff), '%H:%M:%S')
							time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
							result = (t1 - time_zero + t2).time()

							with open(f"{voiceTime}/{member.id}.txt","w") as write:
								write.write(str(result))
								write.close()



				os.remove(f"{tempPath}/{member.id}.txt")

	else:
		pass


@client.command()
async def mywallet(ctx):
	sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
	member_id_Pass = (f"{ctx.message.author.id}",)
	cursor.execute(sql_string,member_id_Pass)
	user = client.get_user(ctx.message.author.id)

	result = cursor.fetchall()
	try:

		coin_count = result[0][2]
		await ctx.send(f"<@{ctx.message.author.id}> You Currently Have {coin_count} Coin(s)!")

	except:
		await ctx.send(f"<@{ctx.message.author.id}> You Currently Dont Have A Wallet. Create One Using -createwallet")

@client.command()
async def xpay(ctx,*,message):
	new_message = message.split("-")
	member_idx = new_message[0]
	coin_ammount = new_message[1]

	stripped_id = (new_message[0])

	stID = stripped_id.strip("><@&!")
	new_id = stID.replace(">"," ")

	print(new_id)

	sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
	member_id_Pass = (f"{ctx.message.author.id}",)
	cursor.execute(sql_string,member_id_Pass)
 
	result = cursor.fetchall()

	if str(result) == "None":
		await ctx.send(f"<@{ctx.message.author.id}> You Are Not In The Database Type -addmedb to get added to the database!")

	elif str(result) != "None":
		sender_coins = result[0][2]

		sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
		member_id_Pass = (f"{message}",)
		cursor.execute(sql_string,member_id_Pass)
		result = cursor.fetchall()

		if str(result) != "None":
			print("Found")
			if int(sender_coins) >= int(coin_ammount):
				print("SENT",new_id)

				sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
				values = (f"{int(new_id)}",)
				cursor.execute(sql_string,values)
				result = cursor.fetchall()
				reciever_coins = result[0][2]


				sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
				values = (int(reciever_coins) + int(coin_ammount),int(new_id))
				cursor.execute(sql_string,values)
				mydb.commit()


				sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
				values = (int(sender_coins) - int(coin_ammount)),int(ctx.message.author.id)
				cursor.execute(sql_string,values)
				mydb.commit()
				await ctx.send(f"<@{ctx.message.author.id}> Has Successfully Sent {coin_ammount} To <@{int(new_id)}>")
				with open("transaction_logs.txt","a") as Write:
					Write.write(f"[{current_time}]: Transaction^ [Successfull] [{ctx.message.author.id}] ----------> [{int(new_id)}], \n")

			else:
				await ctx.send(f"<@{ctx.message.author.id}> Not Enought Coins To Send!")
				with open("transaction_logs.txt","a") as Write:
					Write.write(f"[{current_time}]: Transaction^ [Failed] [{ctx.message.author.id}] ----------> [{int(new_id)}] \n")



#embed = discord.Embed(

		#title = "Shop",
		#description = "Cat-Bot Shop",
		#colour = discord.Colour.blue()

		#)
	#embed.set_image(url="https://media.istockphoto.com/vectors/vintage-small-shop-pixel-art-style-vector-icon-on-white-background-vector-id1040011824?k=6&m=1040011824&s=170667a&w=0&h=-pWRfZrBT0P1kSKsazducrJ9MLioD7IgyZ8lXb2JLTo=")
	#embed.add_field(name = "Shitpost Coin Boost 3x",value="350 Coins",inline=False)
	#embed.add_field(name="Memes Coin Boost 2x",value ="150 Coins",inline=False)
	#sent_message = await ctx.send(embed=embed)
	#print(ctx.message.author)

	#reaction_shop_id += str(sent_message.id)

	#await sent_message.add_reaction("<:buyboost:810658342124912650>")
	#await sent_message.add_reaction("<:buyboost_shitposts:810686700136431617>")


def main_threading_loop(memberid):
	with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/users/voice_time/{memberid}.txt","w") as File:
		print(memberid)


		
@client.command()
async def loop(ctx,message):
	global loopState

	if str(message) == "enable":
		loopState = True
		print("Loop Enabled")
		await ctx.send("[PLAYER]: Loop Enabled")
	elif str(message) == "disable":
		loopState = False
		print("Loop Disabled")
		await ctx.send("[PLAYER]: Loop Disabled")



@client.command()
async def playersettings(ctx):
	textstate = ""
	if loopState == 1:
		textstate += "Enabled"

	elif loopState == 0:
		textstate += "Disabled"

	embed = discord.Embed(
		title = "Music Player",
		description = "Player 0.1",
		colour = discord.Colour.blue()

		)

	#embed.set_image(url="##")
	embed.add_field(name=f"Player Version",value=f"0.1",inline=False)
	embed.add_field(name=f"Loop State",value=f"{textstate}",inline=False)
	embed.add_field(name=f"Key",value=f"FFmpegExtractAudio",inline=False)
	embed.add_field(name=f"Preferredcodec",value=f"wav",inline=False)
	embed.add_field(name=f"Preferredquality",value=f"320 Highest",inline=False)
	await ctx.send(embed=embed)





@client.command()
async def playerque(ctx):
	global music_que

	if not music_que:
		await ctx.send("Nothing Found In The Que List")

	elif music_que:
		await ctx.send(f"Found {len(music_que)} Song(s) In Que")



@client.command()
async def playercommands(ctx):
	embed = discord.Embed(
		title = "Music Player",
		description = "Player 0.1",
		colour = discord.Colour.blue()
		)

	#embed.set_image(url="##")
	embed.add_field(name=f"play",value=f"Plays the music from youtube and soundcloud?? maybe",inline=False)
	embed.add_field(name=f"Loop -enable * -disable",value="Enables or Disables Loop",inline=False)
	embed.add_field(name=f"pause",value="what u expect it to do",inline=False)
	embed.add_field(name=f"stop",value=f"stops the current audio",inline=False)
	embed.add_field(name=f"resume",value=f"well resumes the song?",inline=False)
	embed.add_field(name=f"clearque",value=f"clears the current que for the songs * if there is one",inline=False)
	await ctx.send(embed=embed)





@client.command()
async def geolocate(ctx,*,ip_addr):
	req = requests.get(f"http://ip-api.com/json/{ip_addr}")
	json = req.json()


	Status = json["status"]
	Country = json["country"]
	regionName = json["regionName"]
	isp = json["isp"]
	timeZone = json["timezone"]
	zip_code = json["zip"]
	lattitude = json["lat"]
	longtitude = json["lon"]



	print(Status,Country,regionName,isp,timeZone,zip_code,lattitude,longtitude)

	embed = discord.Embed(
		title = "Geo Locator",
		description = "Geo Locate Status",
		colour = discord.Colour.blue()
	)

	try:

		embed.add_field(name=f"Status",value=f"{Status}",inline=False)
		embed.add_field(name=f"Country",value=f"{Country}",inline=False)
		embed.add_field(name=f"Region",value=f"{regionName}",inline=False)
		embed.add_field(name=f"ISP",value=f"{isp}",inline=False)
		embed.add_field(name=f"Time Zone",value=f"{timeZone}",inline=False)
		embed.add_field(name=f"Zip Code",value=f"{zip_code}",inline=False)
		embed.add_field(name=f"Lattitude",value=f"{lattitude}",inline=False)
		embed.add_field(name=f"Longtitude",value=f"{longtitude}",inline=False)

	except:
		pass



	await ctx.send(embed=embed)









@client.command()
async def skip(ctx):
	global music_que
	if not music_que:
		await ctx.send("Noting In Que!")

	if music_que:
		
		await ctx.send("Skipped Song!")
		voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

		if voice.is_connected():
			voice.stop()
			next_url = music_que[0]

			os.remove("song.wav")
			ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'wav',
					'preferredquality': '1411',
				}],
			}
			url = str(music_que[0])
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
			for file in os.listdir("./"):
				if file.endswith(".wav"):
					os.rename(file, "song.wav")




			voice.play(discord.FFmpegPCMAudio("song.wav"),after=lambda e: music_loop(voice))
			music_que.pop(0)
		else:
			await ctx.send("Bot Is Not In Voice Channel")



def takeBalance():
	pass






@client.command()
async def pfp(ctx,member :discord.User):
	author = member
	pfp = author.avatar_url

	await ctx.send(pfp)




@client.command()
async def openshop(ctx):
	global open_shop_id

	channel = client.get_channel(811219034615447562)
	embed = discord.Embed(
	title = "Shop",
	description = "Cat-Bot Shop",
	colour = discord.Colour.blue()

	)

	embed.set_image(url="https://media.istockphoto.com/vectors/vintage-small-shop-pixel-art-style-vector-icon-on-white-background-vector-id1040011824?k=6&m=1040011824&s=170667a&w=0&h=-pWRfZrBT0P1kSKsazducrJ9MLioD7IgyZ8lXb2JLTo=")
	embed.add_field(name = "cattolvl1",value="500",inline=False)
	embed.add_field(name = "cattolvl2",value="1000",inline=False)
	embed.add_field(name = "cattolvl3",value="3000",inline=False)
	embed.add_field(name = "cattolvl4",value="6000",inline=False)
	embed.add_field(name = "cattolvl5",value="11000",inline=False)

	#embed.add_field(name="Memes Coin Boost 2x",value ="150 Coins",inline=False)

	sent_message = await channel.send(embed=embed)
	await sent_message.add_reaction("<:catcoin:811203398367313920>")

	print(sent_message.id)

	open_shop_id += str(sent_message.id)



@client.command()
async def luckycard(ctx,message):
	role = discord.utils.get(ctx.message.guild.roles, name = "cattolvl1")
	global temp_ticket_id
	current_time = datetime.datetime.now()
	ticks = 0
	card_type = str(message)
	##path = "C:/Users/xdSavitar/Desktop/Discord Bot/users/user_cattolvl1_ticket_count"


	if role in ctx.message.author.roles:

		if card_type == "small":
			price = 10

			min_x = 0
			max_y = 20


		if card_type == "medium":
			price = 20

			min_x = 0
			max_y = 40

		if card_type == "large":
			price = 50

			min_x = 0
			max_y = 60



		sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
		values = (f"{int(ctx.message.author.id)}",)
		cursor.execute(sql_string,values)
		result = cursor.fetchall()
		coins_user = result[0][2]

		sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
		values = (int(coins_user) - int(price),int(ctx.message.author.id))
		cursor.execute(sql_string,values)
		mydb.commit()


		if int(coins_user) >= price:
			random_num = random.randint(min_x,max_y)

			reward = (random_num * 2)

			print(reward)


			sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
			values = (int(coins_user) + int(reward),int(ctx.message.author.id))
			cursor.execute(sql_string,values)
			mydb.commit()




			embed = discord.Embed(
				title = "Ticket",
				escription = "Lucky Catto Ticket",
				colour = discord.Colour.blue()

			)

			embed.set_image(url="https://i.imgur.com/DiUKLXV.png")

			embed.add_field(name=f"Ticket Size",value=f"Small",inline=False)
			#embed.add_field(name=f"Valid For",value=f"1 Hour",inline=False)
			embed.add_field(name=f"Total Winnings",value=f"{reward}",inline=False)
			sent_message = await ctx.send(embed=embed)

	else:
		await ctx.send(f"<@{ctx.message.author.id}> You Dont Have `cattolvl1` Role Please Buy One At The ``Shop``")

@client.command()
async def clearque(ctx):
	global music_que
	music_que.clear()
	await ctx.send("Que Cleared")



#ranking














@client.command()
async def play(ctx, * , url : str):
	if "https" in url:
		url = url

	else:
		videosSearch = VideosSearch(f'{str(url)}', limit = 1)
		url = str(videosSearch.result()["result"][0]["link"])
	#
	def music_loop(voice):
		song_there = os.path.isfile("song.wav")
		if loopState == True:
			voice.play(discord.FFmpegPCMAudio("song.wav"),after=lambda e: music_loop(voice))
		elif loopState == False:
			if not music_que:
				print("Print Music Ended Without Que")
				return
			elif music_que:
				os.remove("song.wav")
				ydl_opts = {
					'format': 'bestaudio/best',
					'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': 'wav',
						'preferredquality': '1411',
					}],
				}
				url = str(music_que[0])
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([url])
				for file in os.listdir("./"):
					if file.endswith(".wav"):
						os.rename(file, "song.wav")

				voice.play(discord.FFmpegPCMAudio("song.wav"),after=lambda e: music_loop(voice))
				music_que.pop(0)
				#


	song_there = os.path.isfile("song.wav")
	try:
		if song_there:
			os.remove("song.wav")
	except PermissionError:
		await ctx.send("Ay give it a minute will ya? music is still being playing if you wanna stop it use 'stop' command")
		music_que.append(url)
		await ctx.send(f"Music Added To The Que. QUE Length {len(music_que)}")
		print(music_que)
		return



	voiceChannel = ctx.message.author.voice.channel
	await voiceChannel.connect()
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)



	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'wav',
			'preferredquality': '1411',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".wav"):
			os.rename(file, "song.wav")
			song_name = file.rsplit("-",2)

			full_song_name = (f"{song_name[0]} - {song_name[1]}") 
			duration = "Unknown!" #str(videosSearch.result()["result"][0]["duration"])

	#await ctx.send(f"Playing {full_song_name}!")
	embed = discord.Embed(
		title = "Music Player",
		description = "Player 0.1",
		colour = discord.Colour.blue()

		)

	embed.set_image(url="https://media1.tenor.com/images/77f57fc5d06dc6642b0d96ef200cb550/tenor.gif?itemid=18482815")
	embed.add_field(name=f"Playing",value=f"Currently Playig {full_song_name}",inline=False)
	embed.add_field(name=f"Duration",value=f"{str(duration)}",inline=False)
	await ctx.send(embed=embed)
	voice.play(discord.FFmpegPCMAudio("song.wav"),after=lambda e: music_loop(voice))





@client.command()
async def leave(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect(force=True)
	else:
		await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
		await ctx.send("Song Paused")
	else:
		await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
		await ctx.send("Audio Resumed!")
	else:
		await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	voice.stop()
	await ctx.send("Music Stopped")




def ban_word_append(word):
	file = open("banned_words.txt","a")
	file.write(f"{word},")
	file.close()



def seachAPI(search):
	global random_line
	try:

		search = str(search)
		url = (f"https://api.giphy.com/v1/gifs/search?api_key=zIS8pY8QZ9IPtWPfkt4nISCFpIJy8zV1&limit=200&q={search}")
		data = requests.get(url)
		jsonx = data.json()
		f = open("random_gif.txt","a")

		for x in jsonx["data"]:
			#print(x["url"])
			f.write(x["url"])
			f.write("\n")
		f.close()
	except discord.errors.HTTPException:
		print("Bad input")
		pass
	randomLine = open("random_gif.txt","r").read().splitlines()
	random_line += random.choice(randomLine)
	#f.truncate(0)
	#f.close()


def verifyFileCount():
	global memes_count
	global shitpost_count
	global floppa_count
	try:
		while True:
			shitpost_count = 0
			memes_count = 0
			floppa_count = 0
			path, dirs, files = next(os.walk("C:/Users/xdSavitar/Desktop/Discord Bot/database/memes"))
			memes_count += len(files)
			path, dirs, files = next(os.walk("C:/Users/xdSavitar/Desktop/Discord Bot/database/shitpost"))
			shitpost_count += len(files)
			path, dirs, files = next(os.walk("C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa"))
			floppa_count += len(files)
			time.sleep(0.3)

	except StopIteration:
		print("Same Shit Again")

th2 = threading.Thread(target=verifyFileCount)
th2.start()

def printToConsole(args):
	print(f"{args} Just Used a command")



@client.event
async def on_ready():
	global start
	activity = discord.Game(name="please send help", type=3)
	await client.change_presence(status=discord.Status.online, activity=activity)
	end = time.time()
	print(f"Bot up and running execution time {start - end}")
@client.command()
async def cat(ctx):
	author = ctx.message.author
	printToConsole(author)

	img = 1
	for image in range(0,3):
		await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/cat/{img}.jpg"))
		img += 1

@client.command()
async def bonk(ctx):
	author = ctx.message.author
	printToConsole(author)
	img = random.randint(1,4)
	await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/bonk/{img}.jpg"))

@client.command()
async def walter(ctx):
	author = ctx.message.author
	printToConsole(author)
	img = 1
	for image in range(0,3):
		await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/walter/{img}.jpg"))
		img += 1



@client.command()
async def whoasked(ctx):
	img = random.randint(1,2)
	await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/whoasked/{img}.mp4"))




@client.command()
async def emergency(ctx):

	author = ctx.message.author
	printToConsole(author)
	await ctx.send(file=discord.File("C:/Users/xdSavitar/Desktop/Discord Bot/database/emergency/test.gif"))

	await ctx.send(f"<@454696216400232448> <@459002707315785730> <@236893334172336129>")


@client.command()
async def gocrazy(ctx):
	author = ctx.message.author
	printToConsole(author)
	await ctx.send(file=discord.File("C:/Users/xdSavitar/Desktop/Discord Bot/database/gocrazy/1.png"))


@client.command()
async def idk(ctx,message):
	author = ctx.message.author
	printToConsole(author)
	message = str(message)
	await ctx.send(message)


@client.command()
async def memecount(ctx):
	await ctx.send(f"Current Meme Count Is {memes_count}")

@client.command()
async def flopps(ctx):
	await ctx.send(f"Current Flopps Count {floppa_count}")


@client.command()
async def shitpost(ctx,*,message):
	if message == "r":
		try:

			video = random.randint(1,int(shitpost_count))
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/shitpost/{video}.mp4"))
		except discord.errors.HTTPException:
			print("[DEBUG] File To Large To Display")
			await ctx.send("File To Large To Display")
	else:

		try:

			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/shitpost/{message}.mp4"))

		except discord.errors.HTTPException:
			print("File To Large To Display")
			await ctx.send("File To Large To Display")


@client.command()
async def meme(ctx,*, message):
	if message == "r":
		img = random.randint(1,int(memes_count))
		try:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/memes/{img}.jpg"))
		except:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/memes/{img}.png"))
	else:
		try:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/memes/{message}.jpg"))
		except:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/memes/{message}.png"))


@client.command()
async def shitcount(ctx):
	await ctx.send(f"Current Shitpost Count {shitpost_count}")






@client.command()
async def floppa(ctx, * , message):
	if message == "r":
		img = random.randint(1,int(floppa_count))

		try:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa/{img}.jpg"))

		except:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa/{img}.png"))

	else:
		try:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa/{message}.jpg"))

		except:
			await ctx.send(file=discord.File(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa/{message}.png"))





@client.command()
async def gif(ctx,message):
	global random_line
	seachAPI(message)
	text = str(random_line)
	await ctx.send(text)
	file = open("random_gif.txt","w")
	file.write(" ")
	file.close()
	print(f"[DEBUG]: {text}")
	print(f"[DEBUG]: {random_line}")
	text = ""
	random_line = ""


@client.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def banword(ctx,message):
	banned_word = str(message)
	ban_word_append(banned_word)
	await ctx.send(f"Word Has Been Banned")


@client.command()
async def kick(ctx, member: discord.Member, * , reason = None): # member: discord.Member Because to work with discord user object 
	try:

		await member.kick(reason=reason)
	except discord.errors.Forbidden:
		print("Missing Permission")
		pass


@client.command()
async def commands(ctx):
	embed = discord.Embed(

		title = "Commands",
		description = "Current Commands For Cat-Bot",
		colour = discord.Colour.blue()

		)
	embed.set_footer(text="Ok go away now PS: if the bot is not working that cause its offline u donut i host the bot from my machine")
	embed.set_image(url="https://static.wikia.nocookie.net/dogelore/images/e/e1/Big_Floppa.jpg/revision/latest?cb=20200908210314")
	embed.set_thumbnail(url= "https://i2.wp.com/animeeverything.online/wp-content/uploads/2019/08/maxresdefault.jpg?fit=1280%2C720&ssl=1")
	embed.set_author(name = "Savitar",icon_url="https://i2.wp.com/animeeverything.online/wp-content/uploads/2019/08/maxresdefault.jpg?fit=1280%2C720&ssl=1")
	embed.add_field(name = "shitpost *r or *number",value="Gets a random shitpost video",inline=False)
	embed.add_field(name="meme *r or *number",value ="Gets a randodm meme",inline=False)
	embed.add_field(name="gif *search_query",value ="Gets a randomized gif from giphy",inline=False)
	embed.add_field(name="banword *word",value ="bans a specified word",inline=False)
	embed.add_field(name="banwordlist",value ="show the list of banned words",inline=False)
	embed.add_field(name="shitcount",value ="displays the ammount of shitpost videos in the database",inline=False)
	embed.add_field(name="memecount",value ="displays the ammount of memes in the database",inline=False)
	embed.add_field(name="bonk",value ="no horny",inline=False)
	embed.add_field(name="cat",value ="yes big cat",inline=False)
	embed.add_field(name="walter",value ="walter is the king",inline=False)
	embed.add_field(name="emergency",value ="emergency meeting",inline=False)
	embed.add_field(name="mywallet",value ="Shows ammount of coins you have",inline=False)
	embed.add_field(name="createwallet",value ="makes you a wallet if you dont have one",inline=False)
	embed.add_field(name="shop",value ="what do you expect this to be",inline=False)
	embed.add_field(name="playercommands",value ="shows the current list of commands for Music Player",inline=False)
	embed.add_field(name="floppa",value ="floppa is life",inline=False)



	await ctx.send(embed=embed)


@client.command()
async def banwordlist(ctx):
	file_words = open("banned_words.txt","r").read()
	await ctx.send(file_words)






@client.command()
@has_permissions(administrator=True, manage_messages=True, manage_roles=True)
async def clear(ctx,ammount=10):
	await ctx.channel.purge(limit=ammount)


def Logs(user,server_id,file_type):

	#print(user,server_id,file_type)
	#print(type(user),type(server_id),type(file_type))
	print("Logs")
	current_time = datetime.datetime.now()

	if (file_type == "jpg" or file_type == "png"):
		file = "Meme"
	elif file_type == ("mp4"):
		file = "Shitpost"


	if str(file_type) != "Usage Of Blacklisted Words":

		with open("logs.txt","a",encoding='utf-8') as LogsFile:
			LogsFile.write(f"[{str(current_time)}] {str(user)} Added {str(file)} To The Server [{str(server_id)}] \n")
			LogsFile.close()
	else:
		with open("logs.txt","a",encoding='utf-8') as LogsFile:
			LogsFile.write(f"[{str(current_time)}] {str(user)} Has Been Kicked From The Server {str(server_id)} \n")
			LogsFile.close()



def give_random_coin_reward(member_id,typei,boost):
	global coin_value
	print(boost)
	coin_value = 0
	current_time = datetime.datetime.now()

	random_coin_duplicate = random.randint(1,3)
	random_coin_duplicate1 = random.randint(1,3)


	if typei == "jpg" or typei == "png":
		if boost == True:
			coin_value += 1 * 2
		else:
			coin_value += 1


	if typei == "mp4":
		if boost == True:
			coin_value += 3 * 3
		else:
			coin_value += 3

		sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
		values = (f"{int(member_id)}",)
		cursor.execute(sql_string,values)
		result = cursor.fetchall()
		bonus_coins = result[0][2]


		sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
		values = (int(bonus_coins) + int(coin_value),int(member_id))
		cursor.execute(sql_string,values)
		mydb.commit()





def verifyUserBalance(member):
	global user_coins
	sql_string = "SELECT * FROM discordusersnew WHERE userID = %s"
	values = (f"{int(member)}",)
	cursor.execute(sql_string,values)
	result = cursor.fetchall()
	user_coins += int(result[0][2])



def updateUserBalance(member,price):
	global user_coins
	print(user_coins)
	
	sql_string = "UPDATE discordusersnew SET cat_coin = %s WHERE userID =%s"
	values = (int(user_coins) - int(price),int(member))
	cursor.execute(sql_string,values)
	mydb.commit()



#SHOP
@client.event
async def on_raw_reaction_add(payload):
	global user_coins
	global reaction_shop_id
	global temp_ticket_id
	global open_shop_id
	path = "C:/Users/xdSavitar/Desktop/Discord Bot/user_perks"

	if str(payload.message_id) == f"{reaction_shop_id}":
		channel = client.get_channel(payload.channel_id)

		if str(payload.emoji.name) == "buyboost" and str(payload.member) != "Cat-Bot#7325":
			verifyUserBalance(payload.member.id)
			if int(user_coins) >= 150 and int(user_coins) > 0:
				print("User Has Bought Coin Boost")

				if os.path.isdir(f"{path}/{payload.member.id}") == True:
					with open(f"{path}/{payload.member.id}/2xBoost.dvp","w") as W:
						W.close()
						await channel.send(f"<@{payload.member.id}> Has Bought Coin Boost 2X For Memes")
						updateUserBalance(payload.member.id,3)



		if str(payload.emoji.name) == "buyboost_shitposts" and str(payload.member) != "Cat-Bot#7325":
			verifyUserBalance(payload.member.id)
			if int(user_coins) >= 350 and int(user_coins) > 0:

				if os.path.isdir(f"{path}/{payload.member.id}") == True:
					with open(f"{path}/{payload.member.id}/2xBoost_shitpost.dvp","w") as W:
						W.close()
						await channel.send(f"<@{payload.member.id}> Has Bought Coin Boost 3X For Shitposts")
						updateUserBalance(payload.member.id,3)



	if str(payload.message_id) == str(811243009773273090):

		guild_id = payload.guild_id
		guild = client.get_guild(guild_id)
		role = discord.utils.get(guild.roles,name="cattolvl1")
		if str(payload.emoji.name) == "catcoin" and str(payload.member) != "Cat-Bot#7325":

			if role in payload.member.roles:
				print("Already have that role!")
			else:
				
				verifyUserBalance(payload.member.id)
				if int(user_coins) >= 500 and int(user_coins) > 0:
					print("cattolvl1 Role Bought")
					await client.get_channel(811221345064976415).send(f"<@{payload.member.id}> Has Bought ``cattolvl1`` Role!")
					await payload.member.add_roles(role)
					updateUserBalance(payload.member.id,450)





@client.command()
async def shop(ctx):
	global reaction_shop_id
	reaction_shop_id = ""
	embed = discord.Embed(

		title = "Shop",
		description = "Cat-Bot Shop",
		colour = discord.Colour.blue()

		)
	embed.set_image(url="https://media.istockphoto.com/vectors/vintage-small-shop-pixel-art-style-vector-icon-on-white-background-vector-id1040011824?k=6&m=1040011824&s=170667a&w=0&h=-pWRfZrBT0P1kSKsazducrJ9MLioD7IgyZ8lXb2JLTo=")
	embed.add_field(name = "Shitpost Coin Boost 3x",value="350 Coins",inline=False)
	embed.add_field(name="Memes Coin Boost 2x",value ="150 Coins",inline=False)
	sent_message = await ctx.send(embed=embed)
	print(ctx.message.author)

	reaction_shop_id += str(sent_message.id)

	await sent_message.add_reaction("<:buyboost:810658342124912650>")
	await sent_message.add_reaction("<:buyboost_shitposts:810686700136431617>")



troll_string = ["Sandex who asked you no1 . exactly.","Sandro no1 asked please stop taking thanks!","jett main please stop talking no1 asked","chuuu",]



@client.event
async def on_message(message):
	path = "C:/Users/xdSavitar/Desktop/Discord Bot/user_perks"
	global memes_count
	global floppa_count
	file_words = open("banned_words.txt","r")
	meme_DEPOSIT = [808457122454831114,811935847309115456]
	floppa_id = 813552118224781383

	if str(message.author) != "Cat-Bot#7325":
		if "wattson" in message.content.lower() or "wattsy" in message.content.lower():
			await message.channel.send("Wattson is ugly i spit on her Valkyrie best")
		

	try:

		format_type = (str(message.attachments[0].filename).split(".")[1])
	except IndexError:
		print(f"Command Executed By {str(message.author)}")

	try:

		if (str(message.author) != "Cat-Bot#7325" and str(message.attachments[0].filename).endswith(f"{format_type}") and int(message.channel.id) == floppa_id):
			role = discord.utils.get(message.guild.roles, name = "Memer")

			if str(role) in str(message.author.roles):
				print("Role Found")

				typeA = (str(message.attachments[0].filename).split(".")[1])
				attachment_url = (message.attachments[0].url)
				request = requests.get(attachment_url)
				print(request.status_code)


				if (typeA == "png" or typeA == "jpg" and request.status_code == 200):
					print(floppa_count)
					print("API ALIVE")
					with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/floppa/{int(floppa_count) + 1}.{str(typeA)}","wb") as file:
						file.write(request.content)
						await message.channel.send(f"<@{message.author.id}> Floppa is very happy, Floppa Count: {floppa_count + 2}")
						Logs(str(message.author),str(message.channel.id),str(typeA))




		if (str(message.author) != "Cat-Bot#7325" and str(message.attachments[0].filename).endswith(f"{format_type}") and int(message.channel.id) in meme_DEPOSIT):
			role = discord.utils.get(message.guild.roles, name = "Memer")
			print(role)
			print(message.author.roles)

			for roleInLoop in message.author.roles:

				if str(roleInLoop) == str(role):
					print("Role Found")

					print(f"[DEBUG]: new meme! meme count {memes_count}")
					image_type = (str(message.attachments[0].filename).split(".")[1])
					attachment_url = (message.attachments[0].url)
					request = requests.get(attachment_url)


					if (image_type == "mp4" and request.status_code == 200):
						print(request.status_code)
						with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/shitpost/{shitpost_count + 1}.{str(image_type)}","wb") as file:
							file.write(request.content)
							await message.channel.send(f"<@{message.author.id}> Thank you KIMNG! New Shitpost Has Been Added!. Current Meme Count {shitpost_count}")
							print(f"New Shitpost Added By {str(message.author)}")
							Logs(str(message.author),str(message.channel.id),str(image_type))
							print(message.author.id)

							try:
								with open(f"{path}/{message.author.id}/2xBoost_shitpost.dvp") as DVP:
									give_random_coin_reward(message.author.id,image_type,True)
									await message.channel.send(f"[BOOST ACTIVE]: <@{message.author.id}> You have recieved {coin_value} Coin(s) That has been added to your wallet!")

							except:
								give_random_coin_reward(message.author.id,image_type,False)
								await message.channel.send(f"<@{message.author.id}> You have recieved {coin_value} Coin(s) That has been added to your wallet!")




					if (image_type == "png" or image_type == "jpg" and request.status_code == 200):
						print(request.status_code)
						with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/database/memes/{memes_count + 2}.{str(image_type)}","wb") as file:
							file.write(request.content)
							await message.channel.send(f"<@{message.author.id}> Thank you KIMNG! New Meme Has Been Added!. Current Meme Count {memes_count}")
							print(f"New Meme Added By {str(message.author)}")
							Logs(str(message.author),str(message.channel.id),str(image_type))
							print(message.author.id)


							try:
								with open(f"{path}/{message.author.id}/2xBoost.dvp") as DVP:
									give_random_coin_reward(message.author.id,image_type,True)
									await message.channel.send(f"[BOOST ACTIVE]: <@{message.author.id}> You have recieved {coin_value} Coin(s) That has been added to your wallet!")
							except:
								give_random_coin_reward(message.author.id,image_type,False)
								await message.channel.send(f"<@{message.author.id}> You have recieved {coin_value} Coin(s) That has been added to your wallet!")


							#time.sleep(2)
							#await channel.message.purge(limt=1)			

	except IndexError:
		pass


	message_txt = str(message.content)

	if message_txt == "":
		message_txt = "Null"
	else:
		message_txt = str(message_txt)


	if message_txt.lower() in file_words.read().split(",") and str(message.author) != "Cat-Bot#7325":
		print("Banned word found")
		await message.channel.purge(limit=1)
		await message.channel.send(f"<@{message.author.id}> Bad Boy! Thats a Blacklisted Word You Will Be Kicked On 3 Warnings")

		try:

			with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/warnings/{str(message.author.id)}.txt","r",encoding="utf-8") as File:
				text = File.read()
				warning_ammount = str(text)
				File.close()
				print(text)

			with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/warnings/{str(message.author.id)}.txt","w",encoding="utf-8") as File:
				File.write(f"{int(warning_ammount) + 1}")
				File.close()





			if int(warning_ammount) == 2:
				await message.channel.send(f"<@{message.author.id}> You Have Been Warned {warning_ammount} Times: Action /Kick")
				os.remove(f"C:/Users/xdSavitar/Desktop/Discord Bot/warnings/{str(message.author.id)}.txt")
				try:
					await message.author.kick(reason="Blacklisted Words")


					await message.author.send(f"You Have Been Banned From The {message.guild.name} For Using Blacklisted Words")



					Logs(str(message.author),str(message.channel.id),"Usage Of Blacklisted Words")


				except discord.errors.Forbidden:

					print("Bot does not have admin or the user you are trying to kick is higher rank")




		except FileNotFoundError:
			f = open(f"C:/Users/xdSavitar/Desktop/Discord Bot/warnings/{str(message.author.id)}.txt","w",encoding="utf-8")
			f.write(f"{1}")
			f.close()




		except FileNotFoundError:
			print("File not found")

			with open(f"C:/Users/xdSavitar/Desktop/Discord Bot/warnings/{str(message.author.id)}.txt","w",encoding="utf-8") as File:

				text = File.write(f"{1}")
				

	
	await client.process_commands(message)


client.run("ODA4MDcwMzkyOTE2MjEzNzYw.YCBMMg.DcQW6JkwH9vFJYdYCnwSyc_ubzE")


