import json, sys, urllib.request
def call(url, method, params=None, session=None, timeout=60, headers=None):
    body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params or {}}).encode()
    h={'Content-Type':'application/json','Accept':'application/json, text/event-stream','User-Agent':'mcp-probe/0.1'}
    if session: h['Mcp-Session-Id']=session
    if headers: h.update(headers)
    req=urllib.request.Request(url, data=body, headers=h, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        sid=r.headers.get('Mcp-Session-Id'); raw=r.read().decode('utf-8','replace')
    # SSE or JSON
    if raw.lstrip().startswith('event:') or '\ndata:' in raw or raw.startswith('data:'):
        datas=[l[5:].strip() for l in raw.splitlines() if l.startswith('data:')]
        obj=json.loads(datas[-1]) if datas else {}
    else:
        obj=json.loads(raw) if raw.strip() else {}
    return obj, sid
def session(url, headers=None):
    init,sid=call(url,'initialize',{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"0.1"}},headers=headers)
    try: call(url,'notifications/initialized',{},session=sid,headers=headers)
    except Exception: pass
    return sid, init
if __name__=='__main__':
    url=sys.argv[1]; method=sys.argv[2]; params=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
    sid,init=session(url)
    obj,_=call(url,method,params,session=sid)
    print(json.dumps(obj,ensure_ascii=False)[:3000])
