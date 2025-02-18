import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [uploading, setUploading] = useState(false);

  // ファイル選択時のハンドラ
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // アップロード処理
  const handleUpload = async () => {
    if (!file) {
      alert('アップロードするファイルを選択してください');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);

    try {
      // const url = 'http://localhost:8000/api/gcs/ocmai/upload'
      const url = '/api/gcs/ocmai/upload'
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadResult(response.data);
    } catch (error) {
      console.error('アップロードエラー:', error);
      alert('ファイルのアップロードに失敗しました');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1>ファイルアップロード</h1>
      <input type="file" onChange={handleFileChange} accept="image/webp, application/pdf" />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? 'アップロード中...' : 'アップロード'}
      </button>
      {uploadResult && (
        <div>
          <h2>アップロード結果</h2>
          <pre>{JSON.stringify(uploadResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
