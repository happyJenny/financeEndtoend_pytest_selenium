## 技术债
- [ ] `conftest.driver_conftest` 改名 `driver`（第 5 步 fixture 链时）
- [x] `pages/home_Page.py` → `home_page.py`，`register_Page.py` → `register_page.py`（已改）
- [x] `user_factory.idCard` 恢复切片（已改）
- [ ] `pytest.ini` 删 `pythonpath = .`（走 `__init__.py` 路线，二选一）
- [ ] `RegisterPage.register()` 改双模式返回（第 2 步）
- [ ] `test_register_ok` 用 `Users_Factory.build()` 但注册后不清理数据（第 5 步 fixture 链后统一管）
- [ ] `util.py` 残留，第 2–3 步拆入 pages 后删除


# README — 第 2 步定稿

```markdown

---

# 第 2 步：操作与断言分离（方案 A 契约）— 定稿

> 本文为第 2 步定稿。此后新增 PO 一律按本契约写，不再变更。

## 1. 契约一句话

**PO 方法成功返回业务数据（`None` / `str` / `float` / `Decimal` 等），失败抛 `UIError` 子类。用例层用 `pytest.raises(XxxError, match=re.escape(msg))` 测失败，成功路径"不抛即成功"。**

PO 里零 `assert`、零 `print`。`is_*` 读状态方法返回 `bool` 是允许的——它是"读状态"，不是"操作"。

## 2. 异常体系（`assertions/assertions.py`）

```python
class UIError(Exception):
    def __init__(self, msg, *, current_url=None, from_disable=False):
        super().__init__(msg)
        self.msg = msg
        self.current_url = current_url
        self.from_disable = from_disable

class RegisterError(UIError): ...
class LoginError(UIError): ...
class TransferError(UIError): ...
class DepositError(UIError): ...
class OpenPageError(UIError): ...
```

**与方案文档的有意差异（保留现状，不改）**：
- 类名 `UIError`（方案写 `UiError`），代码已统一，不改。
- 文件名 `assertions/assertions.py`（方案写 `assertions/exceptions.py`），不改文件名。
- 新增 `OpenPageError`（打开新窗口/页面失败），方案未细分，按需加。

新增异常：`class XxxError(UIError): ...` 一行即可，别改 `UIError` 构造函数。

## 3. PO 方法契约速查

| 类别 | 方法示例 | 成功 | 失败 |
|---|---|---|---|
| 无返回值动作 | `login()` / `register()` / `logout()` / `freeze()` | `return None` | `raise LoginError` / `RegisterError` / … |
| 有返回值动作 | `open_account() -> str` / `myBalance() -> float` | `return str/float` | `raise AccountError` / `TransferError` |
| 读状态（不抛） | `is_visible()` / `is_frozen()` / `is_form_ready()` / `is_text_contains()` | `return True/False` | — |
| 读文本（不抛） | `text_of_visible()` | `return str` | 超时抛原生 `TimeoutException`，调用方转成对应 `UIError` |

## 4. inline-msg 等待策略（定稿，不再改）

**事实**：`.inline-msg.success` / `.inline-msg.error` 出现后约 2s 从 DOM 消失。

**定稿策略**（`TransferPage.transfer()` 当前实现）：

1. **第一段 `_wait_inline()`**：`WebDriverWait(timeout=SHORT_TIMEOUT=2, poll_frequency=INLINE_POLL=0.1)`，`EC.any_of(success 文案, error 可见)`。0.1s 高频轮询抓住 2s 窗口。
2. **第一段没抓到** → **第二段 `WebDriverWait(timeout=8)`**，`EC.any_of(success 文案, .holder-info.bad 可见)`。覆盖"inline 没出现，但户名校验 holder 报错"。
3. **第二段也超时** → `raise TransferError(get_first_invalid_msg() or "转账后 10s 内既无提示也未跳转")`，兜底 HTML5 校验。

**已知取舍**：inline error 若 2s 后才出现（后端慢），第二段只等 success / holder，会漏。**接受此取舍**——概率极低，且失败有 holder / HTML5 兜底。**不再加第三分支。**

新增"有 inline-msg 的表单操作"（deposit / withdraw）时，**复用此两段式模板**。

## 5. 用例层写法

```python
# 成功
LoginPage(driver).login("alice", "jepeng")     # 不抛即成功
assert "dashboard" in driver.current_url       # 可选：验证跳转

