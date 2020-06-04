#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random, re, io, asyncio
from PIL import Image
from io import BytesIO
from spongemock import spongemock
from zalgo_text import zalgo
from deeppyer import deepfry
import os
from pathlib import Path
import glob

from typing import List
from telegram import Update, Bot, ParseMode, Message
from telegram.ext import run_async

from haruka import dispatcher, DEEPFRY_TOKEN, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.tr_engine.strings import tld, tld_list

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    faces = [
        '(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', '\(^o\) (/o^)/',
        '( ^ _ ^)∠☆', '(ô_ô)', '~:o', ';____;', '(*^*)', '(>_', '(♥_♥)',
        '*(^O^)*', '((+_+))'
    ]
    reply_text = re.sub(r'[rl]', "w", data)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", data)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), data)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = str(data).translate(WIDE_MAP)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv


@run_async
def mafiatext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/mafia.jpg').is_file():
        LOGGER.warning(
            "images/mafia.jpg not found! Mafia memes module is turned off!")
        return

    for mocked in glob.glob("images/mafiaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/mafia.jpg -font Impact -pointsize 50 -size 1280x720 -stroke white -strokewidth 1 -fill black -background none -gravity north caption:"{}" -flatten images/mafiaed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/mafiaed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/mafiaed{}.jpg'.format(randint))


@run_async
def pidortext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/4pda.jpg').is_file():
        LOGGER.warning(
            "images/4pda.jpg not found! Pidor memes module is turned off!")
        return
    for mocked in glob.glob("images/4pdaed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/4pda.jpg -font Impact -pointsize 50 -size 400x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/4pdaed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/4pdaed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/4pdaed{}.jpg'.format(randint))


@run_async
def kimtext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/kim.jpg').is_file():
        LOGGER.warning(
            "images/kim.jpg not found! Kim memes module is turned off!")
        return
    for mocked in glob.glob("kimed*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/kim.jpg -font Impact -pointsize 50 -size 480x360 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/kimed{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/kimed{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/kimed{}.jpg'.format(randint))


@run_async
def hitlertext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/hitler.jpg').is_file():
        LOGGER.warning(
            "images/hitler.jpg not found! Hitler memes module is turned off!")
        return
    for mocked in glob.glob("images/hitlered*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/hitler.jpg -font Impact -pointsize 50 -size 615x409 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/hitlered{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/hitlered{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/hitlered{}.jpg'.format(randint))


@run_async
def spongemocktext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    if not Path('images/bob.jpg').is_file():
        LOGGER.warning(
            "images/bob.jpg not found! Spongemock memes module is turned off!")
        return
    for mocked in glob.glob("images/mocked*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert images/bob.jpg -font Impact -pointsize 30 -size 512x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten images/mocked{}.jpg""".format(
        reply_text, randint)
    os.system(magick)
    with open('images/mocked{}.jpg'.format(randint), 'rb') as mockedphoto:
        if noreply:
            message.reply_photo(photo=mockedphoto,
                                reply=message.reply_to_message)
        else:
            message.reply_to_message.reply_photo(
                photo=mockedphoto, reply=message.reply_to_message)
    os.remove('images/mocked{}.jpg'.format(randint))


@run_async
def zalgotext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = zalgo.zalgo().zalgofy(data)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text(tld(chat.id, "memes_deepfry_nothing"))
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        process_deepfry(image, message.reply_to_message, bot))
    loop.close()


async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(img=image,
                          token=DEEPFRY_TOKEN,
                          url_base='westeurope')

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")


# shitty maymay modules made by @divadsn ^^^


@run_async
def shout(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        data = " ".join(args)
    else:
        data = tld(chat.id, "memes_no_message")

    msg = "```"
    result = []
    result.append(' '.join([s for s in data]))
    for pos, symbol in enumerate(data[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = data[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


@run_async
def insults(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    text = random.choice(tld_list(chat.id, "memes_insults_list"))

    if message.reply_to_message:
        message.reply_to_message.reply_text(text)
    else:
        message.reply_text(text)


@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat
    update.effective_message.reply_text(
        random.choice(tld_list(chat.id, "memes_runs_list")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    msg = update.effective_message

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                                   msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username == "RealAkito":
            reply_text(tld(chat.id, "memes_not_doing_that"))
            return
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld_list(chat.id, "memes_slaps_templates_list"))
    item = random.choice(tld_list(chat.id, "memes_items_list"))
    hit = random.choice(tld_list(chat.id, "memes_hit_list"))
    throw = random.choice(tld_list(chat.id, "memes_throw_list"))
    itemp = random.choice(tld_list(chat.id, "memes_items_list"))
    itemr = random.choice(tld_list(chat.id, "memes_items_list"))

    repl = temp.format(user1=user1,
                       user2=user2,
                       item=item,
                       hits=hit,
                       throws=throw,
                       itemp=itemp,
                       itemr=itemr)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


__help__ = True

OWO_HANDLER = DisableAbleCommandHandler("owo",
                                        owo,
                                        admin_ok=True,
                                        pass_args=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch, pass_args=True)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor",
                                          vapor,
                                          pass_args=True,
                                          admin_ok=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock",
                                         spongemocktext,
                                         admin_ok=True,
                                         pass_args=True)
KIM_HANDLER = DisableAbleCommandHandler("kim",
                                        kimtext,
                                        admin_ok=True,
                                        pass_args=True)
MAFIA_HANDLER = DisableAbleCommandHandler("mafia",
                                          mafiatext,
                                          admin_ok=True,
                                          pass_args=True)
PIDOR_HANDLER = DisableAbleCommandHandler("pidor",
                                          pidortext,
                                          admin_ok=True,
                                          pass_args=True)
HITLER_HANDLER = DisableAbleCommandHandler("hitler",
                                           hitlertext,
                                           admin_ok=True,
                                           pass_args=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext, pass_args=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry",
                                            deepfryer,
                                            admin_ok=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
INSULTS_HANDLER = DisableAbleCommandHandler("insults", insults, admin_ok=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap",
                                         slap,
                                         pass_args=True,
                                         admin_ok=True)

dispatcher.add_handler(MAFIA_HANDLER)
dispatcher.add_handler(PIDOR_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(KIM_HANDLER)
dispatcher.add_handler(HITLER_HANDLER)
dispatcher.add_handler(INSULTS_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
n", "yes"):
        sql.set_clean_welcome(str(chat.id), True)
        update.effective_message.reply_text("I'll try to delete old welcome messages!")
        return "<b>{}:</b>" \
               "\n#CLEAN_WELCOME" \
               "\n<b>Admin:</b> {}" \
               "\nHas toggled clean welcomes to <code>ON</code>.".format(html.escape(chat.title),
                                                                         mention_html(user.id, user.first_name))
    elif args[0].lower() in ("off", "no"):
        sql.set_clean_welcome(str(chat.id), False)
        update.effective_message.reply_text("I won't delete old welcome messages.")
        return "<b>{}:</b>" \
               "\n#CLEAN_WELCOME" \
               "\n<b>Admin:</b> {}" \
               "\nHas toggled clean welcomes to <code>OFF</code>.".format(html.escape(chat.title),
                                                                          mention_html(user.id, user.first_name))
    else:
        # idek what you're writing, say yes or no
        update.effective_message.reply_text("I understand 'on/yes' or 'off/no' only!")
        return ""


@run_async
@user_admin
def security(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    if len(args) >= 1:
        var = args[0]
        print(var)
        if (var == "no" or var == "off"):
            sql.set_welcome_security(chat.id, False)
            update.effective_message.reply_text("Disabled welcome security")
        elif(var == "soft"):
            sql.set_welcome_security(chat.id, "soft")
            update.effective_message.reply_text("I will restrict user's permission to send media for 24 hours")
        elif(var == "hard"):
            sql.set_welcome_security(chat.id, "hard")
            update.effective_message.reply_text("New users will be muted if they do not click on the button")
        else:
            update.effective_message.reply_text("Please enter `off`/`no`/`soft`/`hard`!", parse_mode=ParseMode.MARKDOWN)
    else:
        status = sql.welcome_security(chat.id)
        update.effective_message.reply_text(status)


@run_async
@user_admin
def cleanservice(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    if chat.type != chat.PRIVATE:
        if len(args) >= 1:
            var = args[0]
            print(var)
            if (var == "no" or var == "off"):
                sql.set_clean_service(chat.id, False)
                update.effective_message.reply_text("I'll leave service messages")
            elif(var == "yes" or var == "on"):
                sql.set_clean_service(chat.id, True)
                update.effective_message.reply_text("I will clean service messages")
            else:
                update.effective_message.reply_text("Please enter yes or no!", parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text("Please enter yes or no!", parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Please enter yes or no in your group!", parse_mode=ParseMode.MARKDOWN)


# TODO: get welcome data from group butler snap
# def __import_data__(chat_id, data):
#     welcome = data.get('info', {}).get('rules')
#     welcome = welcome.replace('$username', '{username}')
#     welcome = welcome.replace('$name', '{fullname}')
#     welcome = welcome.replace('$id', '{id}')
#     welcome = welcome.replace('$title', '{chatname}')
#     welcome = welcome.replace('$surname', '{lastname}')
#     welcome = welcome.replace('$rules', '{rules}')
#     sql.set_custom_welcome(chat_id, welcome, sql.Types.TEXT)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(bot, update, chat, chatP, user):
    chat_id = chat.id
    welcome_pref, _, _ = sql.get_welc_pref(chat_id)
    goodbye_pref, _, _ = sql.get_gdbye_pref(chat_id)
    return "This chat has it's welcome preference set to `{}`.\n" \
           "It's goodbye preference is `{}`.".format(welcome_pref, goodbye_pref)


__help__ = """
Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

Available commands are:
 - /welcome <on/off/yes/no>: enables/disables welcome messages. If no option is given, returns the current welcome message and welcome settings. 
 - /goodbye <on/off/yes/no>: enables/disables goodbye messages. If no option is given, returns  the current goodbye message and goodbye settings.
 - /setwelcome <message>: sets your new welcome message! Markdown and buttons are supported, as well as fillings.
 - /resetwelcome: resets your welcome message to default; deleting any changes you've made.
 - /setgoodbye <message>: sets your new goodbye message! Markdown and buttons are supported, as well as fillings.
 - /resetgoodbye: resets your goodbye message to default; deleting any changes you've made.
 - /cleanwelcome <on/off/yes/no>: deletes old welcome messages; when a new person joins, the old message is deleted.
 - /cleanservice <on/off/yes/no>: deletes all service message; those are the annoying "x joined the group" you see when people join.
 - /welcomesecurity <off/soft/hard>: soft - restrict user's permission to send media files for 24 hours, hard - restict user's permission to send messages until they click on the button \"I'm not a bot\"


Fillings:
As mentioned, you can use certain tags to fill in your welcome message with user or chat info; there are:
{first}: The user's first name.
{last}: The user's last name.
{fullname}: The user's full name.
{username}: The user's username; if none is available, mentions the user.
{mention}: Mentions the user, using their firstname.
{id}: The user's id.
{chatname}: The chat's name.

An example of how to use fillings would be to set your welcome, via:
/setwelcome Hey there {first}! Welcome to {chatname}.

You can enable/disable welcome messages as such:
/welcome off

If you want to save an image, gif, or sticker, or any other data, do the following:
/setwelcome while replying to a sticker or whatever data you'd like. This data will now be sent to welcome new users.

Tip: use /welcome noformat to retrieve the unformatted welcome message.
This will retrieve the welcome message and send it without formatting it; getting you the raw markdown, allowing you to make easy edits.
This also works with /goodbye.
"""


__mod_name__ = "Welcomes/Goodbyes"

NEW_MEM_HANDLER = MessageHandler(Filters.status_update.new_chat_members, new_member)
LEFT_MEM_HANDLER = MessageHandler(Filters.status_update.left_chat_member, left_member)
WELC_PREF_HANDLER = CommandHandler("welcome", welcome, pass_args=True, filters=Filters.group)
GOODBYE_PREF_HANDLER = CommandHandler("goodbye", goodbye, pass_args=True, filters=Filters.group)
SET_WELCOME = CommandHandler("setwelcome", set_welcome, filters=Filters.group)
SET_GOODBYE = CommandHandler("setgoodbye", set_goodbye, filters=Filters.group)
RESET_WELCOME = CommandHandler("resetwelcome", reset_welcome, filters=Filters.group)
RESET_GOODBYE = CommandHandler("resetgoodbye", reset_goodbye, filters=Filters.group)
CLEAN_WELCOME = CommandHandler("cleanwelcome", clean_welcome, pass_args=True, filters=Filters.group)

SECURITY_HANDLER = CommandHandler("welcomesecurity", security, pass_args=True, filters=Filters.group)
CLEAN_SERVICE_HANDLER = CommandHandler("cleanservice", cleanservice, pass_args=True, filters=Filters.group)

help_callback_handler = CallbackQueryHandler(check_bot_button, pattern=r"check_bot_")

dispatcher.add_handler(NEW_MEM_HANDLER)
dispatcher.add_handler(LEFT_MEM_HANDLER)
dispatcher.add_handler(WELC_PREF_HANDLER)
dispatcher.add_handler(GOODBYE_PREF_HANDLER)
dispatcher.add_handler(SET_WELCOME)
dispatcher.add_handler(SET_GOODBYE)
dispatcher.add_handler(RESET_WELCOME)
dispatcher.add_handler(RESET_GOODBYE)
dispatcher.add_handler(CLEAN_WELCOME)
dispatcher.add_handler(SECURITY_HANDLER)
dispatcher.add_handler(CLEAN_SERVICE_HANDLER)

dispatcher.add_handler(help_callback_handler)
