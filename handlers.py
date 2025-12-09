from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import config
from keyboards import keyboards
from doodstream_api import dood_api

class Handlers:
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        welcome_text = f"""
👋 *Welcome to DoodStream Bot!*

Hello {user.first_name}!

*Features Available:*
• 📁 List all your videos
• 📤 Upload via URL
• 📊 View account statistics
• 🔗 Get download links

Use buttons below to get started!
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.main_menu()
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "main_menu":
            await query.edit_message_text(
                "🏠 *Main Menu*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboards.main_menu()
            )
        
        elif data.startswith("list_videos_"):
            page = int(data.split("_")[2])
            await self.show_videos(query, page)
        
        elif data == "upload_menu":
            await query.edit_message_text(
                "📤 *Upload Options*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboards.upload_menu()
            )
        
        elif data == "account_stats":
            await self.show_stats(query)
        
        elif data == "upload_url":
            await self.request_url_upload(query, context)
        
        elif data == "help":
            await self.show_help(query)
    
    async def show_videos(self, query, page=1):
        await query.edit_message_text(
            "📁 *Loading your videos...*",
            parse_mode=ParseMode.MARKDOWN
        )
        
        result = dood_api.list_files(page)
        
        if "result" in result and "files" in result["result"]:
            videos = result["result"]["files"]
            total_files = result["result"].get("total_files", 0)
            total_pages = (total_files + config.ITEMS_PER_PAGE - 1) // config.ITEMS_PER_PAGE
            
            if not videos:
                await query.edit_message_text(
                    "📭 *No videos found!*",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📤 Upload Video", callback_data="upload_menu")],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
                    ])
                )
                return
            
            text = f"📁 *Your Videos*\n\n"
            text += f"*Total:* {total_files} videos\n"
            text += f"*Page:* {page} of {total_pages}\n\n"
            
            for i, video in enumerate(videos, 1):
                title = video.get('title', 'Untitled')[:35]
                size = self._format_size(video.get('size', 0))
                views = video.get('views', 0)
                text += f"{i}. *{title}*\n"
                text += f"   📦 {size} | 👁️ {views} views\n"
            
            await query.edit_message_text(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboards.video_pagination(page, total_pages)
            )
        else:
            await query.edit_message_text(
                "❌ *Error loading videos!*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboards.back_to_main()
            )
    
    async def show_stats(self, query):
        await query.edit_message_text(
            "📊 *Loading account statistics...*",
            parse_mode=ParseMode.MARKDOWN
        )
        
        stats = dood_api.get_account_stats()
        info = dood_api.get_account_info()
        
        if "result" in stats and "result" in info:
            stats_result = stats["result"]
            info_result = info["result"]
            
            text = "📊 *Account Statistics*\n\n"
            
            text += "*👤 Account Info:*\n"
            text += f"• Email: {info_result.get('email', 'N/A')}\n"
            text += f"• Balance: ${info_result.get('balance', '0')}\n"
            text += f"• Storage: {info_result.get('storage_used', '0')}\n\n"
            
            text += "*📈 Statistics:*\n"
            text += f"• Total Views: {stats_result.get('total_views', '0')}\n"
            text += f"• Total Files: {stats_result.get('total_files', '0')}\n"
            text += f"• Total Earnings: ${stats_result.get('total_earning', '0')}"
            
            await query.edit_message_text(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Refresh", callback_data="account_stats")],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
                ])
            )
        else:
            await query.edit_message_text(
                "❌ *Error loading statistics!*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboards.back_to_main()
            )
    
    async def request_url_upload(self, query, context):
        await query.edit_message_text(
            "🔗 *Upload from URL*\n\nPlease send me the direct video URL.\n\n"
            "*Example:* https://example.com/video.mp4\n\n"
            "Or press cancel to go back.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.cancel_button()
        )
        
        # Set state for URL upload
        context.user_data['waiting_for_url'] = True
    
    async def handle_url_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get('waiting_for_url'):
            url = update.message.text.strip()
            
            if not url.startswith(('http://', 'https://')):
                await update.message.reply_text("❌ Please send a valid URL")
                return
            
            await update.message.reply_text("📤 *Uploading...*", parse_mode=ParseMode.MARKDOWN)
            
            try:
                result = dood_api.upload_from_url(url)
                
                if result.get("msg") == "OK":
                    file_code = result["result"][0].get("filecode")
                    
                    success_msg = f"✅ *Upload Successful!*\n\n*File Code:* `{file_code}`"
                    
                    context.user_data['waiting_for_url'] = False
                    
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📁 View Videos", callback_data="list_videos_1")],
                        [InlineKeyboardButton("📤 Upload Another", callback_data="upload_menu")]
                    ])
                    
                    await update.message.reply_text(
                        success_msg,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=keyboard
                    )
                else:
                    error_msg = result.get("msg", "Unknown error")
                    await update.message.reply_text(f"❌ Upload failed: {error_msg}")
                    context.user_data['waiting_for_url'] = False
                    
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {str(e)}")
                context.user_data['waiting_for_url'] = False
    
    async def show_help(self, query):
        help_text = """
🆘 *DoodStream Bot Help*

*Features:*
• 📁 View all your videos
• 📤 Upload via direct URL
• 📊 Check account statistics

*How to use:*
1. Use buttons for navigation
2. For URL upload, send direct video link
3. Check stats anytime

*Note:* Processing may take 1-5 minutes.
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboards.back_to_main()
        )
    
    @staticmethod
    def _format_size(size_bytes):
        if size_bytes == 0:
            return "0 B"
        
        size_names = ("B", "KB", "MB", "GB")
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"

handlers = Handlers()
