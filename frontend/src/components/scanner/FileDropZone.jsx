import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File, AlertCircle } from 'lucide-react';

const FileDropZone = ({ onFileUpload, isLoading }) => {
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0 && !isLoading) {
            onFileUpload(acceptedFiles[0]);
        }
    }, [onFileUpload, isLoading]);

    const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
        onDrop,
        maxFiles: 1,
        maxSize: 100 * 1024 * 1024, // 100MB
    });

    return (
        <div
            {...getRootProps()}
            className={`
        border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300
        ${isDragActive ? 'border-threat-clean bg-dark-800' : 'border-gray-600 bg-dark-900 hover:border-gray-400'}
        ${isDragReject ? 'border-threat-critical bg-threat-critical/10' : ''}
        ${isLoading ? 'opacity-50 pointer-events-none' : ''}
      `}
        >
            <input {...getInputProps()} />

            <div className="flex flex-col items-center justify-center space-y-4">
                {isDragReject ? (
                    <>
                        <AlertCircle className="h-16 w-16 text-threat-critical animate-pulse" />
                        <p className="text-xl font-medium text-threat-critical">File type not supported or too large</p>
                    </>
                ) : (
                    <>
                        {isDragActive ? (
                            <UploadCloud className="h-16 w-16 text-threat-clean animate-bounce" />
                        ) : (
                            <File className="h-16 w-16 text-gray-500" />
                        )}
                        <div>
                            <p className="text-xl font-medium text-gray-300">
                                {isDragActive ? 'Drop your payload here' : 'Drag & Drop a file to scan'}
                            </p>
                            <p className="text-sm text-gray-500 mt-2">
                                Supported: PE Executables, DLLs, Office Macros, PDFs (Max 100MB)
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default FileDropZone;
