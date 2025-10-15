from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from database import is_admin, add_book, get_all_books, get_book_by_id, update_book, delete_book, get_all_users
from buttons import adminmenu_kb, menu_kb, book_management_kb, back_kb, get_book_inline_kb
from states.admin import BookAdd, BookEdit
from aiogram.fsm.context import FSMContext

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_handler(message: Message):
	if is_admin(message.from_user.id) or message.from_user.id == 776560887:
		await message.answer("👑 Admin paneliga xush kelibsiz!\n\nQuyidagi variantlardan birini tanlang:", reply_markup=adminmenu_kb)
	else:
		await message.answer("⛔ Sizda admin huquqi yo‘q.")

@admin_router.message(Command("user"))
async def get_user(message:Message):
	await message.answer("Userga qaytdingiz", reply_markup=menu_kb)

@admin_router.message(F.text == "📚 Kitoblar boshqaruvi")
async def book_management(message: Message):
	await message.answer("📚 Kitoblar boshqaruvi menyusi:\n\nQuyidagi amallardan birini tanlang:", reply_markup=book_management_kb)

@admin_router.message(F.text == "➕ Kitob qo'shish")
async def add_book_start(message: Message, state: FSMContext):
	await state.set_state(BookAdd.title)
	await message.answer("📖 Yangi kitob qo'shish\n\nKitob nomini kiriting:", reply_markup=back_kb)

@admin_router.message(BookAdd.title)
async def add_book_title(message: Message, state: FSMContext):
	await state.update_data(title=message.text)
	await state.set_state(BookAdd.description)
	await message.answer("📝 Kitob tavsifini kiriting:")

@admin_router.message(BookAdd.description)
async def add_book_description(message: Message, state: FSMContext):
	await state.update_data(description=message.text)
	await state.set_state(BookAdd.author)
	await message.answer("👤 Muallif nomini kiriting:")

@admin_router.message(BookAdd.author)
async def add_book_author(message: Message, state: FSMContext):
	await state.update_data(author=message.text)
	await state.set_state(BookAdd.price)
	await message.answer("💰 Narxini kiriting (faqat raqamlar):")

@admin_router.message(BookAdd.price)
async def add_book_price(message: Message, state: FSMContext):
	try:
		price = int(message.text)
		await state.update_data(price=price)
		await state.set_state(BookAdd.genre)
		await message.answer("Janrini kiriting:")
	except ValueError:
		await message.answer("❌ Narx faqat raqam bo'lishi kerak!")

@admin_router.message(BookAdd.genre)
async def add_book_genre(message: Message, state: FSMContext):
	await state.update_data(genre=message.text)
	await state.set_state(BookAdd.quantity)
	await message.answer("📦 Miqdorini kiriting (faqat raqamlar):")

@admin_router.message(BookAdd.quantity)
async def add_book_quantity(message: Message, state: FSMContext):
	try:
		quantity = int(message.text)
		data = await state.get_data()
		book_id = add_book(
			data['title'],
			data['description'],
			data['author'],
			data['price'],
			data['genre'],
			quantity
		)
		if book_id:
			await message.answer(f"✅ Kitob muvaffaqiyatli qo'shildi!\n\nID: {book_id}", reply_markup=book_management_kb)
		else:
			await message.answer("❌ Kitob qo'shishda xatolik yuz berdi!", reply_markup=book_management_kb)
		await state.clear()
	except ValueError:
		await message.answer("❌ Miqdor faqat raqam bo'lishi kerak!")

@admin_router.message(F.text == "📋 Barcha kitoblar")
async def list_books(message: Message):
	books = get_all_books()
	if not books:
		await message.answer("📚 Hozircha kitoblar yo'q.", reply_markup=book_management_kb)
		return

	response = "📚 Barcha kitoblar:\n\n"
	for book in books:
		response += f"🆔 {book[0]}\n📖 {book[1]}\n👤 {book[3]}\n💰 {book[4]} so'm\n📦 {book[6]} dona\n\n"
	await message.answer(response, reply_markup=book_management_kb)

