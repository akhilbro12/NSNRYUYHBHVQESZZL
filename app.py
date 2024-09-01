import telebot
import yt_dlp
import os
import re

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7344915455:AAFSYEOEOBFxw5DRA0ZGg2bDPaT6TizoH90'
bot = telebot.TeleBot(BOT_TOKEN)

# Ensure the download directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Function to validate YouTube URL
def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube\.com/watch\?v=|youtube\.com/shorts/|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)'
        r'[\w-]+')
    return re.match(youtube_regex, url) is not None

# Track progress state
last_progress = None

# Progress bar function
def download_progress_hook(d):
    global last_progress
    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)
        percent = (downloaded / total) * 100 if total else 0
        bar_length = 10
        filled_length = int(bar_length * percent // 100)
        bar = '▰' * filled_length + '▱' * (bar_length - filled_length)
        progress_message = f"{bar} {int(percent)}%"
        
        if progress_message != last_progress:
            bot.edit_message_text(text=progress_message, chat_id=progress_chat_id, message_id=progress_message_id)
            last_progress = progress_message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "𝗛𝗲𝘆, 𝗦𝗲𝗻𝗱 𝗺𝗲 𝗮 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝘃𝗶𝗱𝗲𝗼 𝗨𝗥𝗟 𝗮𝗻𝗱 𝗜 𝘄𝗶𝗹𝗹 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗶𝘁 𝗳𝗼𝗿 𝘆𝗼𝘂.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    print(f"Received URL: {url}")  # Debug print

    if not is_valid_youtube_url(url):
        bot.reply_to(message, 'This is not a valid YouTube Video/short/watch URL, Try Again.🤔')
        return

    global progress_chat_id, progress_message_id, last_progress
    try:
        # Send an initial message to update with progress
        progress_message = bot.reply_to(message, "▰▱▱▱▱▱▱▱▱▱ 0%")
        progress_chat_id = message.chat.id
        progress_message_id = progress_message.message_id
        last_progress = "▰▱▱▱▱▱▱▱▱▱ 0%"

        ydl_opts = {
            'format': 'best',  # Download the best available single file format
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [download_progress_hook],  # Add progress hook
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        # Send the video to the user
        with open(file_path, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption=f'Downloaded: {info["title"]}')

        # Clean up: delete the video file after sending it
        os.remove(file_path)

        # Update the progress message to indicate completion
        bot.edit_message_text(text="▰▰▰▰▰▰▰▰▰▰ 100%\n𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅", chat_id=progress_chat_id, message_id=progress_message_id)

        # Send a new message indicating success
        bot.send_message(message.chat.id, "𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙚𝙙 𝘽𝙮 𝙍𝙚𝙖𝙡𝙞𝙨𝙩𝙞𝙘 ♥️")

    except Exception as e:
        print(f"Exception: {str(e)}")  # Debug print
        bot.reply_to(message, '𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐰𝐞𝐧𝐭 𝐰𝐫𝐨𝐧𝐠. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫.😟\n𝐏𝐨𝐬𝐬𝐢𝐛𝐥𝐞 𝐑𝐞𝐚𝐬𝐨𝐧𝐬:\n• 𝐈𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐋𝐢𝐧𝐤\n• 𝐋𝐢𝐧𝐤 𝐄𝐱𝐩𝐢𝐫𝐞𝐝\n• 𝐍𝐨𝐭 𝐀 𝐕𝐚𝐥𝐢𝐝 𝐘𝐨𝐮𝐓𝐮𝐛𝐞 𝐋𝐢𝐧𝐤.')

# Start polling
bot.polling()
