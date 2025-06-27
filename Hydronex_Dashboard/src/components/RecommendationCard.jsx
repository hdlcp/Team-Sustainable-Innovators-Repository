export default function RecommendationCard({ title, description }) {
  return (
    <div className="bg-[#e6f9ff] border-l-4 border-blue-400 p-4 rounded-md shadow-sm">
      <p className="text-sm font-semibold text-blue-800">{title}</p>
      <p className="text-xs text-blue-700 mt-1">{description}</p>
    </div>
  );
}
