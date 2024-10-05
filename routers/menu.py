from textwrap import dedent
from aiogram import Router, F, types
from aiogram.filters import Command

menu = Router()


@menu.message(Command('admin'))
async def admin_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Создать рассылку")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите команду", reply_markup=keyboard)


@menu.message(Command('start'))
async def start_command(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="✨Start Farming✨", url="https://t.me/ton1moonBot/app?startapp")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    text = dedent("""
        Welcome to Moon App — your gateway to the future of reward-based farming! 🚀🌕

        We’re building a platform where you can engage in smart giveaways, earning points through tasks, inviting friends, and competing for exciting rewards. With Moon App, you don’t just wait for luck — you work your way to the top.

        Here’s what you can do right now:
        💯 Farm MOON Points: Collect your points daily and watch your rewards grow
        👾 Launch Shuttles: Use NFT shuttles to multiply your farming speed
        🌠 Invite Friends: Earn 10% from your friends' points and 2.5% from their referrals

        Start farming MOON today, and reach the stars with Moon App! 🌟
    """)

    await message.answer(text, reply_markup=keyboard)


@menu.message(F.text.casefold() == "menu")
async def menu_command(message: types.Message):
    await message.answer(
        text="Вы вернулись в главное меню",
    )
