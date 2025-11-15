import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, FileImage, X } from "lucide-react";
import { toast } from "sonner";

interface UploadZoneProps {
  onUpload: (file: File) => void;
}

const UploadZone = ({ onUpload }: UploadZoneProps) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      toast.error("Por favor, envie apenas arquivos de imagem");
      return;
    }

    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
    onUpload(file);
  };

  const clearFile = () => {
    setPreview(null);
    setFileName("");
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <Card className="relative overflow-hidden" style={{ boxShadow: "var(--shadow-medium)" }}>
      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt="Preview"
            className="w-full h-64 object-contain bg-muted"
          />
          <Button
            variant="destructive"
            size="icon"
            className="absolute top-4 right-4"
            onClick={clearFile}
          >
            <X className="h-4 w-4" />
          </Button>
          <div className="p-4 border-t border-border">
            <p className="text-sm text-muted-foreground truncate">{fileName}</p>
          </div>
        </div>
      ) : (
        <div
          className={`p-12 border-2 border-dashed rounded-lg transition-all ${
            dragActive
              ? "border-primary bg-accent/50"
              : "border-border bg-card"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="flex flex-col items-center cursor-pointer"
          >
            <div className="w-16 h-16 rounded-full bg-accent flex items-center justify-center mb-4">
              {dragActive ? (
                <FileImage className="h-8 w-8 text-accent-foreground" />
              ) : (
                <Upload className="h-8 w-8 text-accent-foreground" />
              )}
            </div>
            <h3 className="text-lg font-semibold mb-2">
              Arraste uma imagem ou clique para selecionar
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Formatos suportados: JPG, PNG, WEBP
            </p>
            <Button variant="secondary">Selecionar Arquivo</Button>
          </label>
        </div>
      )}
    </Card>
  );
};

export default UploadZone;
