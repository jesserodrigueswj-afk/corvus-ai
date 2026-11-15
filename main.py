import discord
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    texto = message.content.lower().strip()

    if texto in ['!ola', '!olá', 'ola', 'olá']:
        await message.channel.send('Olá! Eu sou o CORVUS AI. 🐦‍⬛')
        return

    if texto == '!ajuda':
        await message.channel.send('**Sou o CORVUS AI. da Ordem dos Corvos!**\nUse:\n`!ola` - para falar oi\n`!pergunta raid` - como funciona raid\n`!pergunta build` - dicas de build\n`!regras` - regras da Ordem\n`!evento raid sábado 20h` - criar comunicado de evento\nOu me marque e pergunte qualquer coisa!')
        return

    if texto == '!regras':
        await message.channel.send('**REGRAS DA ORDEM DOS CORVOS:**\n\n**1.** Respeito acima de tudo. Proibido racismo, preconceito, homofobia, xenofobia ou qualquer tipo de discriminação. Zero tolerância.\n**2.** Proibido pornografia. Proibido foto, vídeo, link, figurinha ou conversa com conteúdo sexual, nudez ou pornografia.\n**3.** Proibido pedir dinheiro, Pix, doação, empréstimo ou venda dentro do servidor.\n**4.** Proibido link de jogos de azar. Proibido tigrinho, cassino, aposta, roleta, ou qualquer link de jogo de azar.\n**5.** Sem briga, sem ofensa, sem toxicidade no chat ou no voice.\n**6.** Proibido trapaça, hack, exploit ou bug para levar vantagem no Once Human.\n**7.** Ajude nas raids e eventos. Se confirmar presença, apareça.\n**8.** Respeite os líderes e os membros mais antigos.\n\nQuem quebrar, leva advertência, depois mute, e se continuar, ban.')
        return

    if texto.startswith('!evento '):
        tema = message.content[8:]
        await message.channel.send(f'📢 **COMUNICADO DA ORDEM DOS CORVOS** 📢\n\nCorvos, atenção!\nTemos evento: **{tema}**\n\nConfirmem presença reagindo aqui! 🐦‍⬛\nNos vemos no campo de batalha!')
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
