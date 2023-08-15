import polib


def get_text(msgid: str, language: str = "us") -> str:
    po_file = polib.pofile(f"bot/locales/texts/{language.lower()}/messages.po")

    entry = po_file.find(msgid)

    if entry:
        return entry.msgstr

    return msgid
