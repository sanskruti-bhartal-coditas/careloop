import { useState } from "react";
import Button from "../../../components/Button/Button";
import styles from "./UploadDocuments.module.scss";

interface UploadDocumentsProps {
  onClose: () => void;
}

const UploadDocuments = ({ onClose }: UploadDocumentsProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);

    try {
      // 1. Call your single API to get the presigned URL
      // const { presignedUrl } = await getPresignedUrlApi(file.name).unwrap();

      // 2. Upload the file directly to the S3/Cloud storage using the presigned URL
      // await fetch(presignedUrl, {
      //   method: "PUT",
      //   body: file,
      //   headers: {
      //     "Content-Type": file.type,
      //   },
      // });

      // Mock delay for demonstration
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      onClose();
    } catch (error) {
      console.error("Failed to upload document:", error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <h3>Upload Document</h3>
        <input 
            type="file" 
            onChange={handleFileChange} 
            className={styles.fileInput} 
        />
        <div className={styles.actions}>
          <Button 
            type="button" 
            variant="primary" 
            disabled={!file || isUploading} 
            onClick={handleUpload}
          >
            {isUploading ? "Uploading..." : "Upload"}
          </Button>
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </div>
    </div>
  );
};

export default UploadDocuments;