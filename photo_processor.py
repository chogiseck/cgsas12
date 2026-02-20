"""
사진 메타데이터 추출 및 썸네일 생성 모듈
"""
import os
from datetime import datetime
from PIL import Image, ExifTags, UnidentifiedImageError


THUMBNAIL_SIZE = (400, 400)

# EXIF 태그 이름 → ID 역방향 매핑
TAG_MAP = {v: k for k, v in ExifTags.TAGS.items()}


def _get_exif(img):
    """PIL Image에서 EXIF 딕셔너리 반환 (없으면 {})."""
    try:
        raw = img._getexif()
        if raw:
            return {ExifTags.TAGS.get(k, k): v for k, v in raw.items()}
    except Exception:
        pass
    return {}


def _parse_datetime(value):
    """'YYYY:MM:DD HH:MM:SS' 형식 → datetime."""
    for fmt in ('%Y:%m:%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S'):
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            pass
    return None


def _parse_gps(gps_info):
    """GPSInfo 딕셔너리 → (latitude, longitude) 또는 (None, None)."""
    if not gps_info:
        return None, None
    try:
        def to_degrees(vals):
            d, m, s = vals
            d = float(d[0]) / float(d[1]) if isinstance(d, tuple) else float(d)
            m = float(m[0]) / float(m[1]) if isinstance(m, tuple) else float(m)
            s = float(s[0]) / float(s[1]) if isinstance(s, tuple) else float(s)
            return d + m / 60 + s / 3600

        # GPSInfo 키가 숫자인 경우
        gps_keys = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_info.items()}

        lat = to_degrees(gps_keys.get('GPSLatitude', (0, 0, 0)))
        lon = to_degrees(gps_keys.get('GPSLongitude', (0, 0, 0)))

        if gps_keys.get('GPSLatitudeRef', 'N') != 'N':
            lat = -lat
        if gps_keys.get('GPSLongitudeRef', 'E') != 'E':
            lon = -lon

        return round(lat, 6), round(lon, 6)
    except Exception:
        return None, None


def extract_metadata(file_path):
    """
    이미지 파일에서 메타데이터를 추출합니다.
    반환값: dict with keys:
        width, height, taken_at, camera_make, camera_model,
        latitude, longitude
    """
    meta = {}
    try:
        with Image.open(file_path) as img:
            # 자동 회전 적용
            img = _auto_rotate(img)
            meta['width'], meta['height'] = img.size

            exif = _get_exif(img)

            # 촬영 일시
            for field in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
                if field in exif:
                    dt = _parse_datetime(exif[field])
                    if dt:
                        meta['taken_at'] = dt
                        break

            # 카메라 정보
            meta['camera_make']  = str(exif.get('Make', '')).strip() or None
            meta['camera_model'] = str(exif.get('Model', '')).strip() or None

            # GPS
            gps_info = exif.get('GPSInfo')
            lat, lon = _parse_gps(gps_info)
            meta['latitude']  = lat
            meta['longitude'] = lon

    except UnidentifiedImageError:
        pass
    except Exception as e:
        print(f"[photo_processor] 메타데이터 추출 실패: {e}")

    return meta


def _auto_rotate(img):
    """EXIF Orientation 태그에 따라 이미지를 자동 회전합니다."""
    try:
        exif = _get_exif(img)
        orientation = exif.get('Orientation')
        rotations = {
            3: Image.ROTATE_180,
            6: Image.ROTATE_270,
            8: Image.ROTATE_90,
        }
        if orientation in rotations:
            return img.rotate(rotations[orientation], expand=True)
    except Exception:
        pass
    return img


def create_thumbnail(src_path, dest_path, size=THUMBNAIL_SIZE):
    """
    src_path 이미지의 썸네일을 dest_path에 저장합니다.
    실패하면 False를 반환합니다.
    """
    try:
        with Image.open(src_path) as img:
            img = _auto_rotate(img)
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            img.thumbnail(size, Image.LANCZOS)
            # RGBA → RGB (JPEG는 투명 채널 불가)
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            img.save(dest_path, 'JPEG', quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"[photo_processor] 썸네일 생성 실패: {e}")
        return False
