import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import { useState } from "react";

const PARAM_COLORS = {
  salinity: "#3b82f6",
  temperature: "#f97316",
  pH: "#10b981",
  turbidity: "#8b5cf6"
};

const PARAM_LABELS = {
  salinity: "Salinité",
  temperature: "Température",
  pH: "pH",
  turbidity: "Turbidité"
};

const PARAM_Y_DOMAIN = {
  salinity: [0, 10],
  temperature: [0, 40],
  pH: [0, 14],
  turbidity: [0, 100]
};

const ParameterChart = ({ data }) => {
  const [selectedParam, setSelectedParam] = useState("salinity");

  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-4 rounded-xl shadow-md w-full text-center text-gray-500">
        Aucune donnée disponible pour ce paramètre.
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-xl shadow-md w-full">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          Évolution de {PARAM_LABELS[selectedParam]} sur 24h
        </h3>
        <select
          className="mt-2 sm:mt-0 bg-gray-100 px-3 py-1.5 text-sm rounded-lg border border-gray-300 shadow-sm focus:outline-none"
          value={selectedParam}
          onChange={(e) => setSelectedParam(e.target.value)}
        >
          {Object.keys(PARAM_COLORS).map((param) => (
            <option key={param} value={param}>
              {PARAM_LABELS[param]}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" tick={{ fontSize: 11 }} />
          <YAxis domain={PARAM_Y_DOMAIN[selectedParam]} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey={selectedParam}
            stroke={PARAM_COLORS[selectedParam]}
            strokeWidth={2}
            dot={{ r: 3 }}
            isAnimationActive={true}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ParameterChart;
