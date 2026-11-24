import subprocess

for flag in ['--headless', '--headless=new']:
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        flag,
        '--no-sandbox',
        '--disable-gpu',
        '--window-size=390,844',
        '--virtual-time-budget=1000',
        '--enable-logging=stderr',
        '--v=1',
        'file:///d:/Jewellery/temp_vw.html'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for l in (res.stderr + res.stdout).splitlines():
        if 'INNER_WIDTH' in l:
            print(flag, l)
