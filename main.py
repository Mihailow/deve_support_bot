from handlers.user_handlers import *
from handlers.manager_handlers import *
from handlers.admin_handlers import *
# from handlers.mailing_handlers import *
from handlers.all_handlers import *

from mailingsSystems import check_file_type, AlbumMiddleware

if __name__ == "__main__":
    scheduler.start()
    scheduler.add_job(del_new_appeals_without_category, "interval", minutes=30)
    scheduler.add_job(resend_new_appeals, "interval", minutes=30)
    scheduler.add_job(notice_old_appeals, "interval", minutes=30)
    scheduler.add_job(send_message_to_user, "interval", seconds=10)
    scheduler.add_job(change_settings_from_website, "interval", seconds=10)
    executor.start_polling(dp, skip_updates=True)
