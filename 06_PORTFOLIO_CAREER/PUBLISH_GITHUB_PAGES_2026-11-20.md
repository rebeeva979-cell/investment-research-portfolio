# Публикация портфолио на GitHub Pages

**Цель:** получить публичный URL вида `https://<username>.github.io/<repo>/` и подставить его в CV и LinkedIn.

GitHub Pages отдаёт только папку `docs/` (1,1 МБ, 28 файлов). Сам репозиторий содержит также `04_ETHFI/onchain/` с кодом и raw-снимками и кейсы LTC/SNX/other — это доказательство процесса, а не только витрина. Папка `07_PUBLICATION/` и старые сборки исключены через `.gitignore`.

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

Браузерная загрузка всей папки проекта (67 МБ, 205 файлов) неудобна: GitHub ограничивает число файлов за один upload. Для полного репозитория используйте GitHub Desktop или вариант B. Если нужен только сайт, загрузите `docs/` и создайте `docs/.nojekyll` вручную.

## Вариант B — через терминал (репозиторий уже инициализирован)

Локальный git уже создан, первые коммиты есть. Нужно только создать пустой репозиторий на GitHub и добавить remote:

```bash
cd /home/nikolay/Documents/codex/03-INVESTICI/portfeli-i-onchain/Crypto_Investment_Research_Portfolio

git branch -M main
git remote add origin https://github.com/<username>/crypto-research-portfolio.git

# HTTPS: GitHub попросит логин и Personal Access Token вместо пароля.
# Токен создаётся: GitHub → Settings → Developer settings → Personal access tokens.
git push -u origin main
```

Если remote уже добавлен: `git push -u origin main`. Не делать `git init` и не добавлять только `docs` — иначе код пайплайна не попадёт в репозиторий.

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
