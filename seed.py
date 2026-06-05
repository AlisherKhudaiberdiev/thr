from models import db, Software, Alternative, Distro

def seed_data():
    if Software.query.count() > 0:
        return

    software_data = [
        # Office
        ('Microsoft Word',    'Office',  '📝', False, 1, 'Текстовый редактор'),
        ('Microsoft Excel',   'Office',  '📊', False, 2, 'Табличный редактор'),
        ('Microsoft PowerPoint','Office','📽️', False, 1, 'Презентации'),
        ('Microsoft Outlook', 'Office',  '📧', False, 2, 'Почтовый клиент'),
        ('Microsoft Teams',   'Office',  '💬', False, 1, 'Мессенджер для работы'),
        ('Notepad++',         'Office',  '📓', True,  1, 'Текстовый редактор с подсветкой'),
        # Browser
        ('Google Chrome',     'Browser', '🌐', False, 1, 'Браузер'),
        ('Mozilla Firefox',   'Browser', '🦊', False, 1, 'Браузер'),
        ('Opera',             'Browser', '🎭', False, 1, 'Браузер'),
        # Media
        ('Adobe Photoshop',   'Design',  '🎨', True,  3, 'Редактор фото'),
        ('Adobe Illustrator', 'Design',  '✏️', True,  3, 'Векторная графика'),
        ('Adobe Premiere',    'Design',  '🎬', True,  3, 'Видеомонтаж'),
        ('VLC Media Player',  'Media',   '▶️', False, 1, 'Медиаплеер'),
        ('Winamp',            'Media',   '🎵', True,  1, 'Музыкальный плеер'),
        ('Spotify',           'Media',   '🎧', False, 1, 'Стриминг музыки'),
        # Dev
        ('Visual Studio Code','Dev',     '💻', False, 1, 'Редактор кода'),
        ('PyCharm',           'Dev',     '🐍', False, 1, 'IDE для Python'),
        ('Git',               'Dev',     '🌿', False, 1, 'Система контроля версий'),
        ('XAMPP',             'Dev',     '🗄️', False, 2, 'Локальный веб-сервер'),
        # Gaming
        ('Steam',             'Gaming',  '🎮', False, 1, 'Игровая платформа'),
        ('Epic Games',        'Gaming',  '🕹️', False, 2, 'Игровая платформа'),
        ('Discord',           'Gaming',  '🎙️', False, 1, 'Голосовой чат'),
        # Security
        ('Kaspersky',         'Security','🛡️', True,  2, 'Антивирус'),
        ('Malwarebytes',      'Security','🔒', False, 2, 'Защита от малвари'),
        # System
        ('WinRAR',            'System',  '🗜️', True,  1, 'Архиватор'),
        ('7-Zip',             'System',  '📦', False, 1, 'Архиватор'),
        ('CCleaner',          'System',  '🧹', True,  1, 'Очистка системы'),
        ('Everything',        'System',  '🔍', True,  1, 'Поиск файлов'),
    ]

    software_objects = []
    for name, cat, icon, win_only, diff, desc in software_data:
        s = Software(name=name, category=cat, icon=icon,
                     windows_only=win_only, migration_difficulty=diff, description=desc)
        db.session.add(s)
        software_objects.append(s)
    db.session.flush()

    sw = {s.name: s for s in Software.query.all()}

    alts = [
        # Word
        (sw['Microsoft Word'].id,    'LibreOffice Writer',  'Полноценная замена Word. Открывает .docx файлы.', 9.0, 'https://libreoffice.org', True, 95),
        (sw['Microsoft Word'].id,    'WPS Office Writer',   'Очень похож на Word интерфейсом. Бесплатный.', 8.5, 'https://wps.com', True, 98),
        (sw['Microsoft Word'].id,    'OnlyOffice',          'Отличная совместимость с форматами MS Office.', 8.3, 'https://onlyoffice.com', True, 92),
        # Excel
        (sw['Microsoft Excel'].id,   'LibreOffice Calc',    'Полная замена Excel с поддержкой формул и макросов.', 8.8, 'https://libreoffice.org', True, 90),
        (sw['Microsoft Excel'].id,   'WPS Office Spreadsheets', 'Интерфейс максимально похож на Excel.', 8.5, 'https://wps.com', True, 95),
        # PowerPoint
        (sw['Microsoft PowerPoint'].id, 'LibreOffice Impress', 'Замена PowerPoint, открывает .pptx файлы.', 8.5, 'https://libreoffice.org', True, 88),
        (sw['Microsoft PowerPoint'].id, 'WPS Presentation',  'Лучший аналог PowerPoint по интерфейсу.', 8.7, 'https://wps.com', True, 95),
        # Outlook
        (sw['Microsoft Outlook'].id, 'Thunderbird',         'Мощный почтовый клиент от Mozilla.', 8.5, 'https://thunderbird.net', True, 80),
        (sw['Microsoft Outlook'].id, 'Evolution',           'Полная замена Outlook с календарём и задачами.', 8.0, 'https://wiki.gnome.org/Apps/Evolution', True, 85),
        # Teams
        (sw['Microsoft Teams'].id,   'Element (Matrix)',    'Безопасный мессенджер с видеозвонками.', 8.0, 'https://element.io', True, 75),
        (sw['Microsoft Teams'].id,   'Slack',               'Популярный корпоративный мессенджер.', 8.5, 'https://slack.com', True, 85),
        # Notepad++
        (sw['Notepad++'].id,         'Kate',                'Мощный текстовый редактор для KDE.', 8.5, 'https://kate-editor.org', True, 90),
        (sw['Notepad++'].id,         'Gedit',               'Простой редактор для GNOME.', 7.5, 'https://wiki.gnome.org/Apps/Gedit', True, 80),
        (sw['Notepad++'].id,         'Visual Studio Code',  'Бесплатный редактор с подсветкой синтаксиса.', 9.5, 'https://code.visualstudio.com', True, 95),
        # Chrome
        (sw['Google Chrome'].id,     'Google Chrome',       'Доступен нативно для Linux!', 9.0, 'https://google.com/chrome', True, 100),
        (sw['Google Chrome'].id,     'Chromium',            'Открытая версия Chrome без слежки Google.', 8.5, 'https://chromium.org', True, 99),
        # Firefox
        (sw['Mozilla Firefox'].id,   'Mozilla Firefox',     'Доступен нативно для Linux!', 9.0, 'https://firefox.com', True, 100),
        # Photoshop
        (sw['Adobe Photoshop'].id,   'GIMP',                'Мощный бесплатный редактор изображений.', 8.5, 'https://gimp.org', True, 75),
        (sw['Adobe Photoshop'].id,   'Krita',               'Профессиональный редактор для цифровой живописи.', 8.8, 'https://krita.org', True, 70),
        (sw['Adobe Photoshop'].id,   'Photopea',            'Онлайн-редактор, почти полный клон Photoshop.', 8.0, 'https://photopea.com', True, 90),
        # Illustrator
        (sw['Adobe Illustrator'].id, 'Inkscape',            'Мощный бесплатный векторный редактор.', 8.5, 'https://inkscape.org', True, 80),
        (sw['Adobe Illustrator'].id, 'Gravit Designer',     'Онлайн-редактор векторной графики.', 7.5, 'https://designer.io', True, 75),
        # Premiere
        (sw['Adobe Premiere'].id,    'DaVinci Resolve',     'Профессиональный видеоредактор. Бесплатная версия очень мощная.', 9.0, 'https://blackmagicdesign.com', True, 85),
        (sw['Adobe Premiere'].id,    'Kdenlive',            'Бесплатный видеоредактор для Linux.', 8.0, 'https://kdenlive.org', True, 70),
        (sw['Adobe Premiere'].id,    'OpenShot',            'Простой видеоредактор для начинающих.', 7.5, 'https://openshot.org', True, 65),
        # VLC
        (sw['VLC Media Player'].id,  'VLC Media Player',    'Доступен нативно для Linux!', 9.5, 'https://videolan.org', True, 100),
        # Spotify
        (sw['Spotify'].id,           'Spotify',             'Официальный клиент Spotify доступен для Linux!', 9.0, 'https://spotify.com', True, 100),
        (sw['Spotify'].id,           'Rhythmbox',           'Встроенный музыкальный плеер GNOME.', 7.5, 'https://wiki.gnome.org/Apps/Rhythmbox', True, 60),
        # VS Code
        (sw['Visual Studio Code'].id,'Visual Studio Code',  'Официальный клиент VS Code доступен для Linux!', 9.5, 'https://code.visualstudio.com', True, 100),
        # Steam
        (sw['Steam'].id,             'Steam',               'Официальный клиент Steam доступен для Linux! Proton позволяет играть в Windows-игры.', 9.0, 'https://store.steampowered.com', True, 95),
        # Discord
        (sw['Discord'].id,           'Discord',             'Официальный клиент Discord доступен для Linux!', 9.0, 'https://discord.com', True, 100),
        # WinRAR
        (sw['WinRAR'].id,            'PeaZip',              'Бесплатный архиватор с поддержкой всех форматов.', 8.0, 'https://peazip.github.io', True, 90),
        (sw['WinRAR'].id,            'File Roller',         'Встроенный архиватор GNOME.', 8.5, 'https://wiki.gnome.org/Apps/FileRoller', True, 85),
        # 7-Zip
        (sw['7-Zip'].id,             'p7zip',               'Порт 7-Zip для Linux с полной поддержкой форматов.', 9.0, 'https://p7zip.sourceforge.net', True, 100),
        # CCleaner
        (sw['CCleaner'].id,          'BleachBit',           'Мощная утилита очистки системы для Linux.', 8.5, 'https://bleachbit.org', True, 85),
        # Kaspersky
        (sw['Kaspersky'].id,         'ClamAV',              'Бесплатный антивирус с открытым кодом.', 7.5, 'https://clamav.net', True, 70),
        (sw['Kaspersky'].id,         'Sophos',              'Бесплатный антивирус для Linux от Sophos.', 8.0, 'https://sophos.com', True, 75),
    ]

    for sw_id, name, desc, rating, website, is_free, similarity in alts:
        a = Alternative(software_id=sw_id, name=name, description=desc,
                        rating=rating, website=website, is_free=is_free, similarity=similarity)
        db.session.add(a)

    distros = [
        Distro(name='Linux Mint', description='Самый дружелюбный дистрибутив для переходящих с Windows. Интерфейс Cinnamon сразу напоминает привычный рабочий стол.', based_on='Ubuntu', category='Новичкам', desktop='Cinnamon', difficulty='Лёгкий', min_ram=2, rating=9.2, website='https://linuxmint.com', tags='windows-like,beginner,gaming', why_good='Cinnamon Desktop очень похож на Windows. Меню "Пуск", панель задач, трей — всё на своих местах. Идеален для первого опыта с Linux.'),
        Distro(name='Ubuntu', description='Самый популярный дистрибутив с огромным сообществом и поддержкой.', based_on='Debian', category='Новичкам', desktop='GNOME', difficulty='Лёгкий', min_ram=4, rating=9.0, website='https://ubuntu.com', tags='beginner,popular', why_good='Огромная база документации на русском языке. Любой вопрос легко загуглить. Отличная поддержка оборудования.'),
        Distro(name='Pop!_OS', description='Разработан для разработчиков и геймеров. Отличная поддержка NVIDIA.', based_on='Ubuntu', category='Продвинутым', desktop='COSMIC', difficulty='Лёгкий', min_ram=4, rating=9.0, website='https://pop.system76.com', tags='gaming,dev,nvidia', why_good='Лучшая поддержка NVIDIA из коробки. Steam и Proton работают без дополнительной настройки. Идеален для игр.'),
        Distro(name='Zorin OS', description='Специально создан для пользователей Windows. Интерфейс максимально похож.', based_on='Ubuntu', category='Новичкам', desktop='GNOME', difficulty='Лёгкий', min_ram=2, rating=8.8, website='https://zorin.com', tags='windows-like,beginner', why_good='Zorin создан именно для перехода с Windows. Даже иконки и расположение элементов имитируют Windows 10/11.'),
        Distro(name='Fedora', description='Современный дистрибутив с последними версиями ПО. Для разработчиков.', based_on='Независимый', category='Продвинутым', desktop='GNOME', difficulty='Средний', min_ram=4, rating=8.7, website='https://fedoraproject.org', tags='dev,modern', why_good='Всегда самые новые версии программ. Отличная среда для разработки. Используется многими профессиональными разработчиками.'),
        Distro(name='Manjaro', description='Мощный rolling-release дистрибутив на основе Arch. Для опытных.', based_on='Arch Linux', category='Продвинутым', desktop='KDE Plasma', difficulty='Средний', min_ram=4, rating=8.8, website='https://manjaro.org', tags='gaming,dev,rolling', why_good='KDE Plasma максимально настраиваем. Отличная игровая производительность. Доступ к AUR — крупнейшему репозиторию пакетов.'),
        Distro(name='Ubuntu MATE', description='Лёгкий дистрибутив для слабых компьютеров. Классический интерфейс.', based_on='Ubuntu', category='Новичкам', desktop='MATE', difficulty='Лёгкий', min_ram=1, rating=8.5, website='https://ubuntu-mate.org', tags='lightweight,beginner,old-pc', why_good='Работает на компьютерах с 1 ГБ RAM. Классический интерфейс напоминает Windows XP/7. Идеален для старых ПК.'),
        Distro(name='Debian', description='Стабильнейший дистрибутив. Основа для Ubuntu и сотен других.', based_on='Независимый', category='Серверная', desktop='GNOME', difficulty='Средний', min_ram=2, rating=9.0, website='https://debian.org', tags='stable,server', why_good='Максимальная стабильность. Подходит для серверов и долгосрочного использования без переустановки.'),
    ]
    for d in distros:
        db.session.add(d)

    db.session.commit()
    print("База данных LinuxMigrator заполнена!")