# 失败
with pytest.raises(LoginError, match=re.escape(msg)):
    LoginPage(driver).login(username, password)
```

**规则**：
- `match=` 一律 `re.escape(msg)`——错误文案含 `。`、空格、数字，不 escape 会被当正则元字符。
- 失败用例**禁止** `try/except` 包住 PO 调用，用 `pytest.raises`。
- 失败后的副作用断言（页面未离开 / 余额未变）写在 `with` 块**之后**。

## 6. 本步已覆盖的 PO 与用例

| PO | 方法 | 契约 | 对应用例 |
|---|---|---|---|
| `HomePage` | `to_login_register_page(page, title)` | 成功 `None`，超时抛原生 `TimeoutException` | 所有用例入口 |
| `LoginPage` | `login(u, p)` | 成功 `None` / 失败 `LoginError` | `test_login.py` |
| `RegisterPage` | `register(...)` | 成功 `None` / 失败 `RegisterError` | `test_register_validation.py` |
| `DashboardPage` | `to_transfer_page()` | 成功 `None` / 失败 `OpenPageError` | `test_transfer.py` |
| `TransferPage` | `transfer(...)` | 成功 `None` / 失败 `TransferError` | `test_transfer.py` |
| `TransferPage` | `myBalance()` / `is_frozen()` / `is_form_ready()` | 读状态（`myBalance` 解析失败抛 `AssertionError`，待办见 §7） | 同上 |

**验收命令**：

```bash
pytest -v
# 预期：全绿

grep -rn "assert " pages/
# 预期：无输出

grep -rn "print(" pages/
# 预期：无输出
```

## 7. 已知待办（第 3–6 步处理）

- [ ] `TransferPage.myBalance()` 解析失败 `raise AssertionError` → 改 `raise TransferError`（第 3 步）。
- [ ] `TransferPage.myBalance()` 返回 `float`，用例 `round(x*100)` 比较 → 第 3 步改 `Decimal`，用例改 `new == old - amount`。
- [ ] `DashboardPage.to_transfer_page()` 返回 `None` → 第 4 步改返回 `TransferPage`（对齐 `switch_to_tab()` 返回 Tab 对象的模式）。
- [ ] `LoginPage.login()` / `RegisterPage.register()` 后端错误在 2s 后才出现会漏 → 第 6 步稳定性优化时观察实际延迟再决定是否加兜底。
- [ ] fixture 名 `driver_conftest` 暂不改，第 5 步 fixture 链需要时统一改 `driver`。
- [ ] `assertions/assertions.py` → `exceptions.py`（可选，改则 4 处 import 同步改）。
- [ ] `UIError` → `UiError`（可选，改则所有子类同步改）。

## 8. 第 2 步"不做"清单（避免重复讨论）

- ❌ 不再给第二段 `any_of` 加 `EC.visibility_of_element_located(inline_err)`——inline 2s 消失是事实，两段式够用。
- ❌ 不引入 dict 双模式 / dataclass Result——已选方案 A（返回值 + 抛异常）。
- ❌ PO 里不写 `assert` / `print`。
- ❌ 用例里不 `try/except` 包 PO 调用。
- ❌ 不为"契约纯粹"改已跑通的 `driver_conftest` 名字。

## 9. 下一步（第 3 步入口）

1. `DashboardPage.switch_to_tab(name)` 返回对应 Tab 对象（`AccountTab` / `TransactionTab` / …）。
2. `DashboardPage` 加 `wait_loaded()` / `logout()`。
3. 建 `pages/dashboard/account_tab.py`（`open_account() -> str` / `freeze()` / `get_balance()`）和 `transaction_tab.py`（`deposit()` / `withdraw()`），供第 5 步 `funded_user` / `frozen_user` fixture 使用。
4. 顺手清 §7 前 3 条待办（`myBalance` → `Decimal`、`raise TransferError`、`to_transfer_page` 返回 `TransferPage`）。

其余 5 个 Tab（`overview` / `transfer`（内嵌）/ `records` / `logs` / `profile`）留第 4 步。
```

---

直接 append 到现有 README 末尾即可。第 8 节"不做清单"建议保留——第 3–6 步遇到争议时先看这一节。