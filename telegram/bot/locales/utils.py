import polib


def get_text(msgid: str, language: str = "us", **format) -> str:
    po_file = polib.pofile(f"bot/locales/texts/{language.lower()}/messages.po")

    entry = po_file.find(msgid)

    if entry:
        if format:
            return entry.msgstr.format(**format)
        return entry.msgstr

    return msgid
