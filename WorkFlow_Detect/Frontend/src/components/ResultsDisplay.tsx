import { Card } from "@/components/ui/card";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface WorkflowResult {
  input: string;
  appName?: string;
  action?: string;
  error?: string;
}

interface ResultsDisplayProps {
  results: WorkflowResult[];
  isLoading: boolean;
}

const ResultsDisplay = ({ results, isLoading }: ResultsDisplayProps) => {
  if (isLoading) {
    return (
      <Card className="p-6 shadow-lg border-border/50 bg-card/80 backdrop-blur-sm flex items-center justify-center min-h-[400px]">
        <div className="text-center space-y-4">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto" />
          <div>
            <p className="text-lg font-medium text-foreground">Interpreting workflow steps...</p>
            <p className="text-sm text-muted-foreground">This will only take a moment</p>
          </div>
        </div>
      </Card>
    );
  }

  if (results.length === 0) {
    return (
      <Card className="p-6 shadow-lg border-border/50 bg-card/80 backdrop-blur-sm flex items-center justify-center min-h-[400px]">
        <div className="text-center text-muted-foreground space-y-2">
          <div className="w-16 h-16 rounded-full bg-muted/50 flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8" />
          </div>
          <p className="text-lg font-medium">No results yet</p>
          <p className="text-sm">Enter workflow steps and click "Interpret Steps" to begin</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6 shadow-lg border-border/50 bg-card/80 backdrop-blur-sm">
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Results</h2>
          <div className="text-sm text-muted-foreground">
            {results.length} step{results.length !== 1 ? 's' : ''} processed
          </div>
        </div>

        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
          {results.map((result, index) => (
            <div
              key={index}
              className={cn(
                "p-4 rounded-lg border transition-all hover:shadow-md",
                result.error
                  ? "bg-destructive/5 border-destructive/20"
                  : "bg-success/5 border-success/20"
              )}
            >
              <div className="flex items-start gap-3">
                <div className="mt-0.5">
                  {result.error ? (
                    <XCircle className="w-5 h-5 text-destructive" />
                  ) : (
                    <CheckCircle2 className="w-5 h-5 text-success" />
                  )}
                </div>

                <div className="flex-1 space-y-2">
                  <p className="text-sm font-mono text-foreground/80 bg-muted/30 px-3 py-2 rounded border border-border/50">
                    {result.input}
                  </p>

                  {result.error ? (
                    <p className="text-sm text-destructive font-medium">{result.error}</p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">
                        {result.appName}
                      </span>
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-secondary/10 text-secondary border border-secondary/20">
                        {result.action}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
};

export default ResultsDisplay;
