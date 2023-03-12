import discord
import os
import random
import io
import aiohttp
from dotenv import load_dotenv
from discord.ext import commands
from db_filmes import lista_filmes

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_TOKEN = os.getenv('CHANNEL_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready(message):
    # print("Hello World. Framed Bot is now online!")
    print(f"Hello World! {bot.user} is now online!")
    channel = bot.get_channel(CHANNEL_TOKEN)
    await message.channel.send("Hello World! Framed Bot is now online")


meio_jogo = 0
index_filme = 1000
index_imagem_filme = 1
@bot.event
async def on_message(message):
    if message.content.startswith("!"):
        global meio_jogo
        global index_filme
        global index_imagem_filme
        if not meio_jogo:
            index_filme = random.randint(31, 370)
            index_imagem_filme = 1
        if message.content.startswith("!framed"):
            meio_jogo = 1
            index_filme = random.randint(31, 370)
            await message.channel.send("Vamos jogar uma partida de Framed!")
            
            # envio da imagem ---> é preciso criar uma função, 
            # já que tal processo é repetido ao longo do código. 
            async with aiohttp.ClientSession() as session:
                foto_inicial = "https://framed.wtf/images/{0}/00{1}.jpeg".format(str(lista_filmes[index_filme]["id"]), str(index_imagem_filme))
                async with session.get(foto_inicial) as resp:
                    if resp.status != 200:
                        return await message.channel.send("Estou com problemas para enviar a imagem...")
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, "imagem.jpeg"))

        else: #tentativa de filme e.g. !Kill Bill
            tentativa = message.content[1:]
            if tentativa.lower() == lista_filmes[index_filme]["title"].lower():
                await message.channel.send("Parabéns, você acertou! :grin:")
            else:
                index_imagem_filme += 1
                if index_imagem_filme == 6:
                    await message.channel.send("Errado... Sua última tentativa:")

                    # envio da imagem ---> é preciso criar uma função, 
                    # já que tal processo é repetido ao longo do código. 
                    async with aiohttp.ClientSession() as session:
                        foto = "https://framed.wtf/images/{0}/00{1}.jpeg".format(str(lista_filmes[index_filme]["id"]), str(index_imagem_filme))
                        async with session.get(foto) as resp:
                            if resp.status != 200:
                                return await message.channel.send("Estou com problemas para enviar a imagem...")
                            data = io.BytesIO(await resp.read())
                            await message.channel.send(file=discord.File(data, "imagem.jpeg"))

                elif index_imagem_filme > 6:
                    await message.channel.send("Errado de novo. O filme era {0} :nerd:".format(lista_filmes[index_filme]["title"]))
                else:    
                    await message.channel.send("Errado... Vou mandar uma foto mais fácil:")

                    # envio da imagem ---> é preciso criar uma função, 
                    # já que tal processo é repetido ao longo do código. 
                    async with aiohttp.ClientSession() as session:
                        foto = "https://framed.wtf/images/{0}/00{1}.jpeg".format(str(lista_filmes[index_filme]["id"]), str(index_imagem_filme))
                        async with session.get(foto) as resp:
                            if resp.status != 200:
                                return await message.channel.send("Estou com problemas para enviar a imagem...")
                            data = io.BytesIO(await resp.read())
                            await message.channel.send(file=discord.File(data, "imagem.jpeg"))


bot.run(BOT_TOKEN)