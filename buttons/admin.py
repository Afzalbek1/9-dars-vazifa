from aiogram.types import (
	ReplyKeyboardMarkup, ReplyKeyboardRemove,
	KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
)

adminmenu_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="📚 Kitoblar boshqaruvi")],
		[KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")],
		[KeyboardButton(text="⬅️ Orqaga")]
	],resize_keyboard=True
)

book_management_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="➕ Kitob qo'shish")],
		[KeyboardButton(text="📋 Barcha kitoblar")],
		[KeyboardButton(text="✏️ Kitobni tahrirlash")],
		[KeyboardButton(text="🗑️ Kitobni o'chirish")],
		[KeyboardButton(text="⬅️ Orqaga")]
	],resize_keyboard=True
)

back_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="⬅️ Orqaga")]
	],resize_keyboard=True
)

# Inline keyboards for book actions
def get_book_inline_kb(book_id):
	return InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"edit_book_{book_id}")],
			[InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_book_{book_id}")]
		]
	)