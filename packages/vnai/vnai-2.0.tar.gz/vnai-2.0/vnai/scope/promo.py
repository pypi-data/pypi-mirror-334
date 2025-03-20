_A=None
import requests
from datetime import datetime
import random,threading,time
class ContentManager:
	_instance=_A;_lock=threading.Lock()
	def __new__(A):
		with A._lock:
			if A._instance is _A:A._instance=super(ContentManager,A).__new__(A);A._instance._initialize()
			return A._instance
	def _initialize(A):A.last_display=0;A.display_interval=86400;A.content_url='https://vnstocks.com/files/package_ads.html';A.target_url='https://vnstocks.com/lp-khoa-hoc-python-chung-khoan';A.image_url='https://course.learn-anything.vn/wp-content/uploads/2025/03/cta-python-chung-khoan-k10-simple.jpg';A._start_periodic_display()
	def _start_periodic_display(A):
		def B():
			while True:
				B=random.randint(7200,21600);time.sleep(B);C=time.time()
				if C-A.last_display>=A.display_interval:A.present_content()
		C=threading.Thread(target=B,daemon=True);C.start()
	def fetch_remote_content(B):
		try:
			A=requests.get(B.content_url,timeout=3)
			if A.status_code==200:return A.text
			return
		except:return
	def present_content(A,environment=_A):
		B=environment;A.last_display=time.time()
		if B is _A:from vnai.scope.profile import inspector as F;B=F.examine().get('environment','unknown')
		D=A.fetch_remote_content();G=f'''
        <a href="{A.target_url}">
            <img src="{A.image_url}" 
            alt="Khóa học Python Chứng khoán" style="max-width: 100%; border-radius: 4px;">
        </a>
        ''';H=f"[![Khóa học Python Chứng khoán]({A.image_url})]({A.target_url})";I=f"""
        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║  🚀 Phân tích dữ liệu & tạo bot chứng khoán K10          ║
        ║                                                          ║
        ║  ✓ Khai giảng khóa mới từ 23/3/2025                      ║
        ║  ✓ Tạo bot python đầu tư từ số 0                         ║
        ║  ✓ Học 10 buổi chiều Chủ Nhật                            ║
        ║                                                          ║
        ║  → Đăng ký ngay: {A.target_url} ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝
        """
		if B=='jupyter':
			try:
				from IPython.display import display as C,HTML as E,Markdown as J
				if D:C(E(D))
				else:
					try:C(J(H))
					except:C(E(G))
			except:pass
		elif B=='terminal':print(I)
		else:print(f"🚀 Phân tích dữ liệu & tạo bot chứng khoán K10 - Đăng ký: {A.target_url}")
manager=ContentManager()
def present():return manager.present_content()