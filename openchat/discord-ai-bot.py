import discord
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model dan tokenizer DialoGPT
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")

# Setup client Discord dengan intents
intents = discord.Intents.default()
intents.message_content = True  # Ini perlu agar bot bisa baca pesan

client = discord.Client(intents=intents)

# Fungsi untuk generate respons dari bot dengan gaya lebih santai untuk roleplay
def chat_with_bot(input_text):
    # Persona atau gaya bicara bot yang santai
    persona = "Kamu adalah teman yang santai, asyik, dan selalu siap ngobrol. Jangan terlalu formal, lebih ke gaya ngobrol biasa aja."
    
    # Gabungkan persona dan input
    input_text = persona + " " + input_text

    # Encode input dan generate output
    new_user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    
    # Generate response dengan pengaturan kreatif
    bot_output = model.generate(
        new_user_input_ids,
        max_length=1000,
        temperature=0.8,  # Lebih kreatif dan variatif
        top_p=0.9,  # Lebih natural dengan memilih kata-kata yang relevan
        pad_token_id=tokenizer.eos_token_id
    )
    
    # Decode output ke dalam bentuk teks
    bot_output_text = tokenizer.decode(bot_output[0], skip_special_tokens=True)
    return bot_output_text

# Event ketika bot siap
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event ketika ada pesan masuk
@client.event
async def on_message(message):
    # Jangan balas pesan dari bot itu sendiri
    if message.author == client.user:
        return

    # Cek jika bot disebut di server
    if client.user in message.mentions:
        # Menghapus mention bot dari pesan
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        # Kirim ke model untuk mendapatkan respons
        response = chat_with_bot(prompt)

        # Balas dengan respons dari bot
        await message.reply(response)

    # Kalau bot nggak disebut, tetap bisa respons biasa jika perlu
    # (bisa kamu tambahkan logika lain kalau perlu)

# Jalankan bot dengan token yang sudah didapatkan
client.run('token')
