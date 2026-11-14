import sys
sys.modules['mongo_config'] = type(sys)('mongo_config')
sys.modules['mongo_config'].users_col = None
sys.modules['mongo_config'].history_col = None
sys.modules['mongo_config'].skp_col = None
sys.modules['mongo_config'].client = type('obj', (object,), {'__getitem__': lambda self, x: type('obj', (object,), {'__getitem__': lambda self, y: None})()})()
sys.modules['backend_additions.material_colors'] = type(sys)('backend_additions.material_colors')
sys.modules['backend_additions.material_colors'].material_colors_bp = None
sys.modules['backend_additions.material_colors'].init = lambda x: None
sys.modules['backend_additions.material_colors'].DEFAULT_MATERIALS = []

from backend import pack_with_adaptive_sheets

parts = [{'w': 200, 'h': 500, 'material': 'Oak', 'label': 'PANEL', 'grain': 'length', 'qty': 1}]
sheets = pack_with_adaptive_sheets(parts, 2440, 1220, 3)

if sheets and sheets[0]['parts']:
    print('GRAIN IN OUTPUT:', sheets[0]['parts'][0].get('grain'))
    print('PART:', sheets[0]['parts'][0])
else:
    print('PACKING FAILED - No sheets returned')
