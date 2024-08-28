import asyncio
import random
import sys
from traceback import format_exc

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

DATA = {}
ENV = """
API_ID={20840106}
API_HASH={bf9a89f3eeb6f95a807f0630343b90a1}
BOT_TOKEN={7120419293:AAGr3AXCO7NFoxjRfwzisTDKZA73b_RNbtA}
SESSION={BQFljg4AOFezSKThTNfj6OKWW-y_ibMXxpbLVxYOdW08oWBy3XS0OlheMdh8Q_Zreyb7506aoV5icRCm7rx8B3VmYxG4B8XDQ0iNKgGSgwjpRPCbR-gBDQ4YYm2zG53J-aYWU3usPqMkxDT-j44KtRGz_Lcqa0KeAMP00VXPimMaQL-5KLY95Q9o16szpUZsMNp8PDF0uIaNj05XPBWbPe-hRpZgLBLgUVjXdK75L2_GzN2ctH-1QvMkjFzJ60TkieUBveHvLnt3D0fhixZLAxAp1DfrRNTWisNQDlRMVeLOeXSpmW4W8jkoo1AwhQGfZT4AJpnrFNIZbEd-1FxwIvx1QB1JHQAAAAFFiah_AA}
MAIN_CHANNEL={-1002127007062}
LOG_CHANNEL={-1001514459022}
CLOUD_CHANNEL={-1002138483355}
BACKUP_CHANNEL={-1002212479203}
FIREBASE_URL={https://rengoku1637-default-rtdb.firebaseio.com/}
FIREBASE_SERVICE_ACCOUNT_FILE={https://gist.githubusercontent.com/Sakazuki-Akainu/ced64ac21a7231e24cdec3732077ebe0/raw/888e6eaeed12ec507ace467b8a81765100e0ca78/service.json}
OWNER={5461616767}
"""


async def generate_session_string():
    api_id = int(input("Enter your API_ID: "))
    api_hash = input("Enter your API_HASH: ")
    if api_id and api_hash:
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            DATA["api_id"] = api_id
            DATA["api_hash"] = api_hash
            DATA["session"] = str(client.session.save())
            return (str(client.session.save()), api_id, api_hash)
    print("API_ID and HASH Not Found!")
    sys.exit(1)


def get_firebase():
    uri = input("Enter your Firebase Realtime Database Url: ")
    _pass = input("Enter your Firebase Realtime Database Service Account File Link: ")
    if uri and _pass:
        DATA["firebase_uri"] = uri
        DATA["firebase_pass"] = _pass
        return True
    else:
        DATA["firebase_uri"] = ""
        DATA["firebase_pass"] = ""
        return False


async def create_channel(client, title):
    try:
        r = await client(
            CreateChannelRequest(
                title=title,
                about="Made By https://github.com/kaif-00z/AutoAnimeBot",
                megagroup=False,
            )
        )

        created_chat_id = r.chats[0].id
        return f"-100{created_chat_id}"
    except BaseException:
        print("Unable to Create Channel...")
        sys.exit(1)


def generate_env():
    txt = ENV.format(
        DATA["api_id"],
        DATA["api_hash"],
        DATA["bot_token"],
        DATA["session"],
        DATA["Ongoing Anime 2024"],
        DATA["Ongoing Anime Logs"],
        DATA["Ongoing Anime Samples And SS"],
        DATA["Ongoing Anime Backup"],
        DATA.get("firebase_uri") or "",
        DATA.get("firebase_pass") or "",
        DATA["owner_id"],
    )
    with open(".env", "w") as f:
        f.write(txt.strip())
    print("Succesfully Generated .env File Don't Forget To Save It! For Future Uses.")


async def auto_maker():
    string_session, api_id, api_hash = await generate_session_string()
    print(string_session)
    async with TelegramClient(
        StringSession(string_session), api_id, api_hash
    ) as client:
        print("Creating Bot Account...")
        who = await client.get_me()
        DATA["owner_id"] = who.id
        name = who.first_name + "'s Auto Anime Bot"
        if who.username:
            username = who.username + "_anime_bot"
        else:
            username = "ongoing_anime_" + (str(who.id))[5:] + "_bot"
        bf = "@BotFather"
        await client(UnblockRequest(bf))
        await client.send_message(bf, "/cancel")
        await asyncio.sleep(1)
        await client.send_message(bf, "/newbot")
        await asyncio.sleep(1)
        isdone = (await client.get_messages(bf, limit=1))[0].text
        if isdone.startswith("That I cannot do.") or "20 bots" in isdone:
            print(
                "You Already Made 20 Bots In Your Current Account. You Have To Deleted One Bot To Run This Script."
            )
            sys.exit(1)
        await client.send_message(bf, name)
        await asyncio.sleep(1)
        isdone = (await client.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            print(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            sys.exit(1)
        await client.send_message(bf, username)
        await asyncio.sleep(1)
        isdone = (await client.get_messages(bf, limit=1))[0].text
        await client.send_read_acknowledge("botfather")
        if isdone.startswith("Sorry,"):
            ran = random.randint(1, 100)
            username = "ongoing_anime_" + (str(who.id))[6:] + str(ran) + "_bot"
            await client.send_message(bf, username)
            await asyncio.sleep(1)
            isdone = (await client.get_messages(bf, limit=1))[0].text
        if isdone.startswith("Done!"):
            bot_token = isdone.split("`")[1]
            DATA["bot_token"] = bot_token
            print("Succesfully Created Bot Account...")
        print("Creating Channels...")
        for ch_name in [
            "Ongoing Anime Logs",
            "Ongoing Anime 2024",
            "Ongoing Anime Samples And SS",
            "Ongoing Anime Backup",
        ]:
            try:
                chat_id = await create_channel(client, ch_name)
                await asyncio.sleep(3)
                await client.edit_admin(
                    int(chat_id),
                    username,
                    post_messages=True,
                    edit_messages=True,
                    delete_messages=True,
                    ban_users=True,
                    pin_messages=True,
                    add_admins=True,
                )
                DATA[ch_name] = chat_id
            except BaseException:
                print("Error While Creating Channel And Promoting Bot..")
                print(format_exc())
                sys.exit(1)
        print("Succesfully Created Channel...")
        db = get_firebase()
        if not db:
            print(
                "Generating .env Without Firebase URI and Service Account. Now You Have To Add it Manually!"
            )
        generate_env()


asyncio.run(auto_maker())
