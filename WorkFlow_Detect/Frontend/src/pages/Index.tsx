import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Loader2, FileText, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import ResultsDisplay from "@/components/ResultsDisplay";

interface WorkflowResult {
  input: string;
  appName?: string;
  action?: string;
  error?: string;
}

const Index = () => {
  const [input, setInput] = useState("");
  const [results, setResults] = useState<WorkflowResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async () => {
    if (!input.trim()) {
      toast({
        title: "Empty Input",
        description: "Please enter workflow steps to interpret.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      // Split input by lines and filter out empty lines
      const steps = input.split('\n').filter(step => step.trim().length > 0);
      
      const response = await fetch('http://127.0.0.1:8000/suggest_steps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow_step_descriptions: steps })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Transform API response to match frontend interface
      const transformedResults = data.results.map((result: any, index: number) => ({
        input: steps[index],
        appName: result.app_name,
        action: result.action_name,
        error: result.error
      }));
      
      setResults(transformedResults);

      toast({
        title: "Success",
        description: `Processed ${transformedResults.length} workflow steps.`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to process workflow steps. Make sure the API is running.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setInput("");
    setResults([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/30">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-secondary mb-4 shadow-lg">
            <FileText className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent mb-3">
            Workflow Step Interpreter
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter your workflow steps below, one per line. We'll identify the app and action for each step.
          </p>
        </header>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Input Section */}
          <Card className="p-6 shadow-lg border-border/50 bg-card/80 backdrop-blur-sm">
            <div className="space-y-4">
              <div>
                <label htmlFor="workflow-input" className="text-sm font-medium text-foreground mb-2 block">
                  Workflow Steps
                </label>
                <Textarea
                  id="workflow-input"
                  placeholder="Example:&#10;Send email to customer&#10;Post message to Slack&#10;Schedule calendar event&#10;Upload file to Drive"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="min-h-[300px] font-mono text-sm resize-none bg-background/50"
                  disabled={isLoading}
                />
              </div>

              <div className="flex gap-3">
                <Button 
                  onClick={handleSubmit} 
                  disabled={isLoading || !input.trim()}
                  className="flex-1 bg-gradient-to-r from-primary to-secondary hover:opacity-90 shadow-md"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <FileText className="mr-2 h-4 w-4" />
                      Interpret Steps
                    </>
                  )}
                </Button>
                
                <Button 
                  onClick={handleClear}
                  variant="outline"
                  disabled={isLoading}
                  className="hover:bg-muted"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>

          {/* Results Section */}
          <ResultsDisplay results={results} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default Index;
