from aiogram.types import (
	ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton,
	KeyboardButton
)

register_kb = ReplyKeyboardMarkup( 
	keyboard=[
		[KeyboardButton(text="Ro'yxatdan O'tish")]
	],resize_keyboard=True
)


phoneNumber_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="📞 Telefon raqam ulashish",request_contact=True)]
	],resize_keyboard=True
)

menu_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="📋 Menu")],
    [KeyboardButton(text="🛒 Order")],
    [KeyboardButton(text="📞 Contact")]
	],resize_keyboard=True
)


after_menukb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔎 Search"), KeyboardButton(text="📚 All")],
        [KeyboardButton(text="💸 Discount"), KeyboardButton(text="🆕 New")],
        [KeyboardButton(text="⬅️ Back")]
    ],
    resize_keyboard=True
)


send_toAdminkb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="Yuborish")]
	],resize_keyboard=True
)

all_kb = ReplyKeyboardMarkup (
	keyboard= [
		[KeyboardButton(text="⬅️ back"), KeyboardButton(text="📋 Main menu")]
	],resize_keyboard=True
)

order_kb = ReplyKeyboardMarkup(
    keyboard=[
		[KeyboardButton(text="⬅️ Back")]
	],resize_keyboard=True
)

order_inline_kb = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="➕", callback_data="add"),
			InlineKeyboardButton(text="1", callback_data="one"),
			InlineKeyboardButton(text="➖", callback_data="subtract")
		]
	]
)