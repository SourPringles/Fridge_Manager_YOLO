# Base Librarys

# Libraries
from flask import Blueprint, jsonify

# Custom Librarys
from db import load_storage, update_storage


rename_bp = Blueprint('rename', __name__)

@rename_bp.route('/rename/<uid>/<new_name>', methods=['POST'])
def rename(uid, new_name):
    """
    별명 변경 엔드포인트
    """
    # SQL 조회로 최신 인벤토리 반환
    inventory = load_storage()

    print(uid, new_name)
    print(inventory)

    for data in inventory:
        if data["uuid"] == uid:
            # uid가 일치하는 경우
            data["nickname"] = new_name
            update_storage(data)
            inventory = load_storage()
            print(inventory)
            return jsonify({"message": "Nickname updated successfully.", "result": data})

    return "ok"



    # QR 코드로 항목 찾기
    # if uid in inventory:
    #     inventory[uid]["nickname"] = new_name
    #     update_storage(uid, inventory[uid])
    #     inventory = load_storage()
    #     return jsonify({"message": "Nickname updated successfully.", "inventory": inventory})
    # else:
    #     return jsonify({"error": f"Item with UID '{uid}' not found."}), 404