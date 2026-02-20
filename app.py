import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from photo_processor import extract_metadata, create_thumbnail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'photo-org-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['THUMBNAIL_FOLDER'] = os.path.join('static', 'thumbnails')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'heic'}

db = SQLAlchemy(app)

# ── 모델 ──────────────────────────────────────────────────────────────────────

photo_tags = db.Table('photo_tags',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id'), primary_key=True),
    db.Column('tag_id',   db.Integer, db.ForeignKey('tag.id'),   primary_key=True)
)

album_photos = db.Table('album_photos',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id'),  primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'),  primary_key=True)
)


class Photo(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    filename     = db.Column(db.String(255), nullable=False)
    original_name= db.Column(db.String(255), nullable=False)
    file_size    = db.Column(db.Integer)
    width        = db.Column(db.Integer)
    height       = db.Column(db.Integer)
    taken_at     = db.Column(db.DateTime)
    camera_make  = db.Column(db.String(100))
    camera_model = db.Column(db.String(100))
    latitude     = db.Column(db.Float)
    longitude    = db.Column(db.Float)
    description  = db.Column(db.Text)
    uploaded_at  = db.Column(db.DateTime, default=datetime.utcnow)
    tags         = db.relationship('Tag',   secondary=photo_tags,   backref='photos')
    albums       = db.relationship('Album', secondary=album_photos, backref='photos')

    @property
    def thumbnail_path(self):
        name, _ = os.path.splitext(self.filename)
        return f"{name}_thumb.jpg"

    @property
    def year_month(self):
        if self.taken_at:
            return self.taken_at.strftime('%Y년 %m월')
        return self.uploaded_at.strftime('%Y년 %m월')


class Album(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    cover_photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    cover_photo = db.relationship('Photo', foreign_keys=[cover_photo_id])


class Tag(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'


# ── 유틸 ──────────────────────────────────────────────────────────────────────

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_dirs():
    os.makedirs(app.config['UPLOAD_FOLDER'],    exist_ok=True)
    os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)


# ── 라우트 ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    sort  = request.args.get('sort', 'date')
    query = request.args.get('q', '').strip()
    tag   = request.args.get('tag', '')
    year  = request.args.get('year', '')
    month = request.args.get('month', '')

    photos_q = Photo.query

    if query:
        photos_q = photos_q.filter(
            db.or_(
                Photo.original_name.ilike(f'%{query}%'),
                Photo.description.ilike(f'%{query}%'),
                Photo.camera_model.ilike(f'%{query}%'),
            )
        )
    if tag:
        photos_q = photos_q.filter(Photo.tags.any(Tag.name == tag))
    if year:
        photos_q = photos_q.filter(db.extract('year', Photo.taken_at) == int(year))
    if month:
        photos_q = photos_q.filter(db.extract('month', Photo.taken_at) == int(month))

    if sort == 'date':
        photos_q = photos_q.order_by(
            db.case((Photo.taken_at.isnot(None), Photo.taken_at), else_=Photo.uploaded_at).desc()
        )
    elif sort == 'name':
        photos_q = photos_q.order_by(Photo.original_name)
    elif sort == 'size':
        photos_q = photos_q.order_by(Photo.file_size.desc())

    photos = photos_q.all()
    albums = Album.query.order_by(Album.created_at.desc()).all()
    tags   = Tag.query.order_by(Tag.name).all()

    # 연도별 그룹
    years = db.session.query(
        db.extract('year', Photo.taken_at).label('yr')
    ).filter(Photo.taken_at.isnot(None)).distinct().order_by(db.text('yr desc')).all()

    return render_template('index.html',
        photos=photos, albums=albums, tags=tags,
        years=[int(y.yr) for y in years],
        sort=sort, query=query, selected_tag=tag,
        selected_year=year, selected_month=month)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('photos')
        album_id = request.form.get('album_id', '')
        tag_names = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]

        if not files or all(f.filename == '' for f in files):
            flash('파일을 선택해주세요.', 'error')
            return redirect(request.url)

        uploaded = 0
        for file in files:
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                save_path   = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(save_path)

                meta = extract_metadata(save_path)
                thumb_name = f"{unique_name.rsplit('.', 1)[0]}_thumb.jpg"
                create_thumbnail(save_path, os.path.join(app.config['THUMBNAIL_FOLDER'], thumb_name))

                photo = Photo(
                    filename      = unique_name,
                    original_name = file.filename,
                    file_size     = os.path.getsize(save_path),
                    width         = meta.get('width'),
                    height        = meta.get('height'),
                    taken_at      = meta.get('taken_at'),
                    camera_make   = meta.get('camera_make'),
                    camera_model  = meta.get('camera_model'),
                    latitude      = meta.get('latitude'),
                    longitude     = meta.get('longitude'),
                )
                db.session.add(photo)
                db.session.flush()

                # 태그
                for tname in tag_names:
                    tag = Tag.query.filter_by(name=tname).first()
                    if not tag:
                        tag = Tag(name=tname)
                        db.session.add(tag)
                    photo.tags.append(tag)

                # 앨범
                if album_id:
                    album = Album.query.get(int(album_id))
                    if album:
                        photo.albums.append(album)
                        if not album.cover_photo_id:
                            album.cover_photo_id = photo.id

                uploaded += 1

        db.session.commit()
        flash(f'{uploaded}장의 사진이 업로드되었습니다.', 'success')
        return redirect(url_for('index'))

    albums = Album.query.order_by(Album.name).all()
    return render_template('upload.html', albums=albums)


@app.route('/photo/<int:photo_id>')
def photo_detail(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    prev_photo = Photo.query.filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    next_photo = Photo.query.filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
    all_tags   = Tag.query.order_by(Tag.name).all()
    all_albums = Album.query.order_by(Album.name).all()
    return render_template('photo_detail.html',
        photo=photo, prev_photo=prev_photo, next_photo=next_photo,
        all_tags=all_tags, all_albums=all_albums)


@app.route('/photo/<int:photo_id>/edit', methods=['POST'])
def edit_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo.description = request.form.get('description', '')

    tag_names = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
    photo.tags.clear()
    for tname in tag_names:
        tag = Tag.query.filter_by(name=tname).first()
        if not tag:
            tag = Tag(name=tname)
            db.session.add(tag)
        photo.tags.append(tag)

    album_ids = request.form.getlist('albums')
    photo.albums.clear()
    for aid in album_ids:
        album = Album.query.get(int(aid))
        if album:
            photo.albums.append(album)

    db.session.commit()
    flash('사진 정보가 수정되었습니다.', 'success')
    return redirect(url_for('photo_detail', photo_id=photo_id))


@app.route('/photo/<int:photo_id>/delete', methods=['POST'])
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    thumb_path  = os.path.join(app.config['THUMBNAIL_FOLDER'], photo.thumbnail_path)
    if os.path.exists(upload_path):
        os.remove(upload_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    db.session.delete(photo)
    db.session.commit()
    flash('사진이 삭제되었습니다.', 'success')
    return redirect(url_for('index'))


@app.route('/albums')
def albums():
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template('albums.html', albums=albums)


@app.route('/album/new', methods=['POST'])
def new_album():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    if not name:
        flash('앨범 이름을 입력해주세요.', 'error')
        return redirect(url_for('albums'))
    album = Album(name=name, description=description)
    db.session.add(album)
    db.session.commit()
    flash(f'앨범 "{name}"이 생성되었습니다.', 'success')
    return redirect(url_for('album_detail', album_id=album.id))


@app.route('/album/<int:album_id>')
def album_detail(album_id):
    album = Album.query.get_or_404(album_id)
    return render_template('album_detail.html', album=album)


@app.route('/album/<int:album_id>/delete', methods=['POST'])
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    flash('앨범이 삭제되었습니다.', 'success')
    return redirect(url_for('albums'))


@app.route('/api/stats')
def stats():
    total_photos = Photo.query.count()
    total_albums = Album.query.count()
    total_tags   = Tag.query.count()
    total_size   = db.session.query(db.func.sum(Photo.file_size)).scalar() or 0
    return jsonify({
        'total_photos': total_photos,
        'total_albums': total_albums,
        'total_tags':   total_tags,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
    })


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/thumbnails/<path:filename>')
def thumbnail_file(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)


# ── 메인 ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        ensure_dirs()
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
