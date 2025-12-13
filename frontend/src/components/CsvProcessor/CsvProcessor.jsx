import { useEffect, useState } from "react";
import UploadCard from "./UploadCard";
import FileIdCard from "./FileIdCard";
import MetadataCard from "./MetadataCard";

export default function CsvProcessor() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);

  // Upload CSV to /process
  async function upload() {
    if (!file) return;
    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    const res = await fetch("http://localhost:2701/upload", {
      method: "POST",
      body: form,
    });

    const data = await res.json();
    setFileId(data.file_id);
    console.log(`Almog - here, ${data.file_id}`)
    setLoading(false);
  }

  // Poll /results/{fileId} for metadata
  useEffect(() => {
    if (!fileId) return;

    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:2701/results/${fileId}`);
      const data = await res.json();
      setMetadata(data);

      if (["processed", "partial", "failed"].includes(data?.status)) {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [fileId]);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold">CSV Processor</h1>

        <UploadCard setFile={setFile} upload={upload} loading={loading} />

        {fileId && <FileIdCard fileId={fileId} />}

        {metadata && <MetadataCard metadata={metadata} />}
      </div>
    </div>
  );
}