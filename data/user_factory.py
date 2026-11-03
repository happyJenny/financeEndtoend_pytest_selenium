import uuid
class Users_Factory:

    @staticmethod    
    def build(username=None,prefix="UI_test_",**overide):
        random=uuid.uuid4().hex
        register_data = {
            "username": username or f"{prefix}{random[:8]}",
            "password": "jepeng",
            "realName": "api-test",
            "idCard": random[:18],
            "phone": f"185{random[:8]}"
        }
        register_data.update(overide)
        return register_data    
                    # "idCard": random[:18],    