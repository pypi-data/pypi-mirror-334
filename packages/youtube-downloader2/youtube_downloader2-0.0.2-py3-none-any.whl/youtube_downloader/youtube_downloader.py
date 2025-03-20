import requests


class YouTubeDownloader:
    def __init__(self, url):
        self.url = url

    def download(self):
        headers = {
            "authority": "ytdlp.online",
            "method": "GET",
            "path": "/stream?command=https%3A%2F%2Fyoutu.be%2F4rtYDigGkfA%3Fsi%3DRC29ELY_l0l3FJsz",
            "scheme": "https",
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://ytdlp.online/",
            "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        }

        response = requests.get(f"https://ytdlp.online/stream?command={self.url}", headers=headers)

        return response.text
    
    def get_best_quality(self):
        headers = {
            "authority": "ytdlp.online",
            "method": "GET",
            "path": "/stream?command=https%3A%2F%2Fyoutu.be%2F4rtYDigGkfA%3Fsi%3DRC29ELY_l0l3FJsz%20-f%20bestvideo%2Bbestaudio%20",
            "scheme": "https",
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://ytdlp.online/",
            "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        }

        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-f%20bestvideo%2Bbestaudio%20", headers=headers)
        return response.text.replace('href="', 'https://ytdlp.online/download/')

    def get_audio(self, format: str = "mp3"):
        headers = {
            "authority": "ytdlp.online",
            "method": "GET",
            "path": "/stream?command=https%3A%2F%2Fyoutu.be%2F4rtYDigGkfA%3Fsi%3DRC29ELY_l0l3FJsz%20%20-x%20--audio-format%20mp3%20",
            "scheme": "https",
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://ytdlp.online/",
            "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        }
        
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-x%20--audio-format%20{format}%20", headers=headers)
        return response.text.replace("download/", "https://ytdlp.online/download/")

    def get_url(self):
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20--get-url%20")
        return response.text
    
    def get_formats(self):
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-F%20")
        return response.text
    
    def get_json(self):
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-j%20")
        return response.text
    
    def get_720p_with_sound(self):
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-f%20136%2B140%20")
        return response.text.replace('href="', 'https://ytdlp.online/download/')

    def get_downloded_videos(self):
        response = requests.get("https://ytdlp.online/download/")
        return response.text.replace('href="', 'https://ytdlp.online/download/')
    
    def get_best_quality_audio(self):
        response = requests.get(f"https://ytdlp.online/stream?command={self.url}%20-f%20bestaudio%20")
        return response.text
