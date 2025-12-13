import { Card, CardContent } from "@/components/ui/card";

export default function MetadataCard({ metadata }) {
  return (
    <Card>
      <CardContent className="p-4 space-y-2">
        <div>Status: <b>{metadata.status}</b></div>

        {metadata.aggregates && (
          <pre className="bg-gray-100 p-2 rounded text-sm">
            {JSON.stringify(metadata.aggregates, null, 2)}
          </pre>
        )}

        {metadata.errors?.length > 0 && (
          <ul className="text-sm text-red-600 list-disc pl-4">
            {metadata.errors.map((e, i) => <li key={i}>{e}</li>)}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
