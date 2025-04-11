from flask import Flask, request, jsonify
from instaloader import Instaloader, Post
import re
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Reel/Post Downloader API - H2I"

@app.route('/api', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    shortcode = extract_shortcode(url)
    if not shortcode:
        return jsonify({"error": "Invalid Instagram URL"}), 400

    try:
        loader = Instaloader()
        post = Post.from_shortcode(loader.context, shortcode)
        media_urls = []

        if post.is_video:
            media_urls.append(post.video_url)
        else:
            for node in post.get_sidecar_nodes():
                media_urls.append(node.video_url if node.is_video else node.display_url)

        return jsonify({"media": media_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_shortcode(url):
    match = re.search(r"/(p|reel|tv)/([A-Za-z0-9_-]+)/?", url)
    if match:
        return match.group(2)
    return None

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
