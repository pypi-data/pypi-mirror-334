# 📌 API 2FA FB

🔹 **api_2fa_fb** is a Python library that allows you to retrieve OTP codes from the Facebook 2FA API quickly and easily.

---

## 🚀 Installation

Install the library via `pip`:

```sh
pip install api-2fa-fb
```


```python
import api_2fa_fb

# Initialize with your 2FA secret code
auth = api_2fa_fb.authy("YOUR_SECRET_CODE")

# Retrieve OTP
otp = auth.get_otp()
print("🔑 OTP:", otp)

# Check exist time
exist = auth.get_exist()
print("⏳ Time Exist:", exist, "seconds")
```

## ⚙️ Requirements

- Python 3.10 or higher
- `requests` library (automatically installed via `pip`)

---

## 🛠️ Update Version

Upgrade to the latest version using:

```sh
pip install --upgrade api-2fa-fb
```

---

## 🐜 License

📝 **MIT License** - You are free to use it for personal and commercial purposes.
