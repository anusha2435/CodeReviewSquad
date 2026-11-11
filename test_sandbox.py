from tools import run_code, sandbox_status

print("Sandbox:", sandbox_status())
print("1 normal    :", run_code("print('hello')"))
print("2 timeout   :", run_code("while True: pass"))
print("3 network   :", run_code("import urllib.request as u; u.urlopen('http://example.com', timeout=3)"))
print("4 file write:", run_code("open('x.txt', 'w').write('a')"))