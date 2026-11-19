
import discord
import os
import random
import datetime
from flask import Flask
from threading import Thread
from discord.ext import tasks

app = Flask('')
@app.route('/')
def home():
    return 'CORVUS AI online!'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
Thread(target=run, daemon=True).start()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

DICAS = [
    "Não esquece de pegar seu Deviation todo dia, ele te ajuda muito no farm.",
    "Antes da raid, come uma comida que dá buff de dano. Faz muita diferença!",
    "Upe sua arma principal primeiro, não gasta material em arma que você não usa.",
    "Deixa sempre munição, cura e comida sobrando na base pra raid de última hora.",
    "Explora o mapa com calma, tem baú e Deviation escondido em lugar que ninguém olha.",
    "Entra no canal de voz antes da raid, fica muito mais fácil combinar.",
    "Não esquece de reparar sua armadura antes de sair pra raid.",
    "Se você está travado em uma missão, chama a Ordem no chat, ninguém joga sozinho aqui.",
    "Guarda seu Starchrom pra coisa que vale a pena, não gasta à toa.",
    "Verifica sua base todo dia, o Deviation da base trabalha pra você mesmo offline.",
    "Na raid, quem vai de tanque vai na frente, quem vai de dano fica atrás. Combina antes!",
    "Leva sempre uma arma secundária, se a principal quebrar no meio da luta você não fica parado.",
    "Faz as missões diárias, elas dão recompensa boa e são rapidinhas.",
    "Se confirmar presença no evento, apareça! A equipe conta com você.",
    "Dorme bem, bebe água e volta forte. Corvo cansado não mira direito! 🐦‍⬛"
]

PALAVRAS_PROIBIDAS = ["tigrinho", "cassino", "aposta", "roleta", "onlyfans", "xvideos", "pornhub", "me manda pix", "faz um pix", "pix pra mim", "me empresta dinheiro", "me doa"]

@tasks.loop(time=datetime.time(hour=13, minute=0))
async def dica_diaria():
    canal = discord.utils.get(client.get_all_channels(), name="evento")
    if canal:
        dica = random.choice(DICAS)
        await canal.send(f"🐦‍⬛ **DICA DO DIA - ORDEM DOS CORVOS**\n\n{dica}\n\nBom jogo, corvos!")

@client.event
async def on_ready():
    print(f'Logado como {client.user}')
    if not dica_diaria.is_running():
        dica_diaria.start()

@client.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.channels, name="geral")
    if not canal:
        canal = discord.utils.get(member.guild.channels, name="boas-vindas")
    if not canal:
        canal = discord.utils.get(member.guild.channels, name="evento")
    if canal:
        await canal.send(f"Bem-vindo, {member.mention}! 🐦‍⬛\nVocê entrou na **ORDEM DOS CORVOS**!\nLê as regras com `!regras` e se apresenta pra galera!\nBom jogo, corvo!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    texto = message.content.lower().strip()

    # 3 - Anti-palavrão / anti-link
    if not texto.startswith("!"):
        for palavra in PALAVRAS_PROIBIDAS:
            if palavra in texto:
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(f"Ei {message.author.mention}, isso é proibido nas regras da Ordem! Proibido link de jogo de azar, pedir Pix/dinheiro e conteúdo pornográfico. Se continuar, leva advertência.")
                return

    if texto in ['!ola', '!olá', 'ola', 'olá']:
        await message.channel.send('Olá! Eu sou o CORVUS AI. 🐦‍⬛')
        return

    if texto == '!dica':
        dica = random.choice(DICAS)
        await message.channel.send(f"🐦‍⬛ **DICA DO DIA**\n\n{dica}")
        return

    if texto == '!ajuda':
        await message.channel.send('**Sou o CORVUS AI. da Ordem dos Corvos!**\nUse:\n`!ola` - para falar oi\n`!dica` - dica do dia de Once Human\n`!pergunta raid` - como funciona raid\n`!pergunta build` - dicas de build\n`!regras` - regras da Ordem\n`!evento raid sábado 20h` - criar comunicado com votação\nOu me marque e pergunte qualquer coisa!')
        return

    if texto == '!regras':
        await message.channel.send('**REGRAS DA ORDEM DOS CORVOS:**\n\n**1.** Respeito acima de tudo. Proibido racismo, preconceito, homofobia, xenofobia ou qualquer tipo de discriminação. Zero tolerância.\n**2.** Proibido pornografia. Proibido foto, vídeo, link, figurinha ou conversa com conteúdo sexual, nudez ou pornografia.\n**3.** Proibido pedir dinheiro, Pix, doação, empréstimo ou venda dentro do servidor.\n**4.** Proibido link de jogos de azar. Proibido tigrinho, cassino, aposta, roleta, ou qualquer link de jogo de azar.\n**5.** Sem briga, sem ofensa, sem toxicidade no chat ou no voice.\n**6.** Proibido trapaça, hack, exploit ou bug para levar vantagem no Once Human.\n**7.** Ajude nas raids e eventos. Se confirmar presença, apareça.\n**8.** Respeite os líderes e os membros mais antigos.\n\nQuem quebrar, leva advertência, depois mute, e se continuar, ban.')
        return

    if texto.startswith('!evento '):
        tema = message.content[8:]
        msg = await message.channel.send(f'📢 **COMUNICADO DA ORDEM DOS CORVOS** 📢\n\nCorvos, atenção!\nTemos evento: **{tema}**\n\nReage com ✅ pra confirmar presença e ❌ se não vai!\nNos vemos no campo de batalha!')
        try:
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
        except:
            pass
        return

    if texto.startswith('!pergunta ') or client.user in message.mentions:
        if texto.startswith('!pergunta '):
            pergunta = texto[10:]
        else:
            pergunta = texto.replace(f'<@{client.user.id}>', '').strip()

        if 'raid' in pergunta:
            resposta = 'No Once Human, raid é missão em grupo, geralmente com 4 jogadores. Leve build forte, munição, comida e cura. Combine com a equipe quem vai de tanque, dano e suporte. Entre no canal de voz antes de começar e siga o líder da raid.'
        elif 'build' in pergunta or 'arma' in pergunta:
            resposta = 'Para build no Once Human, foque em uma arma principal e nos Deviations que combinam com ela. Upe sua arma, use mods certos e não esqueça de comida que dá buff.'
        elif 'evento' in pergunta:
            resposta = 'Para criar um evento, escreve `!evento` + o que vai ter. Exemplo: `!evento raid sábado 20h`. Eu crio o comunicado pronto para o #evento.'
        elif 'regra' in pergunta:
            resposta = 'Escreve `!regras` que eu te mostro as regras da Ordem dos Corvos.'
        elif 'once human' in pergunta or 'jogo' in pergunta:
            resposta = 'Once Human é um jogo de sobrevivência em mundo aberto. Você explora, constrói base, enfrenta monstros e Deviations, e joga em grupo na Ordem dos Corvos.'
        else:
            resposta = f'Boa pergunta! Sobre "{pergunta}", ainda estou aprendendo. Tenta perguntar de raid, build, regras ou evento. Ou escreve `!ajuda` para ver tudo que eu sei.'

        await message.channel.send(resposta)
        return

client.run(TOKEN)