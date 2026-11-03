## 技术债
- [ ] `conftest.driver_conftest` 改名 `driver`（第 5 步 fixture 链时）
- [x] `pages/home_Page.py` → `home_page.py`，`register_Page.py` → `register_page.py`（已改）
- [x] `user_factory.idCard` 恢复切片（已改）
- [ ] `pytest.ini` 删 `pythonpath = .`（走 `__init__.py` 路线，二选一）
- [ ] `RegisterPage.register()` 改双模式返回（第 2 步）
- [ ] `test_register_ok` 用 `Users_Factory.build()` 但注册后不清理数据（第 5 步 fixture 链后统一管）
- [ ] `util.py` 残留，第 2–3 步拆入 pages 后删除