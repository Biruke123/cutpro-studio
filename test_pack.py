from rectpack import newPacker, SORT_AREA
from rectpack.maxrects import MaxRectsBssf

def test_pack():
    print("Running test...")
    
    # Simple dummy part
    parts = [{'w': 200, 'h': 500, 'material': 'Oak', 'label': 'PANEL', 'grain': 'length', 'qty': 1}]
    
    all_parts = []
    part_lookup = {}
    pid = 0
    
    for part in parts:
        for _ in range(int(part.get('qty', 1))):
            p_data = {
                'rid': pid,
                'w': float(part['w']),
                'h': float(part['h']),
                'material': part.get('material', 'MDF'),
                'label': part.get('label', 'Part'),
                'grain': part.get('grain', 'none')
            }
            all_parts.append(p_data)
            part_lookup[pid] = p_data
            pid += 1

    packer = newPacker(rotation=True, pack_algo=MaxRectsBssf, sort_algo=SORT_AREA)
    
    for p in all_parts:
        # Add rect (no rotation lock for now, just to test)
        packer.add_rect(p['w'], p['h'], rid=p['rid'])
    
    packer.add_bin(2440, 1220)
    packer.pack()
    
    used_bins = [b for b in packer if len(b) > 0]
    if not used_bins:
        print("PACKING FAILED")
        return

    # Reconstruct the output
    parts_on_sheet = []
    for rect in used_bins[0]:
        original_part = part_lookup[rect.rid]
        out_part = {
            'w': rect.width,
            'h': rect.height,
            'label': original_part['label'],
            'material': original_part['material'],
            'grain': original_part.get('grain', 'none')  # 🔥 test this
        }
        parts_on_sheet.append(out_part)

    print("SUCCESS")
    for p in parts_on_sheet:
        print(f"Part: {p['label']}, Grain: {p['grain']}")

if __name__ == '__main__':
    test_pack()