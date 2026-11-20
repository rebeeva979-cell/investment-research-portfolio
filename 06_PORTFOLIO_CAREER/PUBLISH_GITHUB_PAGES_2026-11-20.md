# Публикация портфолио на GitHub Pages

**Цель:** получить публичный URL вида `https://<username>.github.io/<repo>/` и подставить его в CV и LinkedIn.

Публикуется только папка `docs/` (1,1 МБ, 28 файлов). Исходные данные, raw JSON и рабочие файлы проекта остаются локально.

## Вариант A — через браузер (без терминала)

1. Войти в GitHub → **New repository**.
2. Имя: `crypto-research-portfolio`. Видимость: **Public** (бесплатный GitHub Pages для public-репозиториев). Не добавлять README, .gitignore и license.
3. На странице пустого репозитория: **Add file → Upload files**.
4. Перетащить папку `docs` целиком из файлового менеджера в окно браузера. GitHub сохранит вложенные папки `assets/` и `data/`.
5. Commit message: `Portfolio v3: ETHFI on-chain case, RU/EN site`. Нажать **Commit changes**.
6. **Settings → Pages → Build and deployment**:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
   - **Save**
7. Подождать 1–10 минут. На странице Pages появится ссылка **Visit site**.
8. Проверить: главная, `/ethfi.html`, `/method.html`, `/cv.html`, PDF и CSV. Переключить RU/EN, открыть с телефона.

Если GitHub не показывает папку `docs` при загрузке, создать её вручную: **Add file → Create new file**, в имени написать `docs/.nojekyll`, оставить пустым, Commit. Затем загрузить остальные файлы внутрь `docs`.

## Вариант B — через терминал

```bash
cd /home/nikolay/Documents/codex/03-INVESTICI/portfeli-i-onchain/Crypto_Investment_Research_Portfolio

git init -b main
git add .gitignore README.md docs
git commit -m "Portfolio v3: ETHFI on-chain case, RU/EN site"

# HTTPS: GitHub попросит логин и Personal Access Token вместо пароля.
# Токен создаётся: GitHub → Settings → Developer settings → Personal access tokens.
git remote add origin https://github.com/<username>/crypto-research-portfolio.git
git push -u origin main
```

Если настроен SSH-ключ, вместо HTTPS:

```bash
git remote add origin git@github.com:<username>/crypto-research-portfolio.git
git push -u origin main
```

Затем включить Pages: **Settings → Pages → Deploy from a branch → main → /docs → Save**.

## После публикации

1. Открыть URL и проверить все страницы, PDF, CSV, переключатель RU/EN и мобильный вид.
2. Прислать URL — заменить `[PUBLIC_PORTFOLIO_URL]` в `CV_LINKEDIN_COPY_2026-11-20.md`, добавить строку портфолио в `docs/cv.html`, перегенерировать оба CV PDF и обновить `PROJECT_STATUS.md`.
3. LinkedIn: **Add profile section → Featured → Add a link** → вставить URL. Заголовок: `On-chain Research Portfolio — ETHFI case, method, CV`.
4. Проверить, что в публичной версии нет лишних персональных данных. Телефон и email уже есть в CV и будут видны публично.

## Важно

- Не присылать пароль GitHub или Personal Access Token в чат. Токен вводится только в терминале или в менеджере учётных данных.
- Для private-репозитория бесплатный Pages не работает; нужен Public или платный план.
- Если URL открывается, но стили не загрузились, проверить, что папка `docs/assets/` загружена и в настройках Pages выбран именно `/docs`.
