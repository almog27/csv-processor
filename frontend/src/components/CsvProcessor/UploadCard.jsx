import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

export default function UploadCard({ setFile, upload, loading }) {
  return (
    <Card>
      <CardContent className="p-4 space-y-4">
        <Input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
        <Button onClick={upload} disabled={loading} className="w-full">
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Upload CSV
        </Button>
      </CardContent>
    </Card>
  );
}
