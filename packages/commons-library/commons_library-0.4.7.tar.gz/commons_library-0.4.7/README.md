# commons-lib

This is a common library for dependencies that might be useful on Python Development.

It offers:
- A thread-safe Database Adapter + Data Migration executor powered by [SQLModel ORM (sqlalchemy)](https://sqlmodel.tiangolo.com/) and [Pydantic](https://pydantic.dev/);
- Local Cache database;
- Dynamic runtime import (`commons.runtime`);
- Local/HTTP Remote Resource representation powered by [httpx](https://www.python-httpx.org/);
- Currency support (`commons.currencies`):
  - Currencies in ISO-4217 format powered by [pycountry](https://github.com/pycountry/pycountry/);
  - Brazilian Pix support;
  - Bitcoin (BTC) and Monero (XMR) support;
  - Live currencies quotation from [Wise](https://wise.com/) and [cryptocompare.com](https://cryptocompare.com/);
  - Payment QRCode generation for cryptocurrencies and Pix;
- Support for i18n via [Babel](https://babel.pocoo.org/) (`commons.locale`):
  - Wraps common features and format methods from Babel;
  - Automatically compile `.po` files;
  - [ ] Extracts translatable strings from source-code;
- [ ] Notification System (powered by [apprise](https://github.com/caronc/apprise)):
  - [x] SMTP tool for sending messages (to be replaced);
- [ ] Media support:
  - [x] Media/MIME Types (`commons.media.mimetypes`);
  - [ ] Document Processor;
  - [x] Image Processor (`commons.media.images`);
  - [ ] Audio Processor;
  - [ ] Video Processor;
  - [ ] Subtitle Processor;

> ⚠️ This is under active development and might not be ready for production environments.

## Testing

> coverage run -m unittest && coverage html -d tests/coverage/html