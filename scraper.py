import requests
import time
import os
import pandas as pd  
import sqlite3
from telegram import Bot
import asyncio
from bs4 import BeautifulSoup
from bd_sqlite import create_connection, setup_database, save_to_database



#TOKEN = os.getenv("TELEGRAM_TOKEN")
#CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


#if not TOKEN or not CHAT_ID:
    #raise ValueError("As variáveis de ambiente TELEGRAM_TOKEN e TELEGRAM_CHAT_ID devem ser definidas.")


#bot = Bot(token=TOKEN)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_page(url):

    response = requests.get(url, headers=headers)

    time.sleep(2) 

    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    product_name = soup.find('span', {'id': 'productTitle'})
    product_name = product_name.get_text().strip() if product_name else "N/A"

    product_price = soup.find('span', class_='a-price-whole')
    product_price = product_price.get_text().strip().replace(",", "") if product_price else "0"

    product_price_fraction = soup.find('span', class_='a-price-fraction')
    product_price_fraction = product_price_fraction.get_text().strip() if product_price_fraction else "0"

    recomended_price = soup.find('span', class_='a-price a-text-price')
    recomended_price = recomended_price.get_text().strip().replace(",", "") if recomended_price else "0"
    full_price = f"{product_price}.{product_price_fraction}"

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    return {
        'product_name': product_name,
        'product_full_price': full_price,
        'recomended_price': recomended_price,
        'timestamp': timestamp
    }

def get_max_price(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(product_full_price), timestamp FROM prices")

    result = cursor.fetchone()

    return result[0], result[1]


#async def telegram_send_message(message):
   #await bot.send_message(chat_id=CHAT_ID, text=message)

def save_to_df(product_info, df):
    new_row = pd.DataFrame([product_info])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

async def main():
    
    url = "https://www.amazon.es/dp/B0DGJHPQKM/ref=sr_1_4_sspa?dib=eyJ2IjoiMSJ9.mS374OgY6mH0aOQZQ1g_6YBFV7Us6CZNkwT7Xda7dCue3eDlpBQIF3jpQuaE9ZBWJ8Q2tp4PnGe5IDMXkIZaVA3wWXeJac8h04VQNRGRxnVeNTSA6h5SHCaA4r1Xfi6Yh2OINLLjreUe1asjybh4OJL7Py_dknjcos6baQNsMh0pk_16dkQQAJzI3YwYItLb-ptT3La-uwxIA-Nh60OavVBDMMg8WvgkeupS53OSJt2zQN9Zl9YAFGJp80ypyDFqMxhXr_-RLSas6aJNr7wFz_9HML_DFoKWy42j1i9bpYg.tfsykA0Xb_v35eci2q5qQp4TcIZMpdohrled88TvsiQ&dib_tag=se&keywords=iphone&qid=1739806372&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
    
    # Cria a conexão com o banco de dados
    conn = create_connection()
    setup_database(conn)

    while True:
        page_content = fetch_page(url)
        product_info = parse_page(page_content)

        max_price, max_timestamp = get_max_price(conn)

        current_price = product_info['product_full_price']

        if current_price is None  > float(max_price):
            print("Max Price detected")
            max_price = current_price
            #await telegram_send_message(f'Max price deteceted: {max_price}')
            max_price_timestamp = product_info['timestamp']
        else:
            print(f"The max price registed is: {max_price} at {max_timestamp}")
            #await telegram_send_message(f'The max price registed is: {max_price} at {max_timestamp}')

        # Salva no banco de dados SQLite
        save_to_database(conn, product_info)
        print("Dados salvos:", product_info)
        time.sleep(20)
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())