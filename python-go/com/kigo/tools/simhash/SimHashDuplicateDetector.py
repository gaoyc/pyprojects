import hashlib
from datasketch import MinHash, MinHashLSH


class hDuplicateDetector:
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def simhash(self, text):
        """计算文本的SimHash值"""
        words = jieba.cut(text)
        v = [0] * 64

        for word in words:
            # 计算词的hash值
            h = hashlib.md5(word.encode('utf-8')).hexdigest()
            h = int(h, 16) & ((1 << 64) - 1)

            for i in range(64):
                bit = (h >> i) & 1
                v[i] += 1 if bit else -1

        # 生成SimHash
        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= 1 << i
        return fingerprint

    def similarity(self, hash1, hash2):
        """计算两个SimHash的相似度"""
        x = (hash1 ^ hash2) & ((1 << 64) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return 1 - ans / 64

    def is_duplicate(self, text1, text2):
        hash1 = self.simhash(text1)
        hash2 = self.simhash(text2)
        return self.similarity(hash1, hash2) >= self.threshold