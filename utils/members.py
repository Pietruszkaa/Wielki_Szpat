import settings

async def update_member_counter(guild):
    channel = guild.get_channel(settings.MEMBER_COUNT_CHANNEL_ID)
    if not channel:
        return

    count = guild.member_count
    new_name = f"Członkowie = {count}"

    if channel.name != new_name:
        await channel.edit(name=new_name)
