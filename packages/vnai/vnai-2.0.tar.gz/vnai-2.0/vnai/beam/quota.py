_E=False
_D='resource_type'
_C='default'
_B='hour'
_A='min'
import time,threading,functools
from collections import defaultdict
from datetime import datetime
class Guardian:
	_instance=None;_lock=threading.Lock()
	def __new__(A):
		with A._lock:
			if A._instance is None:A._instance=super(Guardian,A).__new__(A);A._instance._initialize()
			return A._instance
	def _initialize(A):A.resource_limits=defaultdict(lambda:defaultdict(int));A.usage_counters=defaultdict(lambda:defaultdict(list));A.resource_limits[_C]={_A:60,_B:2000};A.resource_limits['TCBS']={_A:60,_B:2000};A.resource_limits['VCI']={_A:60,_B:2000}
	def verify(B,operation_id,resource_type=_C):
		M='is_exceeded';L='current_usage';K='limit_value';J='limit_type';I='rate_limit';A=resource_type;E=time.time();C=B.resource_limits.get(A,B.resource_limits[_C]);N=E-60;B.usage_counters[A][_A]=[A for A in B.usage_counters[A][_A]if A>N];F=len(B.usage_counters[A][_A]);O=F>=C[_A]
		if O:from vnai.beam.metrics import collector as G;G.record(I,{_D:A,J:_A,K:C[_A],L:F,M:True});return _E
		P=E-3600;B.usage_counters[A][_B]=[A for A in B.usage_counters[A][_B]if A>P];H=len(B.usage_counters[A][_B]);D=H>=C[_B];from vnai.beam.metrics import collector as G;G.record(I,{_D:A,J:_B if D else _A,K:C[_B]if D else C[_A],L:H if D else F,M:D})
		if D:return _E
		B.usage_counters[A][_A].append(E);B.usage_counters[A][_B].append(E);return True
	def usage(A,resource_type=_C):B=resource_type;D=time.time();C=A.resource_limits.get(B,A.resource_limits[_C]);E=D-60;F=D-3600;A.usage_counters[B][_A]=[A for A in A.usage_counters[B][_A]if A>E];A.usage_counters[B][_B]=[A for A in A.usage_counters[B][_B]if A>F];G=len(A.usage_counters[B][_A]);H=len(A.usage_counters[B][_B]);I=G/C[_A]*100 if C[_A]>0 else 0;J=H/C[_B]*100 if C[_B]>0 else 0;return max(I,J)
guardian=Guardian()
def optimize(resource_type):
	B=resource_type
	def A(func):
		A=func
		@functools.wraps(A)
		def C(*F,**G):
			E='function'
			if not guardian.verify(B):raise RuntimeError(f"Resource constraints detected. Please try again later.")
			H=time.time();C=_E;D=None
			try:I=A(*F,**G);C=True;return I
			except Exception as J:D=str(J);raise
			finally:K=time.time()-H;from vnai.beam.metrics import collector as L;L.record(E,{E:A.__name__,_D:B,'execution_time':K,'success':C,'error':D,'timestamp':datetime.now().isoformat()})
		return C
	return A