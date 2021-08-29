import discord

client = discord.Client()

queue = []

admins = [78907597943472128]

priv_roles = [881592747985891419, 881592716121763842]

prefix = '?'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix+"joinq"):
        if message.author.id in queue:
            await message.channel.send('You are already in the queue, use '+prefix+"status to check your position")
        else:
            await message.channel.send('Adding you to the queue')
            queue.append(message.author.id)

    if message.content.startswith(prefix+"leaveq"):
        if message.author.id in queue:
            await message.channel.send('removing you from the queue')
            queue.remove(message.author.id)
        else:
            await message.channel.send('You are not currently in the queue')

    if message.content.startswith(prefix+"status"):
        embed = discord.Embed(title="Current Queue")
        y = 0
        for x in queue:
            embed.add_field(name="Position #"+str(y), value="Member: <@"+str(queue[y])+">")
            y = y + 1
        await message.channel.send(embed=embed)

    if message.content.startswith(prefix+"next"):
        for x in priv_roles:
            for y in message.author.roles:
                if x == y.id:
                    # await message.channel.send('You have permission')
                    await message.channel.send("Next up is <@" + str(queue.pop())+">")
                    return
        await message.channel.send('You do not have permission')
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('token')
