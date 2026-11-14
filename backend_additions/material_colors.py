"""
Material Colors system — added on top of existing backend.
This module gets imported into backend.py when we swap.
For now, we build it standalone in cutpro-next.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime

# This will be set by the importing module
material_colors_col = None

def init(collection):
    """Called from backend.py to wire up the MongoDB collection."""
    global material_colors_col
    material_colors_col = collection

material_colors_bp = Blueprint('material_colors', __name__)

# ============================================
# DEFAULT PALETTE — 12 materials × 4 shades
# ============================================
DEFAULT_MATERIALS = [
    {
        "id": "oak",
        "name": "Oak",
        "color": "#784625",  # rgb(120, 70, 37)
        "is_default": True
    },
    {
        "id": "normal-mdf",
        "name": "Normal MDF",
        "color": "#FFFFFF",  # rgb(255, 255, 255)
        "is_default": True
    },
    {
        "id": "uv-board",
        "name": "UV Board",
        "color": "#FFFACD", # rgb(255, 250, 205)
        "is_default": True
    },
    {
        "id": "grey-mdf",
        "name": "Grey MDF",
        "color": "#A9A9A9",  # rgb(169, 169, 169)
        "is_default": True
    }
]

# ============================================
# ENDPOINTS
# ============================================

@material_colors_bp.route('/api/material-colors', methods=['GET', 'OPTIONS'])
def get_material_colors():
    if request.method == 'OPTIONS':
        return '', 200

    # If no auth, return defaults
    from flask import request as rq
    auth = rq.headers.get('Authorization', '')

    if not auth.startswith('Bearer '):
        return jsonify({'success': True, 'materials': DEFAULT_MATERIALS, 'source': 'default'})

    try:
        import jwt as pyjwt
        from flask import current_app
        token = auth.split(' ')[1]
        data = pyjwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
    except Exception:
        return jsonify({'success': True, 'materials': DEFAULT_MATERIALS, 'source': 'default'})

    if material_colors_col is None:
        return jsonify({'success': True, 'materials': DEFAULT_MATERIALS, 'source': 'default'})

    doc = material_colors_col.find_one({'username': username})
    if doc and 'materials' in doc:
        return jsonify({'success': True, 'materials': doc['materials'], 'source': 'user'})

    return jsonify({'success': True, 'materials': DEFAULT_MATERIALS, 'source': 'default'})


@material_colors_bp.route('/api/material-colors', methods=['POST', 'OPTIONS'])
def save_material_colors():
    if request.method == 'OPTIONS':
        return '', 200

    from flask import request as rq
    auth = rq.headers.get('Authorization', '')

    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401

    try:
        import jwt as pyjwt
        from flask import current_app
        token = auth.split(' ')[1]
        data = pyjwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
    except Exception:
        return jsonify({'error': 'Invalid token'}), 401

    if material_colors_col is None:
        return jsonify({'error': 'Storage unavailable'}), 500

    body = request.json or {}
    materials = body.get('materials', [])

    material_colors_col.update_one(
        {'username': username},
        {'$set': {
            'username': username,
            'materials': materials,
            'updated_at': datetime.now().isoformat()
        }},
        upsert=True
    )

    return jsonify({'success': True, 'message': 'Saved', 'count': len(materials)})


@material_colors_bp.route('/api/material-colors/reset', methods=['POST', 'OPTIONS'])
def reset_material_colors():
    if request.method == 'OPTIONS':
        return '', 200

    from flask import request as rq
    auth = rq.headers.get('Authorization', '')

    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401

    try:
        import jwt as pyjwt
        from flask import current_app
        token = auth.split(' ')[1]
        data = pyjwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
    except Exception:
        return jsonify({'error': 'Invalid token'}), 401

    if material_colors_col is not None:
        material_colors_col.delete_one({'username': username})

    return jsonify({'success': True, 'materials': DEFAULT_MATERIALS, 'message': 'Reset to defaults'})