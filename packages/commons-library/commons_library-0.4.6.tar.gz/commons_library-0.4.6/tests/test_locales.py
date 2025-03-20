import tempfile
import unittest
from pathlib import Path

from commons.locales import Locale, LocaleConfig

TEMP_DIR: Path = Path(tempfile.mkdtemp())

class TestLocales(unittest.TestCase):
    def test_successful(self):
        (TEMP_DIR / "en" / "LC_MESSAGES").mkdir(parents=True)
        (TEMP_DIR / "en" / "LC_MESSAGES" / "messages.po").write_text(
            'msgid "Hello"\nmsgstr "Hello, World!"'
        )

        locale: Locale = Locale("en", TEMP_DIR)

        assert locale
        assert locale.language == "en"
        assert locale.gettext("Hello") == "Hello, World!"
        assert locale.languages(filter_by=["pt_BR", "es_ES"]) == ["Brazilian Portuguese", "European Spanish"]
        assert LocaleConfig(TEMP_DIR, supported_locales=["en"])
        assert LocaleConfig(TEMP_DIR, supported_locales=["en"]).default_locale.language == "en"
        assert LocaleConfig(TEMP_DIR, supported_locales=["en"]).supported_languages == ["English"]
        assert LocaleConfig(TEMP_DIR, supported_locales=["en", "en_US"]).supported_languages == ["English", "American English"]
        assert [str(locale) for locale in
                LocaleConfig(TEMP_DIR, supported_locales=["en", "en_US"]).locales.keys()] == ["en", "en_US"]
        assert str(LocaleConfig(TEMP_DIR, supported_locales=["en"]).lookup("en_US")) == "en"
        assert str(LocaleConfig(TEMP_DIR, supported_locales=["en_US"]).lookup("en")) == "en_US"
        self.assertRaises(ValueError, LocaleConfig, translations_directory=TEMP_DIR / "inexistent", supported_locales=[])
        self.assertRaises(ValueError, LocaleConfig, translations_directory=TEMP_DIR, supported_locales=[])
        self.assertRaises(ValueError, LocaleConfig, translations_directory=TEMP_DIR, supported_locales=["invalid_locale"])

    def test_formatters(self):
        from datetime import date, time, datetime, timedelta
        locale: Locale = Locale("pt_BR")

        assert locale.format_timezone("Europe/Lisbon") == "Horário da Europa Ocidental"
        assert locale.format_number(1234.56) == "1.234,56"
        assert locale.format_currency(1234.56, "BRL") == "R$\u00A01.234,56"
        assert locale.format_date(date(day=4, month=8, year=2025)) == "4 de ago. de 2025"
        assert locale.format_date(date(day=4, month=8, year=2025), format="short") == "04/08/2025"
        assert locale.format_time(time(hour=12, minute=43, second=22)) == "12:43:22"
        assert (locale.format_datetime(datetime(day=4, month=8, year=2025, hour=12, minute=43, second=22)) ==
                "4 de ago. de 2025 12:43:22")
        assert locale.format_datetime(datetime(day=4, month=8, year=2025, hour=12, minute=43, second=22),
                                      format="short") == "04/08/2025 12:43"
        assert locale.format_timedelta(timedelta(days=4)) == "4 dias"
        assert locale.format_interval(start=date(day=4, month=8, year=2025), end=datetime(day=8, month=10, year=2025),
                                      skeleton="ddMMyyyy") == "04/08/2025\u2009–\u200908/10/2025"
        assert locale.format_list(["1", "2", "3"]) == "1, 2 e 3"

    def test_invalid(self):
        self.assertRaises(ValueError, Locale, locale="invalid")