@admin_router.message(F.text == "✏️ Kitobni tahrirlash")
async def edit_book_start(message: Message, state: FSMContext):
	books = get_all_books()
	if not books:
		await message.answer("📚 Tahrirlash uchun kitoblar yo'q.", reply_markup=book_management_kb)
		return

	response = "✏️ Qaysi kitobni tahrirlamoqchisiz?\n\n"
	for book in books:
		response += f"🆔 {book[0]} - 📖 {book[1]}\n"
	response += "\nKitob ID sini kiriting:"
	await state.set_state(BookEdit.book_id)
	await message.answer(response, reply_markup=back_kb)

@admin_router.message(BookEdit.book_id)
async def edit_book_get_id(message: Message, state: FSMContext):
	try:
		book_id = int(message.text)
		book = get_book_by_id(book_id)
		if not book:
			await message.answer("❌ Bunday ID li kitob topilmadi!", reply_markup=book_management_kb)
			await state.clear()
			return

		await state.update_data(book_id=book_id, title=book[1], description=book[2], author=book[3], price=book[4], genre=book[5], quantity=book[6])
		await state.set_state(BookEdit.title)
		await message.answer(f"📖 Joriy nom: {book[1]}\n\nYangi nomni kiriting (yoki o'zgarishsiz qoldirish uchun '-' kiriting):")
	except ValueError:
		await message.answer("❌ ID faqat raqam bo'lishi kerak!")

@admin_router.message(BookEdit.title)
async def edit_book_title(message: Message, state: FSMContext):
	title = message.text if message.text != "-" else None
	await state.update_data(title=title)
	await state.set_state(BookEdit.description)
	data = await state.get_data()
	current_desc = data.get('description', '')
	await message.answer(f"📝 Joriy tavsif: {current_desc}\n\nYangi tavsifni kiriting (yoki o'zgarishsiz qoldirish uchun '-' kiriting):")

@admin_router.message(BookEdit.description)
async def edit_book_description(message: Message, state: FSMContext):
	description = message.text if message.text != "-" else None
	await state.update_data(description=description)
	await state.set_state(BookEdit.author)
	data = await state.get_data()
	current_author = data.get('author', '')
	await message.answer(f"👤 Joriy muallif: {current_author}\n\nYangi muallifni kiriting (yoki o'zgarishsiz qoldirish uchun '-' kiriting):")

@admin_router.message(BookEdit.author)
async def edit_book_author(message: Message, state: FSMContext):
	author = message.text if message.text != "-" else None
	await state.update_data(author=author)
	await state.set_state(BookEdit.price)
	data = await state.get_data()
	current_price = data.get('price', 0)
	await message.answer(f"💰 Joriy narx: {current_price}\n\nYangi narxni kiriting (faqat raqamlar, o'zgarishsiz qoldirish uchun '-' kiriting):")

@admin_router.message(BookEdit.price)
async def edit_book_price(message: Message, state: FSMContext):
	if message.text == "-":
		price = None
	else:
		try:
			price = int(message.text)
		except ValueError:
			await message.answer("❌ Narx faqat raqam bo'lishi kerak!")
			return
	await state.update_data(price=price)
	await state.set_state(BookEdit.genre)
	data = await state.get_data()
	current_genre = data.get('genre', '')
	await message.answer(f"Joriy janr: {current_genre}\n\nYangi janrni kiriting (yoki o'zgarishsiz qoldirish uchun '-' kiriting):")

@admin_router.message(BookEdit.genre)
async def edit_book_genre(message: Message, state: FSMContext):
	genre = message.text if message.text != "-" else None
	await state.update_data(genre=genre)
	await state.set_state(BookEdit.quantity)
	data = await state.get_data()
	current_quantity = data.get('quantity', 0)
	await message.answer(f"📦 Joriy miqdor: {current_quantity}\n\nYangi miqdorni kiriting (faqat raqamlar, o'zgarishsiz qoldirish uchun '-' kiriting):")

