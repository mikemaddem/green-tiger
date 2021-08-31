import discord
import config

client = discord.Client()

queue = []

admins = [78907597943472128]

priv_roles = [877256642280947742, 877256845205581905]

prefix = '?'

is_open=False


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + "joinq"):
        await message.delete()
        if is_open:
            pass
        else:
            await message.channel.send('<@'+str(message.author.id)+'> The queue is currently not open, please wait for office hours to begin')
            return
        
        if message.author.id in queue:
            await message.channel.send('<@' + str(
                message.author.id) + '> You are already in the queue, use ' + prefix + "status to check your position")
        else:
            await message.channel.send('<@' + str(message.author.id) + '> Adding you to the queue')
            queue.append(message.author.id)

    if message.content.startswith(prefix + "leaveq"):
        await message.delete()
        if is_open:
            pass
        else:
            await message.channel.send('<@'+str(message.author.id)+'> The queue is currently not open, please wait for office hours to begin')
            return
        
        if message.author.id in queue:
            await message.channel.send('<@' + str(message.author.id) + '> Removing you from the queue')
            queue.remove(message.author.id)
        else:
            await message.channel.send('<@' + str(message.author.id) + '> You are not currently in the queue')

    if message.content.startswith(prefix + "status"):
        await message.delete()
        if is_open:
            pass
        else:
            await message.channel.send('<@'+str(message.author.id)+'> The queue is currently not open, please wait for office hours to begin')
            return
        
        embed = discord.Embed(title="Current Queue")
        y = 0
        for x in queue:
            embed.add_field(name="Position #" + str(y), value="Member: <@" + str(queue[y]) + ">")
            y = y + 1
        await message.channel.send(embed=embed)

    if message.content.startswith(prefix + "next"):
        if is_open:
            pass
        else:
            await message.channel.send('<@'+str(message.author.id)+'> The queue is currently not open, please wait for office hours to begin')
            return
        
        if len(queue) == 0:
            await message.channel.send("The queue is currently empty!")
            return
        for x in priv_roles:
            for y in message.author.roles:
                if x == y.id:
                    # await message.channel.send('You have permission')
                    await message.channel.send("Next up is <@" + str(queue.pop(0)) + ">")
                    return
        await message.channel.send('<@' + str(message.author.id) + '> You do not have permission to this command')
        return

    if message.content.startswith(prefix + 'help'):
        embed = discord.Embed(title="Bot Commands",
                              description="Get up and running with this simple Discord Queue bot!",
                              url="https://www.github.com/mikemaddem/green-tiger")
        embed.add_field(name=prefix + "joinq Command",
                        value="Use " + prefix + "joinq to join the queue and get assistance", inline=True)
        embed.add_field(name=prefix + "leaveq Command",
                        value="Use " + prefix + "leaveq to leave the queue. You will lose your spot on line, you are able to rejoin however you'll rejoin at the end of the queue", inline=True)
        embed.add_field(name=prefix + "next",
                        value="For use by TA's/Faculty to grab the next person in queue. Current roles = <@" + str(
                            priv_roles[0]) + "> and <@" + str(priv_roles[1]) + ">", inline=True)

        await message.channel.send(embed=embed)

    if message.content.startswith(prefix+'openq'):
        if is_open:
            await message.channel.send("The queue is already open")
            return
        for x in priv_roles:
            for y in message.author.roles:
                if x == y.id:
                    # await message.channel.send('You have permission')
                    is_open=True
                    await message.channel.send("The queue is now open")
                    return

    if message.content.startswith(prefix+'closeq'):
        if not is_open:
            await message.channel.send("The queue is already closed")
            return
        for x in priv_roles:
            for y in message.author.roles:
                if x == y.id:
                    # await message.channel.send('You have permission')
                    is_open=False
                    await message.channel.send("The queue is now closed")
                    return



client.run(config.token)
