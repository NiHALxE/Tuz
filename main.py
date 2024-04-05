import telebot
import requests
import speedtest
import asyncio

# Initialize bot
bot = telebot.TeleBot("6977219925:AAH4c9KOL33rPYlcFCebPBvkGmzn0W7flh8")

def check_proxy(proxy):
    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
    proxy_auth = requests.auth.HTTPProxyAuth(proxy['username'], proxy['password'])
    
    try:
        # Use a reliable website to check if the proxy is working
        response = requests.get('https://api.ipify.org', proxies={'http': proxy_url}, auth=proxy_auth, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def measure_speed(proxy):
    try:
        # Initialize a Speedtest object
        st = speedtest.Speedtest()
        
        # Set proxy for speedtest (optional)
        st.http_proxy = f"http://{proxy['ip']}:{proxy['port']}"
        
        # Get download and upload speed
        st.download()
        st.upload()
        
        # Convert speed to Mbps
        download_speed = st.results.download / 1000000
        upload_speed = st.results.upload / 1000000
        
        return download_speed, upload_speed
    except Exception as e:
        return None, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton('Proxy✨')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Welcome! Please choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Proxy✨':
        bot.send_message(message.chat.id, "Please enter the country code (e.g., US):")
    else:
        bot.send_message(message.chat.id, "Invalid option. Please choose 'Proxy✨'.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
async def process_country_code(message):
    country_code = message.text.upper()
    
    # Replace 'cz' in the username with the country code
    proxy_username = "5flsmkxrsw9o46c-country-cz-session-xnoy1n2rz2-lifetime-15"
    proxy_username = proxy_username.replace('cz', country_code)
    
    # Proxy details
    proxy = {
        'ip': 'rp.proxyscrape.com',
        'port': 6060,
        'username': proxy_username,
        'password': '7fjkcjp6a6s1ega'
    }
    
    if check_proxy(proxy):
        download_speed, upload_speed = measure_speed(proxy)
        if download_speed is not None and upload_speed is not None:
            proxy_info = f"Proxy Details:\nIP: {proxy['ip']}\nPort: {proxy['port']}\nUsername: {proxy['username']}\nPassword: {proxy['password']}\n\nIPv4 Address: {proxy['ip']}\nDownload Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
            await bot.send_message(message.chat.id, proxy_info, parse_mode='Markdown')
        else:
            await bot.send_message(message.chat.id, "Proxy is working, but speed test failed.")
    else:
        await bot.send_message(message.chat.id, "Proxy is not working.")

async def main():
    await bot.polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
