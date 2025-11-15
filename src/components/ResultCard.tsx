import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, FileCheck } from "lucide-react";

interface ResultCardProps {
  examType: string;
  diagnosis: string;
  confidence: number;
}

const ResultCard = ({ examType, diagnosis, confidence }: ResultCardProps) => {
  return (
    <Card
      className="p-6 animate-in fade-in-50 slide-in-from-bottom-4 duration-500"
      style={{ boxShadow: "var(--shadow-medium)" }}
    >
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-full bg-success/10 flex items-center justify-center flex-shrink-0">
          <CheckCircle2 className="h-6 w-6 text-success" />
        </div>
        <div className="flex-1 space-y-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <FileCheck className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium text-muted-foreground">
                Tipo de Exame
              </span>
            </div>
            <h3 className="text-2xl font-bold text-foreground">{examType}</h3>
          </div>

          <div className="border-t border-border pt-4">
            <h4 className="text-sm font-medium text-muted-foreground mb-2">
              Diagnóstico
            </h4>
            <p className="text-lg text-foreground leading-relaxed">
              {diagnosis}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="text-xs">
              Confiança: {confidence}%
            </Badge>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ResultCard;
