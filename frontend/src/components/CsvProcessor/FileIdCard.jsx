import { Card, CardContent } from "@/components/ui/card";

export default function FileIdCard({ fileId }) {
  return (
    <Card>
      <CardContent className="p-4 space-y-2">
        <div className="text-sm text-gray-500">File ID</div>
        <div className="font-mono break-all">{fileId}</div>
      </CardContent>
    </Card>
  );
}
