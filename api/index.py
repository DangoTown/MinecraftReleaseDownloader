from os.path import join
import requests
import json
from flask import Flask, redirect, jsonify, request
import os
import re

app = Flask(__name__)

# Minecraft版本清单API
VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
# 旧版本下载基础URL
OLD_VERSION_BASE_URL = "https://launcher.mojang.com/v1/objects/"

# 旧版本服务器下载链接映射
OLD_VERSION_SERVER_MAP = {
    "1.7.10": "952438ac4e01b4d115c5fc38f891710c4941df29",
    "1.6.4": "050f93c1f3fe9e2052398f7bd6aca10c63d64a87",
    "1.5.2": "f9ae3f651319151ce99a0bfad6b34fa16eb6775f",
    "1.4.7": "2f0ec8efddd2f2c674c77be9ddb370b727dec676",
    "1.3.2": "3c6c8c2c2b026c1f4b9031a4943b3518afa27a41",
    "1.2.5": "d8321edc9470e56b8ad5c67bbd16beba25843336"
}

@app.route('/')
def home():
    with open(join('data', 'index.html'), 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/api/versions')
def get_versions():
    try:
        # 获取版本清单
        response = requests.get(VERSION_MANIFEST_URL)
        data = response.json()
        
        # 提取版本信息
        versions = []
        for version in data['versions']:
            version_type = 'release'
            if version['type'] == 'snapshot':
                version_type = 'snapshot'
                
            versions.append({
                'id': version['id'],
                'name': f"Minecraft {version['id']}",
                'releaseTime': version['releaseTime'],
                'type': version_type
            })
        
        # 添加旧版本信息
        for version_id, hash_value in OLD_VERSION_SERVER_MAP.items():
            versions.append({
                'id': version_id,
                'name': f"Minecraft {version_id} (旧版本)",
                'releaseTime': '2014-01-01T00:00:00+00:00',  # 使用较早的日期
                'type': 'old'
            })
        
        # 按发布时间倒序排序
        versions.sort(key=lambda x: x['releaseTime'], reverse=True)
        return jsonify(versions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<version>')
def download_server(version):
    try:
        # 检查是否是旧版本
        if version in OLD_VERSION_SERVER_MAP:
            hash_value = OLD_VERSION_SERVER_MAP[version]
            download_url = f"{OLD_VERSION_BASE_URL}{hash_value}/server.jar"
            return redirect(download_url, code=302)
        
        # 获取版本清单
        response = requests.get(VERSION_MANIFEST_URL)
        data = response.json()
        
        # 查找指定版本
        version_info = None
        for v in data['versions']:
            if v['id'] == version:
                version_info = v
                break
        
        if not version_info:
            return jsonify({'error': '版本不存在'}), 404
        
        # 获取版本详细信息
        version_response = requests.get(version_info['url'])
        version_data = version_response.json()
        
        # 获取服务器下载URL并重定向
        server_download = version_data['downloads']['server']
        return redirect(server_download['url'], code=302)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
