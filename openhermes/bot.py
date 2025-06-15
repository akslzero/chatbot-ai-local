import discord
import requests
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # penting biar bisa baca isi pesan

client = discord.Client(intents=intents)

TOKEN = "token"

# Fungsi buat komunikasi ke Ollama/OpenHermes
def tanya_openhermes(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "openhermes",
        "prompt": f"Ngobrol santai ya. Gunakan bahasa Indonesia. {prompt}",
        "stream": False
    })
    return response.json()["response"]

@client.event
async def on_ready():
    print(f'Bot aktif sebagai {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Cek jika bot disebut
    if client.user in message.mentions:
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        await message.channel.typing()
        loop = asyncio.get_event_loop()
        jawaban = await loop.run_in_executor(None, tanya_openhermes, prompt)

        await message.reply(jawaban)

client.run(TOKEN)
