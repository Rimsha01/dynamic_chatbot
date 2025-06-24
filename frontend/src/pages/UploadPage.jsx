import { useState } from 'react';
import { uploadFile } from '../api/api';
import { FiUpload, FiFile, FiFileText, FiCheck, FiX, FiLoader } from 'react-icons/fi';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [fileData, setFileData] = useState({
    file_name: '',
    file_type: '',
    description: '',
  });
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setFileData((prev) => ({
      ...prev,
      file_name: selectedFile?.name.split('.').slice(0, -1).join('.') || '',
      file_type: selectedFile?.name.split('.').pop() || '',
    }));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFileData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setIsUploading(true);
    setUploadStatus(null);
    try {
      const response = await uploadFile(file, fileData);
      setUploadStatus({
        success: true,
        message: 'File uploaded and processed successfully!',
        data: response.data,
      });
      // Reset form after successful upload
      setFile(null);
      setFileData({
        file_name: '',
        file_type: '',
        description: '',
      });
      document.getElementById('file-upload').value = '';
    } catch (error) {
      setUploadStatus({
        success: false,
        message: error.response?.data?.detail || 'Upload failed. Please try again.',
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-header">
        <FiUpload size={24} />
        <h1>Upload Document</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="file-upload">
            <FiFile size={18} />
            Select File (CSV or TXT)
          </label>
          <div className="file-input-container">
            <input
              id="file-upload"
              type="file"
              onChange={handleFileChange}
              accept=".txt,.csv"
            />
            <label htmlFor="file-upload" className="file-input-label">
              <FiUpload size={16} />
              Choose File
            </label>
            <span className="file-name">
              {file ? file.name : 'No file selected'}
            </span>
          </div>
        </div>
        <div className="form-group">
          <label>
            <FiFileText size={18} />
            File Name
          </label>
          <input
            type="text"
            name="file_name"
            value={fileData.file_name}
            onChange={handleInputChange}
            required
            placeholder="Enter a name for your file"
          />
        </div>
        <div className="form-group">
          <label>
            <FiFileText size={18} />
            Description
          </label>
          <textarea
            name="description"
            value={fileData.description}
            onChange={handleInputChange}
            placeholder="Optional description of the file contents"
          />
        </div>
        <button
          type="submit"
          className="submit-button"
          disabled={isUploading || !file}
        >
          {isUploading ? (
            <>
              <FiLoader className="spinner" />
              Processing...
            </>
          ) : (
            <>
              <FiUpload size={18} />
              Upload Document
            </>
          )}
        </button>
      </form>
      {uploadStatus && (
        <div className={`status ${uploadStatus.success ? 'success' : 'error'}`}>
          {uploadStatus.success ? (
            <FiCheck size={20} />
          ) : (
            <FiX size={20} />
          )}
          <span>{uploadStatus.message}</span>
          {uploadStatus.data && (
            <div className="upload-details">
              <p>File ID: {uploadStatus.data.file_id}</p>
              <p>Chunks created: {uploadStatus.data.chunks_created}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default UploadPage;