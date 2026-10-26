from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from nova.runtime.router import ModelRouter
from nova.runtime.workspace import PersonaWorkspace

def build_bot(token: str, allowlist: set[int], router: ModelRouter, workspace: PersonaWorkspace):
    app = Application.builder().token(token).build()
    async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        incoming, user = update.effective_message, update.effective_user
        if incoming is None or user is None or not incoming.text or user.id not in allowlist:
            return
        reply = await router.complete(workspace.system_prompt(), incoming.text)
        await incoming.reply_text(reply.content)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    return app