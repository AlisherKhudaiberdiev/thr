from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import db, Distro, Software, Alternative, MigrationResult
from functools import wraps
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'linux-migrator-2026'
ADMIN_PASSWORD = 'admin123'

db.init_app(app)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─── ГЛАВНАЯ ───
@app.route('/')
def index():
    total_software = Software.query.count()
    total_distros  = Distro.query.count()
    total_analyses = MigrationResult.query.count()
    popular = Software.query.order_by(Software.search_count.desc()).limit(8).all()
    return render_template('index.html',
        total_software=total_software,
        total_distros=total_distros,
        total_analyses=total_analyses,
        popular=popular)

# ─── АНАЛИЗАТОР ───
@app.route('/analyzer')
def analyzer():
    categories = db.session.query(Software.category).distinct().all()
    categories = [c[0] for c in categories]
    software_list = Software.query.order_by(Software.name).all()
    return render_template('analyzer.html',
        categories=categories,
        software_list=software_list)

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_ids = request.form.getlist('software_ids', type=int)
    experience   = request.form.get('experience', 'beginner')
    purpose      = request.form.get('purpose', 'desktop')
    ram          = request.form.get('ram', '8', type=str)
    cpu          = request.form.get('cpu', 'modern')

    if not selected_ids:
        return redirect(url_for('analyzer'))

    selected_software = Software.query.filter(Software.id.in_(selected_ids)).all()

    # Увеличиваем счётчик поиска
    for sw in selected_software:
        sw.search_count = (sw.search_count or 0) + 1
    db.session.commit()

    # Подбираем аналоги
    alternatives = {}
    for sw in selected_software:
        alts = Alternative.query.filter_by(software_id=sw.id).order_by(Alternative.rating.desc()).all()
        alternatives[sw.id] = alts

    # Считаем сложность миграции
    difficulty_score = 0
    for sw in selected_software:
        difficulty_score += sw.migration_difficulty

    if len(selected_software) > 0:
        avg_difficulty = difficulty_score / len(selected_software)
    else:
        avg_difficulty = 1

    if avg_difficulty <= 1.5:
        difficulty_label = 'Лёгкая'
        difficulty_color = 'easy'
    elif avg_difficulty <= 2.5:
        difficulty_label = 'Средняя'
        difficulty_color = 'medium'
    else:
        difficulty_label = 'Сложная'
        difficulty_color = 'hard'

    # Подбираем дистрибутивы
    distros = Distro.query.all()
    scored  = []
    for d in distros:
        score = 0
        if experience == 'beginner'     and d.difficulty == 'Лёгкий':   score += 4
        if experience == 'intermediate' and d.difficulty == 'Средний':  score += 4
        if experience == 'advanced'     and d.difficulty == 'Сложный':  score += 4
        if purpose == 'desktop'  and d.category == 'Новичкам':          score += 3
        if purpose == 'dev'      and d.category == 'Продвинутым':       score += 3
        if purpose == 'server'   and d.category == 'Серверная':         score += 4
        if purpose == 'gaming'   and 'gaming' in (d.tags or ''):        score += 3
        ram_int = int(ram) if ram.isdigit() else 8
        if ram_int <= 4  and d.min_ram <= 2:  score += 2
        if ram_int >= 8  and d.min_ram <= 4:  score += 1
        # Штраф если слишком сложный для новичка
        if experience == 'beginner' and d.difficulty == 'Сложный': score -= 3
        scored.append((d, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    recommended = [d for d, s in scored[:3]]

    # Сохраняем результат
    result = MigrationResult(
        experience=experience, purpose=purpose, ram=ram,
        software_count=len(selected_software),
        recommended_distro=recommended[0].name if recommended else '',
        difficulty=difficulty_label
    )
    db.session.add(result)
    db.session.commit()

    # Формируем план миграции
    steps = _build_migration_plan(selected_software, experience, recommended)

    return render_template('result.html',
        selected_software=selected_software,
        alternatives=alternatives,
        recommended=recommended,
        difficulty_label=difficulty_label,
        difficulty_color=difficulty_color,
        avg_difficulty=round(avg_difficulty, 1),
        experience=experience,
        purpose=purpose,
        ram=ram,
        steps=steps)

def _build_migration_plan(software_list, experience, distros):
    steps = [
        {'num': 1, 'title': 'Создай резервную копию данных',
         'desc': 'Скопируй все важные файлы на внешний диск или в облако (Google Drive, Яндекс.Диск). Это самый важный шаг.', 'icon': '💾'},
        {'num': 2, 'title': f'Скачай {distros[0].name if distros else "Ubuntu"}',
         'desc': f'Перейди на официальный сайт и скачай ISO-образ дистрибутива {distros[0].name if distros else "Ubuntu"}.', 'icon': '⬇️'},
        {'num': 3, 'title': 'Создай загрузочную флешку',
         'desc': 'Используй программу Rufus (Windows) или Balena Etcher для записи ISO на USB-флешку (минимум 8 ГБ).', 'icon': '💿'},
        {'num': 4, 'title': 'Попробуй в режиме Live',
         'desc': 'Загрузись с флешки и попробуй систему без установки. Убедись что всё оборудование работает.', 'icon': '🖥️'},
        {'num': 5, 'title': 'Установи систему',
         'desc': 'Следуй инструкциям установщика. Рекомендуем оставить Windows на отдельном разделе для двойной загрузки.', 'icon': '⚙️'},
        {'num': 6, 'title': 'Установи аналоги программ',
         'desc': f'Установи Linux-аналоги для {len(software_list)} твоих программ. Список аналогов ниже.', 'icon': '📦'},
    ]
    if experience == 'beginner':
        steps.append({'num': 7, 'title': 'Изучи основы терминала',
            'desc': 'Выучи 10 базовых команд: ls, cd, sudo apt install, cp, mv, rm. Это займёт 1-2 часа.', 'icon': '📚'})
    return steps

# ─── КАТАЛОГ ───
@app.route('/distros')
def distros():
    all_distros = Distro.query.order_by(Distro.rating.desc()).all()
    return render_template('distros.html', distros=all_distros)

# ─── АНАЛОГИ ───
@app.route('/alternatives')
def alternatives():
    category = request.args.get('category', '')
    search   = request.args.get('search', '')
    query    = Software.query
    if category: query = query.filter_by(category=category)
    if search:   query = query.filter(Software.name.ilike(f'%{search}%'))
    software  = query.order_by(Software.name).all()
    categories = [c[0] for c in db.session.query(Software.category).distinct().all()]
    return render_template('alternatives.html',
        software=software, categories=categories,
        selected_category=category, search=search)

# ─── ГАЙД ───
@app.route('/guide')
def guide():
    return render_template('guide.html')

# ─── API ───
@app.route('/api/software')
def api_software():
    q = request.args.get('q', '').strip()
    if not q: return jsonify([])
    results = Software.query.filter(Software.name.ilike(f'%{q}%')).limit(8).all()
    return jsonify([{'id': s.id, 'name': s.name, 'category': s.category,
                     'icon': s.icon} for s in results])

# ─── ADMIN ───
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        error = 'Неверный пароль'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin_panel():
    software  = Software.query.order_by(Software.name).all()
    distros   = Distro.query.order_by(Distro.name).all()
    results   = MigrationResult.query.order_by(MigrationResult.id.desc()).limit(20).all()
    return render_template('admin_panel.html',
        software=software, distros=distros, results=results)

@app.route('/admin/software/add', methods=['POST'])
@admin_required
def admin_add_software():
    s = Software(
        name=request.form['name'],
        category=request.form.get('category', ''),
        icon=request.form.get('icon', '💻'),
        windows_only=bool(request.form.get('windows_only')),
        migration_difficulty=int(request.form.get('migration_difficulty', 2)),
        description=request.form.get('description', '')
    )
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/software/delete/<int:sw_id>', methods=['POST'])
@admin_required
def admin_delete_software(sw_id):
    Alternative.query.filter_by(software_id=sw_id).delete()
    db.session.delete(Software.query.get_or_404(sw_id))
    db.session.commit()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)
