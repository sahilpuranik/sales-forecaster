import React, { useState } from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Alert, AlertDescription } from './ui/alert';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { cleanCsv } from '../api';

export function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [fileName, setFileName] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    const file = files[0];
    
    if (file && file.type === 'text/csv') {
      handleFileUpload(file);
    } else {
      setUploadStatus('error');
      setErrorMessage('Please upload a CSV file.');
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file: File) => {
    setFileName(file.name);
    setUploadStatus('uploading');
    setErrorMessage('');
    
    try {
      setUploadProgress(50);
      await cleanCsv(file);
      setUploadProgress(100);
      setUploadStatus('success');
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage('Upload failed. Please try again.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <Card className="border-2 border-dashed border-muted-foreground/25">
        <CardContent className="p-12">
          {uploadStatus === 'idle' && (
            <div
              className={`text-center transition-colors ${
                isDragging 
                  ? 'border-primary bg-primary/5' 
                  : 'border-muted-foreground/25 hover:border-muted-foreground/50'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <Upload className="w-16 h-16 mx-auto mb-6 text-muted-foreground" />
              <h2 className="text-2xl font-bold mb-4">Upload Your Sales Data</h2>
              <p className="text-muted-foreground mb-8 text-lg">Drag and drop your CSV file here</p>
              <Button variant="outline" size="lg" asChild>
                <label htmlFor="file-upload" className="cursor-pointer">
                  Choose File
                  <input
                    id="file-upload"
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </label>
              </Button>
            </div>
          )}

          {uploadStatus === 'uploading' && (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 mx-auto mb-6 text-primary" />
              <h3 className="text-2xl font-bold mb-4">Uploading {fileName}</h3>
              <p className="text-muted-foreground mb-8 text-lg">Processing your data...</p>
              <Progress value={uploadProgress} className="w-full max-w-md mx-auto h-3" />
              <p className="text-muted-foreground mt-4 text-lg">{uploadProgress}% complete</p>
            </div>
          )}

          {uploadStatus === 'success' && (
            <div className="text-center py-12">
              <CheckCircle className="w-16 h-16 mx-auto mb-6 text-green-600" />
              <h3 className="text-2xl font-bold mb-4">Upload Successful!</h3>
              <p className="text-muted-foreground mb-8 text-lg">
                {fileName} has been processed successfully.
              </p>
              <Button 
                onClick={() => {
                  setUploadStatus('idle');
                  setUploadProgress(0);
                  setFileName('');
                }}
                size="lg"
              >
                Upload Another File
              </Button>
            </div>
          )}

          {uploadStatus === 'error' && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
