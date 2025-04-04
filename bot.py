import requests
import asyncio
from pyrogram import Client, filters

# === TELEGRAM BOT CONFIG === #
API_ID = 28464245  # <<< Replace with your API ID
API_HASH = "6fe23ca19e7c7870dc2aff57fb05c4d9"  # <<< Replace with your API HASH
BOT_TOKEN = "7289532935:AAGeeVEdfHXoOAGV1NuPPlYCW5o2uj4O2-U"  # <<< Replace with your Bot Token

bot = Client("gateway_checker", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# === UTILITY FUNCTIONS === #

def find_captcha(response_text):
    text = response_text.lower()
    if 'recaptcha' in text:
        return 'Using Google reCAPTCHA ✅'
    elif 'hcaptcha' in text:
        return 'Using hCaptcha ✅'
    return 'Not using Any Captcha 🚫'

def detect_cloudflare(response):
    keywords = ["cloudflare.com", "__cfduid"]
    headers = ["cf-ray", "cf-cache-status", "server"]
    if any(k in response.text.lower() for k in keywords):
        return True
    if any(h in response.headers for h in headers):
        return True
    return False

def find_payment_gateways(response_text):
    detected_gateways = []
    lower_text = response_text.lower()
    gateways = {
        "paypal": "PayPal", "stripe": "Stripe", "braintree": "Braintree",
        "square": "Square", "authorize.net": "Authorize.Net", "2checkout": "2Checkout",
        "adyen": "Adyen", "worldpay": "Worldpay", "sagepay": "SagePay", "checkout.com": "Checkout.com",
        "skrill": "Skrill", "neteller": "Neteller", "payoneer": "Payoneer", "klarna": "Klarna",
        "afterpay": "Afterpay", "sezzle": "Sezzle", "alipay": "Alipay", "wechat pay": "WeChat Pay",
        "tenpay": "Tenpay", "qpay": "QPay", "sofort": "SOFORT Banking", "giropay": "Giropay",
        "trustly": "Trustly", "zelle": "Zelle", "venmo": "Venmo", "epayments": "ePayments",
        "revolut": "Revolut", "wise": "Wise (formerly TransferWise)", "shopify payments": "Shopify Payments",
        "woocommerce": "WooCommerce", "paytm": "Paytm", "phonepe": "PhonePe", "google pay": "Google Pay",
        "bhim upi": "BHIM UPI", "razorpay": "Razorpay", "instamojo": "Instamojo", "ccavenue": "CCAvenue",
        "payu": "PayU", "mobikwik": "MobiKwik", "freecharge": "FreeCharge", "cashfree": "Cashfree",
        "jio money": "JioMoney", "yandex.money": "Yandex.Money", "qiwi": "QIWI", "webmoney": "WebMoney",
        "paysafe": "Paysafe", "bpay": "BPAY", "mollie": "Mollie", "paysera": "Paysera",
        "multibanco": "Multibanco", "pagseguro": "PagSeguro", "mercadopago": "MercadoPago",
        "payfast": "PayFast", "billdesk": "BillDesk", "paystack": "Paystack", "interswitch": "Interswitch",
        "voguepay": "VoguePay", "flutterwave": "Flutterwave"
    }

    for key, value in gateways.items():
        if key in lower_text:
            detected_gateways.append(value)

    return detected_gateways or ["Unknown"]

def find_stripe_version(response_text):
    text = response_text.lower()
    if 'stripe3dsecure' in text:
        return "3D Secured ✅"
    elif 'stripe-checkout' in text:
        return "Checkout external link 🔗"
    return "2D site ACTIVE 📵"

# === COMMAND HANDLER === #

@bot.on_message(filters.command("gate"))
async def check_gate(_, message):
    try:
        processing = await message.reply("**Processing your request...**", disable_web_page_preview=True)
        url = message.text[len('/gate'):].strip()
        if not url:
            return await processing.edit("Please provide a URL after the command. Example: `/gate example.com`", disable_web_page_preview=True)
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()

        gateways = find_payment_gateways(response.text)
        captcha = find_captcha(response.text)
        cloudflare = detect_cloudflare(response)

        result_msg = (
            f"┏━━━━━━━⍟\n"
            f"┃ 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 : ✅\n"
            f"┗━━━━━━━━━━━━⊛\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
            f"•➥ 𝗦𝗶𝘁𝗲 -» `{url}`\n"
            f"•➥ 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀: {', '.join(gateways)}\n"
            f"•➥ 𝗖𝗮𝗽𝘁𝗰𝗵𝗮: {captcha}\n"
            f"•➥ 𝗖𝗹𝗼𝘂𝗱𝗳𝗹𝗮𝗿𝗲 𝗣𝗿𝗼𝘁𝗲𝗰𝘁𝗶𝗼𝗻: {'✅' if cloudflare else '🚫'}\n\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰"
        )
        await processing.edit(result_msg, disable_web_page_preview=True)

    except requests.RequestException:
        await processing.edit("**Error: Site unreachable or invalid.**", disable_web_page_preview=True)

# === RUN THE BOT === #
print("Bot is running... 🟢")
bot.run()

