"""
디스코드 봇 캡챠 v1.0
메인 스크립트
commands, data, auth, database, log, main, verify
제작자: 류관형
"""
import discord
import commands
import verify
import auth
import database
import log

client = discord.Client()


@client.event
async def on_ready():
    log.call(__name__, on_ready.__name__, user=f"{client.user}")


@client.event
async def on_message(message):

    # 디버그 채널인 경우 모두 무시
    if message.channel.id == database.get_id_channel(8, 3):
        return

    # 로그 정보 생성
    user_id = message.author.name + "#" + message.author.discriminator
    log_content = message.content
    if isinstance(message.channel, discord.channel.DMChannel):
        log_author = user_id
        log_channel = 'DM'
        log_etc = {"author_id": message.author.id}
    else:
        log_author = user_id
        log_channel = message.channel.name
        log_etc = {"channel_id": message.channel.id, "Nick": message.author.nick}

    # 로깅
    log.division_line()
    log.call(__name__, on_message.__name__, author=log_author, channel=log_channel, content=log_content, note=log_etc)

    # 발신자가 봇인 경우 아래 내용 실행 안함
    if message.author == client.user:
        return

    # DM인 경우 fork_dm, 아닌경우 fork 호출
    channel = message.channel
    if isinstance(message.channel, discord.channel.DMChannel):
        await commands.direct.fork(channel, message, client)
    else:
        await commands.fork(channel.category, channel, message)

    # 디버그 채널에 로그 전송
    debug_ch = client.get_channel(database.get_id_channel(8, 3))
    try:
        await debug_ch.send('\n'.join(log.cache))
    except discord.errors.HTTPException:
        await debug_ch.send('400: [discord.errors.HTTPException]')
    log.cache.clear()


client.run('ODgyMTc1NTk5MTM1ODE3NzQ4.YS3kDA.t6Q7jLRBY8r5-t97NsCoCzeEq4w')