@admin_router.message(BookEdit.quantity)
async def edit_book_quantity(message: Message, state: FSMContext):
	if message.text == "-":
		quantity = None
	else:
		try:
			quantity = int(message.text)
		except ValueError:
			await message.answer("❌ Miqdor faqat raqam bo'lishi kerak!")
			return

	data = await state.get_data()
	update_data = {}
	if data.get('title') is not None:
		update_data['title'] = data['title']
	else:
		update_data['title'] = data.get('title', '')
	if data.get('description') is not None:
		update_data['description'] = data['description']
	else:
		update_data['description'] = data.get('description', '')
	if data.get('author') is not None:
		update_data['author'] = data['author']
	else:
		update_data['author'] = data.get('author', '')
	if data.get('price') is not None:
		update_data['price'] = data['price']
	else:
		update_data['price'] = data.get('price', 0)
	if data.get('genre') is not None:
		update_data['genre'] = data['genre']
	else:
		update_data['genre'] = data.get('genre', '')
	if quantity is not None:
		update_data['quantity'] = quantity
	else:
		update_data['quantity'] = data.get('quantity', 0)

	success = update_book(
		data['book_id'],
		update_data['title'],
		update_data['description'],
		update_data['author'],
		update_data['price'],
		update_data['genre'],
		update_data['quantity']
	)

	if success:
		await message.answer("✅ Kitob muvaffaqiyatli yangilandi!", reply_markup=book_management_kb)
	else:
		await message.answer("❌ Kitobni yangilashda xatolik yuz berdi!", reply_markup=book_management_kb)
	await state.clear()

@admin_router.message(F.text == "🗑️ Kitobni o'chirish")
async def delete_book_start(message: Message, state: FSMContext):
	books = get_all_books()
	if not books:
		await message.answer("📚 O'chirish uchun kitoblar yo'q.", reply_markup=book_management_kb)
		return

	response = "🗑️ Qaysi kitobni o'chirmoqchisiz?\n\n"
	for book in books:
		response += f"🆔 {book[0]} - 📖 {book[1]}\n"
	response += "\nKitob ID sini kiriting:"
	await state.set_state("delete_book_id")
	await message.answer(response, reply_markup=back_kb)

@admin_router.message(F.text.regexp(r'^\d+$'))
async def delete_book_confirm(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state == "delete_book_id":
		try:
			book_id = int(message.text)
			book = get_book_by_id(book_id)
			if not book:
				await message.answer("❌ Bunday ID li kitob topilmadi!", reply_markup=book_management_kb)
				await state.clear()
				return

			success = delete_book(book_id)
			if success:
				await message.answer(f"✅ Kitob '{book[1]}' muvaffaqiyatli o'chirildi!", reply_markup=book_management_kb)
			else:
				await message.answer("❌ Kitobni o'chirishda xatolik yuz berdi!", reply_markup=book_management_kb)
			await state.clear()
		except ValueError:
			await message.answer("❌ ID faqat raqam bo'lishi kerak!")

@admin_router.message(F.text == "👥 Foydalanuvchilarni ko'rish")
async def view_users(message: Message):
	users = get_all_users()
	if not users:
		await message.answer("👥 Hozircha foydalanuvchilar yo'q.", reply_markup=adminmenu_kb)
		return

	response = "👥 Barcha foydalanuvchilar:\n\n"
	for user in users:
		admin_status = "👑 Admin" if user[6] else "👤 User"
		active_status = "✅ Faol" if user[5] else "❌ Nofaol"
		response += f"🆔 {user[0]}\n👤 {user[2]}\n📞 {user[3]}\n@{user[4] or 'Noma\'lum'}\n{admin_status} | {active_status}\n\n"
	await message.answer(response, reply_markup=adminmenu_kb)

@admin_router.message(F.text == "⬅️ Orqaga")
async def back_to_admin_menu(message: Message, state: FSMContext):
	await state.clear()
	await message.answer("👑 Admin paneliga qaytdingiz:", reply_markup=adminmenu_kb)