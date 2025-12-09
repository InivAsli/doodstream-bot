from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    @staticmethod
    def main_menu():
        keyboard = [
            [InlineKeyboardButton("📁 My Videos", callback_data="list_videos_1")],
            [InlineKeyboardButton("📤 Upload Video", callback_data="upload_menu")],
            [InlineKeyboardButton("📊 Account Stats", callback_data="account_stats")],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def upload_menu():
        keyboard = [
            [InlineKeyboardButton("📁 Upload File", callback_data="upload_file")],
            [InlineKeyboardButton("🔗 Upload from URL", callback_data="upload_url")],
            [InlineKeyboardButton("◀️ Back", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def video_pagination(current_page, total_pages):
        keyboard = []
        
        if current_page > 1:
            keyboard.append([
                InlineKeyboardButton("◀️ Previous", callback_data=f"list_videos_{current_page-1}")
            ])
        
        keyboard.append([
            InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="current_page")
        ])
        
        if current_page < total_pages:
            keyboard.append([
                InlineKeyboardButton("Next ▶️", callback_data=f"list_videos_{current_page+1}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("🔼 Upload New", callback_data="upload_menu"),
            InlineKeyboardButton("🔄 Refresh", callback_data=f"list_videos_{current_page}")
        ])
        
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_main():
        return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]])
    
    @staticmethod
    def cancel_button():
        return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]])

keyboards = Keyboards()
