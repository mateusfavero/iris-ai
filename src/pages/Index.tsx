import { useState } from "react";
import Header from "@/components/Header";
import UploadZone from "@/components/UploadZone";
import ResultCard from "@/components/ResultCard";
import { Button } from "@/components/ui/button";
import { Loader2, Github } from "lucide-react";
import { toast } from "sonner";

interface AnalysisResult {
  examType: string;
  diagnosis: string;
  confidence: number;
}

const Index = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [rawResponse, setRawResponse] = useState<any | null>(null);

  const handleUpload = async (file: File) => {
    setIsAnalyzing(true);
    setResult(null);


    try {
      // Faz upload da imagem para o backend Flask (tenta localhost e 127.0.0.1)
      const formData = new FormData();
      formData.append("image", file);

      const urls = ["http://localhost:5000/analyze", "http://127.0.0.1:5000/analyze"];
      let response: Response | null = null;
      let lastError: any = null;

      for (const u of urls) {
        try {
          response = await fetch(u, { method: "POST", body: formData });
          if (response.ok) break; // sucesso
        } catch (e) {
          lastError = e;
        }
      }

      if (!response) throw lastError || new Error("Nenhuma resposta do backend");
      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Backend error: ${response.status} ${errText}`);
      }

      const data = await response.json();
      setRawResponse(data);

      // Ajusta o formato para o tipo esperado
      const realResult: AnalysisResult = {
        examType: data.examType || "Desconhecido",
        diagnosis: data.diagnosis || "Sem diagnóstico disponível",
        confidence: typeof data.confidence === "number" ? data.confidence : 0,
      };

      setResult(realResult);
      toast.success("Análise concluída com sucesso!");
    } catch (error) {
      console.error("Erro na análise:", error);
      toast.error("Erro ao analisar a imagem. Usando resultado mock.");

      // Fallback: mantém um resultado mock para que a UI continue funcionando
      const mockResult: AnalysisResult = {
        examType: "Raio-X Torácico",
        diagnosis:
          "Exame dentro dos padrões de normalidade. Não foram identificadas alterações significativas nas estruturas pulmonares e cardíacas.",
        confidence: 94,
      };

      setRawResponse(null);
      setResult(mockResult);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: "var(--gradient-bg)" }}>
      <Header />
      
      <main className="container mx-auto px-6 pt-32 pb-20">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16 animate-in fade-in-50 slide-in-from-bottom-4 duration-700">
            <h1 className="text-5xl md:text-6xl font-bold mb-10 tracking-tight">
              <span className="text-6xl md:text-7xl text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary/60 animate-in fade-in-50">
                Iris AI
              </span>
              <br />
              <span className="text-5xl md:text-6xl font-bold text-foreground">
                O futuro do diagnóstico
              </span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
              Envie imagens de exames médicos e receba classificação automática
              do tipo de exame e diagnóstico assistido por IA
            </p>
            {/* <div className="flex gap-4 justify-center">
              <Button
                variant="default"
                size="lg"
                className="gap-2"
                onClick={() => document.getElementById("file-upload")?.click()}
              >
                <Github className="h-5 w-5" />
                Ver no GitHub
              </Button>
            </div> */}
          </div>

          {/* Upload Zone */}
          <div className="mb-8">
            <UploadZone onUpload={handleUpload} />
          </div>

          {/* Loading State */}
          {isAnalyzing && (
            <div className="flex flex-col items-center justify-center py-12 animate-in fade-in-50">
              <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
              <p className="text-lg text-muted-foreground">
                Analisando imagem...
              </p>
            </div>
          )}

          {/* Results */}
          {result && !isAnalyzing && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Resultado da Análise</h2>
              <ResultCard
                examType={result.examType}
                diagnosis={result.diagnosis}
                confidence={result.confidence}
              />
              {rawResponse && (
                <div className="mt-4 p-4 bg-muted/50 rounded">
                  <h3 className="text-sm font-medium mb-2">Resposta bruta (debug)</h3>
                  <pre className="text-xs overflow-auto max-h-48 p-2 bg-card rounded">
                    {JSON.stringify(rawResponse, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* Info Section */}
          {!result && !isAnalyzing && (
            <div className="mt-16 text-center">
              <div className="grid md:grid-cols-3 gap-6">
                <div className="p-6">
                  <div className="w-12 h-12 rounded-full bg-accent mx-auto mb-4 flex items-center justify-center">
                    <span className="text-2xl font-bold text-accent-foreground">1</span>
                  </div>
                  <h3 className="font-semibold mb-2">Faça Upload</h3>
                  <p className="text-sm text-muted-foreground">
                    Envie uma imagem de exame médico em formato JPG
                  </p>
                </div>
                <div className="p-6">
                  <div className="w-12 h-12 rounded-full bg-accent mx-auto mb-4 flex items-center justify-center">
                    <span className="text-2xl font-bold text-accent-foreground">2</span>
                  </div>
                  <h3 className="font-semibold mb-2">Análise Automática</h3>
                  <p className="text-sm text-muted-foreground">
                    Nosso modelo de ML processa e classifica a imagem
                  </p>
                </div>
                <div className="p-6">
                  <div className="w-12 h-12 rounded-full bg-accent mx-auto mb-4 flex items-center justify-center">
                    <span className="text-2xl font-bold text-accent-foreground">3</span>
                  </div>
                  <h3 className="font-semibold mb-2">Receba o Resultado</h3>
                  <p className="text-sm text-muted-foreground">
                    Veja o tipo de exame identificado e o diagnóstico
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Index;
