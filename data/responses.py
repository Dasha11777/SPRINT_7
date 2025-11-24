create_courier_success = {"ok": True}
create_courier_duplicate_login = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
create_courier_missing_data = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

login_courier_not_found = {"code": 404, "message": "Учетная запись не найдена"}
login_courier_missing_data = {"code": 400, "message": "Недостаточно данных для входа"}

status_code_ok = 200
status_code_created = 201
status_code_bad_request = 400
status_code_not_found = 404
status_code_conflict = 409
