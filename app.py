from flask import Flask, render_template_string, request

app = Flask(__name__)

# قائمة لتخزين الكتب التي يضيفها البائعون مؤقتاً
books = []

@app.route('/')
def home():
    return render_template_string(HTML_CODE, books=books)

@app.route('/add', methods=['POST'])
def add_book():
    # استقبال البيانات من واجهة البائع كما في صورتك
    new_book = {
        "wallet": request.form.get('wallet'),
        "desc": request.form.get('desc'),
        "price": request.form.get('price'),
        "title": request.form.get('title', 'PDF File')
    }
    books.append(new_book)
    return "تم النشر بنجاح! <a href='/'>عودة للمتجر</a>"

# تصميم الواجهة (HTML) مدمج في الكود ليسهل عليك رفعه في ملف واحد
HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر آدم الرقمي</title>
    <script src="https://cdn.ethers.io/lib/ethers-5.2.umd.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9f9f9; padding: 20px; }
        .search-container { margin-bottom: 30px; }
        .search-bar { padding: 12px; width: 70%; border-radius: 25px; border: 1px solid #ccc; font-size: 16px; }
        .card { background: white; border-radius: 15px; padding: 15px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .pdf-icon { width: 40px; margin-left: 15px; }
        .buy-btn { background-color: #e2761b; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .add-section { margin-top: 50px; border-top: 2px solid #eee; padding-top: 20px; }
        input, textarea { width: 90%; padding: 10px; margin: 10px 0; border-radius: 8px; border: 1px solid #ddd; }
    </style>
</head>
<body>

    <div class="search-container">
        <input type="text" class="search-bar" placeholder="Search....">
        <button style="background: none; border: none; font-size: 24px;">🔍</button>
    </div>

    <div id="book-list">
        {% for book in books %}
        <div class="card">
            <div style="display: flex; align-items: center;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg" class="pdf-icon">
                <div>
                    <strong>{{ book.title }}</strong><br>
                    <small>{{ book.desc }}</small>
                </div>
            </div>
            <div>
                <span style="font-weight: bold;">{{ book.price }} ETH</span><br>
                <button class="buy-btn" onclick="pay('{{ book.wallet }}', '{{ book.price }}')">شراء</button>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="add-section">
        <h2>إضافة مشروع +</h2>
        <form action="/add" method="POST">
            <input type="text" name="wallet" placeholder="رمز المحفظة الرقمية (0x...)" required>
            <input type="text" name="title" placeholder="اسم الكتاب أو الملف">
            <textarea name="desc" placeholder="الوصف (سيستخدمه الذكاء الاصطناعي للبحث)" rows="3" required></textarea>
            <input type="text" name="price" placeholder="السعر بالـ ETH (مثال: 0.001)" required>
            <button type="submit" class="buy-btn" style="background-color: #28a745; width: 100%;">نشر</button>
        </form>
    </div>

    <script>
    async function pay(sellerWallet, amount) {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const provider = new ethers.providers.Web3Provider(window.ethereum);
                await provider.send("eth_requestAccounts", []);
                const signer = provider.getSigner();
                
                const tx = await signer.sendTransaction({
                    to: sellerWallet,
                    value: ethers.utils.parseEther(amount)
                });
                
                alert("تم إرسال طلب الدفع! رقم العملية: " + tx.hash);
            } catch (error) {
                alert("خطأ في العملية: " + error.message);
            }
        } else {
            alert("يرجى تثبيت MetaMask (رأس الثعلب) للمتابعة");
        }
    }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run()
